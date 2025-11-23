from google.api_core.exceptions import GoogleAPICallError, PermissionDenied
from google.auth.exceptions import DefaultCredentialsError
from fastapi import APIRouter, Depends, HTTPException, status

from config.settings import Settings, get_settings
from models.responses.firestore import FirestoreHealthResponse
from repository.firestore_repository import FirestoreRepository
from services.firestore_service import FirestoreService

router = APIRouter(prefix="/firestore", tags=["Firestore"])


def get_firestore_repository(
    settings: Settings = Depends(get_settings),
) -> FirestoreRepository:
    try:
        return FirestoreRepository(
            project_id=settings.firebase_project_id,
            credentials_file=settings.firebase_credentials_file,
        )
    except (DefaultCredentialsError, FileNotFoundError, ValueError) as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unable to initialise Firestore client: {exc}",
        ) from exc


def get_firestore_service(
    repository: FirestoreRepository = Depends(get_firestore_repository),
) -> FirestoreService:
    return FirestoreService(repository)


@router.get(
    "/health",
    response_model=FirestoreHealthResponse,
    summary="Check Firestore connectivity",
    response_description="Status returned after a Firestore read/write heartbeat.",
)
async def firestore_health_check(
    service: FirestoreService = Depends(get_firestore_service),
    settings: Settings = Depends(get_settings),
) -> FirestoreHealthResponse:
    try:
        payload = await service.check_health(settings.firestore_health_collection)
    except PermissionDenied as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Firestore credentials lack required permissions.",
        ) from exc
    except GoogleAPICallError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(exc),
        ) from exc

    return FirestoreHealthResponse(**payload)

