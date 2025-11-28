from __future__ import annotations

import asyncio
from typing import Any, BinaryIO

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

    async def read_file_from_storage(self, destination_blob_path: str, start_line: int | None, end_line: int | None, page: int | None) -> bytes:

        def _sync_read_file_from_storage() -> bytes:
            bucket = self._client.bucket(self._bucket_name)
            
            # Remove leading slash if present to be flexible
            path = destination_blob_path.lstrip('/')
            
            blob = bucket.blob(path)
            
            content = blob.download_as_bytes()
            
            return content[start_line:end_line]

        return await asyncio.to_thread(_sync_read_file_from_storage)

    async def list_directory_from_storage(self, destination_blob_path: str) -> list[str]:

        def _sync_list_directory_from_storage() -> list[str]:
            bucket = self._client.bucket(self._bucket_name)
            
            # Remove leading slash if present to be flexible
            prefix = destination_blob_path.lstrip('/')
            
            # Ensure prefix ends with / if we are treating it as a folder, unless it's empty (root)
            if prefix and not prefix.endswith("/"):
                prefix += "/"
                
            # Using delimiter='/' mimics a filesystem listing (non-recursive)
            blobs = bucket.list_blobs(prefix=prefix, delimiter="/")
            
            items = []
            # Iterate through blobs (files)
            for blob in blobs:
                name = blob.name
                if name.startswith(prefix):
                    name = name[len(prefix):]
                if name:  # Exclude the directory blob itself or empty strings
                    items.append(name)
            
            # Iterate through prefixes (directories)
            # Note: blobs.prefixes is populated only after iterating through blobs
            if blobs.prefixes:
                for p in blobs.prefixes:
                    name = p
                    if name.startswith(prefix):
                        name = name[len(prefix):]
                    items.append(name)
            
            return sorted(items)

        return await asyncio.to_thread(_sync_list_directory_from_storage)
    
    async def list_directory_as_tree_from_storage(self, destination_blob_path: str) -> str:
        
        def _sync_list_directory_as_tree() -> str:
            bucket = self._client.bucket(self._bucket_name)
            
            # Remove leading slash if present to be flexible
            prefix = destination_blob_path.lstrip('/')
            
            blobs = list(bucket.list_blobs(prefix=prefix))
            
            if not blobs:
                return ""
                
            # Build directory tree
            tree: dict[str, Any] = {}
            for blob in blobs:
                # Get relative path
                name = blob.name
                if name.startswith(prefix):
                    rel_path = name[len(prefix):]
                    # Remove leading slash if present
                    if rel_path.startswith("/"):
                        rel_path = rel_path[1:]
                    
                    if not rel_path:
                        continue
                        
                    parts = [p for p in rel_path.split("/") if p]
                    current = tree
                    for part in parts:
                        if part not in current:
                            current[part] = {}
                        current = current[part]
            
            # Generate tree string
            lines = [prefix if prefix else "."]
            
            def _build_tree_string(node: dict[str, Any], prefix_str: str = ""):
                entries = sorted(node.keys())
                for i, entry in enumerate(entries):
                    is_last = i == len(entries) - 1
                    connector = "└── " if is_last else "├── "
                    lines.append(f"{prefix_str}{connector}{entry}")
                    
                    children = node[entry]
                    if children:
                        extension = "    " if is_last else "│   "
                        _build_tree_string(children, prefix_str + extension)
            
            _build_tree_string(tree)
            return "\n".join(lines)

        return await asyncio.to_thread(_sync_list_directory_as_tree)
