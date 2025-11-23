from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class LLMDocumentResponse(BaseModel):
    """Response returned after storing LLM content."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "document_id": "auto-generated-id",
                "collection": "srtDocs",
                "timestamp": "2025-01-01T00:00:00.000000+00:00",
            }
        }
    )

    document_id: str = Field(
        ...,
        description="Unique identifier of the stored document.",
        example="auto-generated-id",
    )
    collection: str = Field(
        ...,
        description="Firestore collection where the document resides.",
        example="srtDocs",
    )
    timestamp: str = Field(
        ...,
        description="UTC timestamp of when the document was stored.",
        example="2025-01-01T00:00:00.000000+00:00",
    )

