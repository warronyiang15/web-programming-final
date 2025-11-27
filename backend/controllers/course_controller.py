from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, UploadFile, status

from config.settings import Settings, get_settings
from core.database import get_firestore_client
from core.storage import get_storage_client
from decorators.auth import required_login
from models.responses.course import CourseResponse, MultipleCourseResponse
from models.responses.error import ErrorResponse
from models.user import UserModel
from repository.course_repository import CourseRepository
from repository.storage_repository import StorageRepository
from services.course_service import CourseService

router = APIRouter(prefix="/course", tags=["Courses"])


def get_course_repository(
    settings: Settings = Depends(get_settings),
) -> CourseRepository:
    client = get_firestore_client(
        project_id=settings.firebase_project_id,
        credentials_file=settings.firebase_credentials_file,
    )
    return CourseRepository(client=client, collection="course")


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


def get_course_service(
    repository: CourseRepository = Depends(get_course_repository),
    storage_repository: StorageRepository = Depends(get_storage_repository),
) -> CourseService:
    return CourseService(repository, storage_repository)


@router.post(
    "",
    summary="Create a new course",
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse,
            "description": "Invalid file format (only PDF allowed)",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorResponse,
            "description": "User not authenticated",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": ErrorResponse,
            "description": "Server configuration error (e.g. missing GCS bucket)",
        }
    },
)
@required_login
async def create_course(
    request: Request,
    course_name: Annotated[str, Form(description="Name of the course")],
    files: Annotated[list[UploadFile], File(description="Course materials (PDF only)")],
    service: CourseService = Depends(get_course_service),
) -> CourseResponse:
    
    user_dict = request.session["user"]
    user = UserModel(**user_dict)
    
    course = await service.create_course(user, course_name, files)
    return CourseResponse(status="success", course=course)

@router.get(
    "",
    summary="Get all courses",
    response_model=MultipleCourseResponse,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorResponse,
            "description": "User not authenticated",
        }
    }
)
@required_login
async def get_all_courses(
    request: Request,
    service: CourseService = Depends(get_course_service),
) -> MultipleCourseResponse:

    user_dict = request.session["user"]
    user = UserModel(**user_dict)

    courses = await service.get_all_courses(user)

    return MultipleCourseResponse(status="success", courses=courses)