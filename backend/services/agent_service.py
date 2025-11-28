import re
from urllib.parse import unquote

from typing import Optional

from fastapi import HTTPException, status

from repository.storage_repository import StorageRepository


class AgentService:
    def __init__(self, storage_repository: StorageRepository) -> None:
        self._storage_repository = storage_repository

    async def read_file(self, path: str, start_line: Optional[int], end_line: Optional[int], page: Optional[int]) -> bytes:
        decoded_path = unquote(path)
        try:
            return await self._storage_repository.read_file_from_storage(
                decoded_path, 
                start_line, 
                end_line, 
                page
            )
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"File not found: {decoded_path}"
            ) from exc

    async def list_directory(self, path: str) -> list[str]:
        decoded_path = unquote(path)
        return await self._storage_repository.list_directory_from_storage(decoded_path)

    async def list_directory_as_tree(self, path: str) -> str:
        decoded_path = unquote(path)
        return await self._storage_repository.list_directory_as_tree_from_storage(decoded_path)

    async def create_file_or_folder(self, path: str) -> None:
        decoded_path = unquote(path)
        return await self._storage_repository.create_directory_file_from_storage(decoded_path)

    async def delete_file_or_folder(self, path: str, recursive: Optional[bool] = False) -> None:
        decoded_path = unquote(path)
        return await self._storage_repository.delete_directory_file_from_storage(decoded_path, recursive)

    async def rewrite_file(self, path: str, content: str) -> None:
        decoded_path = unquote(path)
        return await self._storage_repository.rewrite_file_from_storage(decoded_path, content)

    async def edit_file(self, path: str, search_replace_blocks: str) -> None:
        decoded_path = unquote(path)
        
        # 1. Read current content
        try:
            content_bytes = await self._storage_repository.read_file_from_storage(decoded_path, None, None, None)
            content_str = content_bytes.decode("utf-8")
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"File not found or unreadable in string format: {decoded_path}"
            ) from exc

        # 2. Parse blocks
        # Assumed format:
        # ${ORIGINAL}
        # ...
        # ${DIVIDER}
        # ...
        # ${FINAL}
        
        # Regex to match blocks
        # The pattern looks for ${ORIGINAL} ... ${DIVIDER} ... ${FINAL}
        # Using re.DOTALL to match across lines
        
        pattern = re.compile(
            r"\$\{ORIGINAL\}(.*?)\$\{DIVIDER\}(.*?)\$\{FINAL\}", 
            re.DOTALL
        )
        
        blocks = pattern.findall(search_replace_blocks)
            
        new_content = content_str
        
        for search_block, replace_block in blocks:
            # 3. Apply edit
            
            # Count occurrences
            count = new_content.count(search_block)
            
            if count == 0:
                # Skip if block not found
                continue
            if count > 1:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Search block found multiple times ({count}), ambiguous edit:\n{search_block}"
                )
            
            new_content = new_content.replace(search_block, replace_block)

        # 4. Write back
        await self._storage_repository.rewrite_file_from_storage(decoded_path, new_content)