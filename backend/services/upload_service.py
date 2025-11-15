from fastapi import UploadFile


class UploadService:

    async def handle_upload(self, file: UploadFile) -> dict[str, str]:

        return {
            "filename": file.filename,
            "content_type": file.content_type,
        }

