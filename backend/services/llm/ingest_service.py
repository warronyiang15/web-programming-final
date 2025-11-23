from datetime import datetime, timezone

from models.requests.llm import LLMDocumentRequest
from repository.firestore_repository import FirestoreRepository


class LLMService:
    """Handle LLM content ingestion workflows."""

    def __init__(self, repository: FirestoreRepository) -> None:
        self._repository = repository

    async def save_srt_document(self, request: LLMDocumentRequest) -> tuple[str, str]:
        """Process and store SRT content in the srtDocs collection."""

        payload = {
            "content": request.content,
            "metadata": request.metadata,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "type": "srt",
        }
        
        document_id, _ = await self._repository.create_document("srtDocs", payload)
        return document_id, payload["created_at"]

