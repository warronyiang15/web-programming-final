from __future__ import annotations

import asyncio
from typing import BinaryIO

from google.cloud import storage


class StorageRepository:

    def __init__(
        self,
        client: storage.Client,
        bucket_name: str,
    ) -> None:
        self._client = client
        self._bucket_name = bucket_name

    async def upload_file(self, destination_blob_name: str, file_obj: BinaryIO, content_type: str) -> str:
        
        def _sync_upload() -> str:
            bucket = self._client.bucket(self._bucket_name)
            blob = bucket.blob(destination_blob_name)
            
            # Rewind file to beginning just in case
            file_obj.seek(0)
            
            blob.upload_from_file(file_obj, content_type=content_type)
            
            return f"gs://{self._bucket_name}/{destination_blob_name}"

        return await asyncio.to_thread(_sync_upload)

    async def upload_file_bytes(self, destination_blob_name: str, content: bytes, content_type: str) -> str:
        
        def _sync_upload_bytes() -> str:
            bucket = self._client.bucket(self._bucket_name)
            blob = bucket.blob(destination_blob_name)
            
            blob.upload_from_string(content, content_type=content_type)
            
            return f"gs://{self._bucket_name}/{destination_blob_name}"

        return await asyncio.to_thread(_sync_upload_bytes)
