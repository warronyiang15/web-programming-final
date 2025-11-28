from pydantic import BaseModel, ConfigDict, Field


class DirectoryListResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "items": ["src/", "package.json", "README.md"],
                "raw_output": "src/\npackage.json\nREADME.md"
            }
        }
    )
    items: list[str] = Field(..., description="List of files and directories")
    raw_output: str = Field(..., description="Raw output string (newline separated)")


class DirectoryTreeResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "tree": "/project/root\n├── src/\n│   ├── app.ts\n│   └── utils.ts\n└── package.json"
            }
        }
    )
    tree: str = Field(..., description="Tree representation of the directory structure")


class FileSystemOpResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": "success",
                "message": "URI /project/src/new-feature/ successfully created."
            }
        }
    )
    status: str = Field(default="success", description="Operation status")
    message: str = Field(..., description="Success message")
