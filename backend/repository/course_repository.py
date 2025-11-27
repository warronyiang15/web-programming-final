from __future__ import annotations

import asyncio
from datetime import datetime, timezone
from typing import Any

from google.cloud import firestore

from models.course import CourseModel


class CourseRepository:
    def __init__(self, client: firestore.Client, collection: str = "courses") -> None:
        self._client = client
        self._collection = collection

    async def create_course(self, owner_id: str,name: str) -> CourseModel:

        def _sync_create_course() -> CourseModel:
            courses_ref = self._client.collection(self._collection)
            doc_ref = courses_ref.document()
            
            now = datetime.now(timezone.utc)
            
            new_course_data = {
                "id": doc_ref.id,
                "owner_id": owner_id,
                "name": name,
                "created_at": now,
                "updated_at": now,
            }
            
            doc_ref.set(new_course_data)
            return CourseModel(**new_course_data)

        return await asyncio.to_thread(_sync_create_course)

