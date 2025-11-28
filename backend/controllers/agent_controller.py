from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response, status

from config.settings import Settings, get_settings
from core.storage import get_storage_client
from decorators.auth import required_api_key
from models.responses.agent import DirectoryListResponse, DirectoryTreeResponse
from models.responses.error import ErrorResponse
from repository.storage_repository import StorageRepository
from services.agent_service import AgentService


router = APIRouter(prefix="/agent", tags=['Agent'])

def get_storage_repository(
    settings: Settings = Depends(get_settings),
) -> StorageRepository:
    if not settings.gcs_bucket_name:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="GCS_BUCKET_NAME is not configured.",
        )

    client = get_storage_client(
        project_id=settings.firebase_project_id,
        credentials_file=settings.firebase_credentials_file,
    )
    return StorageRepository(client=client, bucket_name=settings.gcs_bucket_name)

def get_agent_service(
    repository: StorageRepository = Depends(get_storage_repository),
) -> AgentService:
    return AgentService(repository)

@router.get(
    '/files/content',
    summary="Get the content of a file",
    response_class=Response,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse,
            "description": "File Not Found",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorResponse,
            "description": "X-LLM-API-Key is not valid or missing",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": ErrorResponse,
            "description": "Server configuration error (e.g. missing GCS bucket)",
        },
    },
)
@required_api_key
async def get_file_content(
    request: Request,
    path: str = Query(..., description="Path to the file"),
    start_line: Optional[int] = Query(None, description="Start line of the content"),
    end_line: Optional[int] = Query(None, description="End line of the content"),
    page: Optional[int] = Query(None, description="Page number of the content"),
    service: AgentService = Depends(get_agent_service),
) -> Response:
    content = await service.read_file(path, start_line, end_line, page)
    return Response(content=content, media_type="application/octet-stream")

@router.get(
    '/directories/list',
    summary="List the contents of a directory",
    response_model=DirectoryListResponse,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse,
            "description": "Directory Not Found",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorResponse,
            "description": "X-LLM-API-Key is not valid or missing",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": ErrorResponse,
            "description": "Server configuration error (e.g. missing GCS bucket)",
        },
    },
)
@required_api_key
async def list_directory(
    request: Request,
    path: str = Query(..., description="Path to the directory"),
    service: AgentService = Depends(get_agent_service),
) -> DirectoryListResponse:
    items = await service.list_directory(path)
    return DirectoryListResponse(
        items=items,
        raw_output="\n".join(items)
    )

@router.get(
    '/directories/tree',
    summary="List the contents of a directory as a tree",
    response_model=DirectoryTreeResponse,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse,
            "description": "Directory Not Found",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorResponse,
            "description": "X-LLM-API-Key is not valid or missing",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": ErrorResponse,
            "description": "Server configuration error (e.g. missing GCS bucket)",
        },
    },
)
@required_api_key
async def list_directory_as_tree(
    request: Request,
    path: str = Query(..., description="Path to the directory"),
    service: AgentService = Depends(get_agent_service),
) -> DirectoryTreeResponse:
    tree_str = await service.list_directory_as_tree(path)
    return DirectoryTreeResponse(tree=tree_str)
