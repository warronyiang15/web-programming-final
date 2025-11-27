from __future__ import annotations

import asyncio
from datetime import datetime, timezone
from typing import Any

from google.cloud import firestore

from models.user import UserModel, UserProfile


class UserRepository:
    def __init__(self, client: firestore.Client, collection: str = "user") -> None:
        self._client = client
        self._collection = collection

    async def get_or_create_user(self, profile: UserProfile) -> UserModel:

        def _sync_get_or_create() -> UserModel:
            users_ref = self._client.collection(self._collection)
            
            # query with provider:provider_id
            query = users_ref.where("provider", "==", profile.provider)\
                             .where("provider_id", "==", profile.provider_id)\
                             .limit(1)
            docs = list(query.stream())
            
            now = datetime.now(timezone.utc)

            if docs:
                # User exists
                doc = docs[0]
                data = doc.to_dict()
                
                # set the id from the document into model
                data["id"] = doc.id
                
                return UserModel(**data)

            # Create new user
            new_doc_ref = users_ref.document()
            
            new_user_data = {
                "id": new_doc_ref.id,
                "provider": profile.provider,
                "provider_id": profile.provider_id,
                "email": profile.email or "",
                "name": profile.name,
                "picture": profile.picture,
                "created_at": now,
                "updated_at": now,
            }
            
            new_doc_ref.set(new_user_data)
            return UserModel(**new_user_data)

        return await asyncio.to_thread(_sync_get_or_create)
