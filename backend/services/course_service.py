from datetime import datetime, timezone
from typing import Any

from fastapi import HTTPException, UploadFile, status
from google.api_core.exceptions import GoogleAPICallError

from models.course import CourseModel
from models.message import MessageModel, Role
from models.user import UserModel
from repository.course_repository import CourseRepository
from repository.message_repository import MessageRepository
from repository.storage_repository import StorageRepository


class CourseService:
    def __init__(
        self, 
        repository: CourseRepository,
        storage_repository: StorageRepository,
        message_repository: MessageRepository,
    ) -> None:
        self._repository = repository
        self._storage_repository = storage_repository
        self._message_repository = message_repository
    
    async def create_course(self, user: UserModel, name: str, files: list[UploadFile]) -> CourseModel:
        
        # Validate files are PDFs
        for file in files:
            if file.content_type != "application/pdf":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"File '{file.filename}' is not a PDF. Only PDF files are allowed.",
                )

        # 1. Create the course document first to get the ID
        course = await self._repository.create_course(user.id, name)
        
        # 2. Upload files to GCS under /{course_id}/
        for file in files:
            if not file.filename:
                continue
                
            destination_blob_name = f"{course.id}/{file.filename}"
            
            try:
                # Read file content asynchronously to avoid blocking and potential stream issues
                content = await file.read()
                
                await self._storage_repository.upload_file_bytes(
                    destination_blob_name=destination_blob_name,
                    content=content,
                    content_type=file.content_type or "application/pdf",
                )
            except Exception as exc:
                print(f"Failed to upload {file.filename}: {exc}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Failed to upload file {file.filename} to storage.",
                ) from exc
            
        return course

    async def get_all_courses(self, user: UserModel) -> list[CourseModel]:
        # return all the courses for the user
        return await self._repository.get_all_courses_by_userId(user.id)

    async def get_course_by_id(self, course_id: str, user: UserModel) -> CourseModel | None:
        course = await self._repository.get_course_by_id(course_id)
        
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Course with ID {course_id} not found.",
            )
            
        if course.owner_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this course.",
            )
            
        return course

    async def create_message_by_user(self, course_id: str, user: UserModel, content: str) -> MessageModel:
        # 1. Verify course ownership
        course = await self._repository.get_course_by_id(course_id)
        
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Course with ID {course_id} not found.",
            )
            
        if course.owner_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action on this course.",
            )

        # 2. Create the message
        # For user messages, we only set content and role
        
        message_data = MessageModel(
            id="", # Placeholder, will be set by repository
            index=0, # Placeholder, will be set by repository
            course_id=course_id,
            role=Role.USER,
            content=content,
            createdAt=datetime.now(timezone.utc)
        )
        
        return await self._message_repository.create_message(course_id, message_data)

    async def get_messages_by_course_id(self, course_id: str, user: UserModel) -> list[MessageModel]:
        # 1. Verify course ownership
        course = await self._repository.get_course_by_id(course_id)

        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Course with ID {course_id} not found.",
            )
            
        if course.owner_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action on this course.",
            )
        
        return await self._message_repository.get_all_messages_by_course_id(course_id)