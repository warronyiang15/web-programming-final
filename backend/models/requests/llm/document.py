from typing import Any

from pydantic import BaseModel, Field


class LLMDocumentRequest(BaseModel):
    """Payload for storing LLM-generated content in Firestore."""

    content: str = Field(
        ...,
        description="The generated content (e.g., SRT, Markdown) to store.",
        examples=["This is a generated subtitle file content."],
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Optional metadata associated with the content.",
        examples=[{"source": "video_123", "language": "en"}],
    )

