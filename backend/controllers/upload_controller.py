from fastapi import APIRouter, Depends, UploadFile, status

from services.upload_service import UploadService

router = APIRouter(prefix="/uploads", tags=["Uploads"])


def get_upload_service() -> UploadService:
    return UploadService()


@router.post(
    "",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Upload a file",
    response_description="Metadata describing the accepted file.",
)
async def upload_file(
    file: UploadFile,
    service: UploadService = Depends(get_upload_service),
) -> dict[str, str]:

    return await service.handle_upload(file)

