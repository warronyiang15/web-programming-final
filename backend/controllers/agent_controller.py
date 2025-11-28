from typing import Optional

from fastapi import APIRouter, Body, Depends, HTTPException, Query, Request, Response, status

from config.settings import Settings, get_settings
from core.storage import get_storage_client
from decorators.auth import required_api_key
from models.requests.agent import FileSystemCreateRequest, FileSystemEditRequest, FileSystemRewriteRequest
from models.responses.agent import DirectoryListResponse, DirectoryTreeResponse, FileSystemOpResponse
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

@router.post(
    '/filesystem/create',
    summary="Create a new file or directory",
    response_model=FileSystemOpResponse,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse,
            "description": "Invalid request parameters",
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
async def create_file_or_folder(
    request: Request,
    payload: FileSystemCreateRequest,
    service: AgentService = Depends(get_agent_service),
) -> FileSystemOpResponse:
    await service.create_file_or_folder(payload.path)
    return FileSystemOpResponse(
        message=f"URI {payload.path} successfully created."
    )

@router.delete(
    '/filesystem/delete',
    summary="Delete a file or directory",
    response_model=FileSystemOpResponse,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse,
            "description": "Invalid request parameters",
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
async def delete_file_or_folder(
    request: Request,
    path: str = Query(..., description="Path to the file or directory to delete"),
    recursive: Optional[bool] = Query(False, description="Recursively delete folder content (ignored, always force delete for folders)"),
    service: AgentService = Depends(get_agent_service),
) -> FileSystemOpResponse:
    await service.delete_file_or_folder(path, recursive)
    return FileSystemOpResponse(
        message=f"URI {path} successfully deleted."
    )

@router.put(
    '/files/content',
    summary="Rewrite the content of a file",
    response_model=FileSystemOpResponse,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse,
            "description": "Invalid request parameters",
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
async def rewrite_file_content(
    request: Request,
    payload: FileSystemRewriteRequest,
    service: AgentService = Depends(get_agent_service),
) -> FileSystemOpResponse:
    await service.rewrite_file(payload.path, payload.content)
    return FileSystemOpResponse(
        message=f"Change successfully made to {payload.path}."
    )

@router.patch(
    '/files/edit',
    summary="Edit the contents of a file",
    response_model=FileSystemOpResponse,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse,
            "description": "Invalid request parameters or patch application failed",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorResponse,
            "description": "X-LLM-API-Key is not valid or missing",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "File not found",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": ErrorResponse,
            "description": "Server configuration error (e.g. missing GCS bucket)",
        },
    },
)
@required_api_key
async def edit_file_content(
    request: Request,
    payload: FileSystemEditRequest,
    service: AgentService = Depends(get_agent_service),
) -> FileSystemOpResponse:
    await service.edit_file(payload.uri, payload.search_replace_blocks)
    return FileSystemOpResponse(
        message=f"Change successfully made to {payload.uri}."
    )
