from pydantic import BaseModel, ConfigDict, Field


class FileSystemCreateRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "path": "/project/src/new-feature/"
            }
        }
    )
    path: str = Field(..., description="Path to the file or directory. Ends with / for directory.")


class FileSystemRewriteRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "path": "/project/README.md",
                "content": "# New Content\n\nFull file content here..."
            }
        }
    )
    path: str = Field(..., description="Path to the file")
    content: str = Field(..., description="Content to rewrite")
