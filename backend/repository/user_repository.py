from __future__ import annotations

from google.cloud import firestore

class UserRepository:
    def __init__(self, client: firestore.Client) -> None:
        self._client = client