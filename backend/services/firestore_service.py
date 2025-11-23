from repository.firestore_repository import FirestoreRepository


class FirestoreService:

    def __init__(self, repository: FirestoreRepository) -> None:
        self._repository = repository

    async def check_health(self, collection: str) -> dict[str, str]:
        return await self._repository.check_health(collection)

