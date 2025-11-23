from __future__ import annotations

import asyncio
from datetime import datetime, timezone
import os
from typing import Any

from google.cloud import firestore


class FirestoreRepository:
    """Minimal wrapper to communicate with Google Firestore."""

    def __init__(
        self,
        project_id: str | None = None,
        credentials_file: str | None = None,
    ) -> None:
        resolved_credentials_file = self._resolve_credentials_path(credentials_file)
        
        if resolved_credentials_file:
            self._client = firestore.Client.from_service_account_json(
                resolved_credentials_file,
                project=project_id,
            )
        else:
            self._client = firestore.Client(project=project_id)

    async def check_health(self, collection: str) -> dict[str, Any]:
        """Write and read a heartbeat document to verify connectivity."""

        def _write_and_read() -> dict[str, Any]:
            doc_ref = self._client.collection(collection).document("heartbeat")
            payload = {
                "status": "ok",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
            doc_ref.set(payload)
            snapshot = doc_ref.get()
            return snapshot.to_dict() or payload

        return await asyncio.to_thread(_write_and_read)

    async def create_document(self, collection: str, data: dict[str, Any]) -> tuple[str, dict[str, Any]]:
        """Store a document in the specified collection."""

        def _create() -> tuple[str, dict[str, Any]]:
            # Let Firestore auto-generate the ID by calling document() without args
            doc_ref = self._client.collection(collection).document()
            doc_ref.set(data)
            return doc_ref.id, data

        return await asyncio.to_thread(_create)

    def _resolve_credentials_path(self, explicit_path: str | None) -> str | None:
        """Return a readable credentials path, raising when an explicit path is invalid."""

        candidates = [
            explicit_path,
            os.getenv("FIREBASE_CREDENTIALS_FILE"),
            os.getenv("GOOGLE_APPLICATION_CREDENTIALS"),
        ]

        for path in candidates:
            if path:
                if os.path.exists(path):
                    return path
                if path == explicit_path:
                    raise FileNotFoundError(f"Firestore credentials file not found at '{path}'.")

        return None
