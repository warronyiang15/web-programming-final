from pydantic import BaseModel, ConfigDict, Field


class FirestoreHealthResponse(BaseModel):

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": "ok",
                "timestamp": "2025-01-01T00:00:00.000000+00:00",
            }
        }
    )

    status: str = Field(
        ...,
        description="Result of the connectivity check.",
        example="ok",
    )
    timestamp: str = Field(
        ...,
        description="UTC timestamp recorded during the health check.",
        example="2025-01-01T00:00:00.000000+00:00",
    )

