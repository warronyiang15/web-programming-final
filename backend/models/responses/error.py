from pydantic import BaseModel, ConfigDict, Field


class ErrorResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "detail": "User not authenticated"
            }
        }
    )
    detail: str = Field(..., description="Error detail message")

