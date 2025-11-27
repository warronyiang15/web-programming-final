from fastapi import HTTPException, UploadFile, status
from models.course import CourseModel
from models.user import UserModel
from repository.course_repository import CourseRepository
from repository.storage_repository import StorageRepository


class CourseService:
    def __init__(
        self, 
        repository: CourseRepository,
        storage_repository: StorageRepository,
    ) -> None:
        self._repository = repository
        self._storage_repository = storage_repository

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
            
            await self._storage_repository.upload_file(
                destination_blob_name=destination_blob_name,
                file_obj=file.file,
                content_type=file.content_type or "application/pdf",
            )
            
        return course

    async def get_all_courses(self, user: UserModel) -> list[CourseModel]:
        # return all the courses for the user
        return await self._repository.get_all_courses_by_userId(user.id)
