from urllib.parse import unquote

from typing import Optional

from repository.storage_repository import StorageRepository


class AgentService:
    def __init__(self, storage_repository: StorageRepository) -> None:
        self._storage_repository = storage_repository

    async def read_file(self, path: str, start_line: Optional[int], end_line: Optional[int], page: Optional[int]) -> bytes:
        decoded_path = unquote(path)
        return await self._storage_repository.read_file_from_storage(
            decoded_path, 
            start_line, 
            end_line, 
            page
        )

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