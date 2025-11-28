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


class FileSystemEditRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "uri": "/project/src/config.ts",
                "search_replace_blocks": "${ORIGINAL}\nconst debug = false;\n${DIVIDER}\nconst debug = true;\n${FINAL}"
            }
        }
    )
    uri: str = Field(..., description="The FULL path to the file.")
    search_replace_blocks: str = Field(..., description="A string of SEARCH/REPLACE block(s) which will be applied to the given file.")
