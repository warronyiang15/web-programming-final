from pydantic import BaseModel, ConfigDict, Field

from datetime import datetime

class UserProfile(BaseModel):

    model_config = ConfigDict(extra="ignore")

    provider: str = Field(..., description="OAuth provider (google/github)")
    provider_id: str = Field(..., description="Unique ID from the provider")
    email: str | None = Field(None, description="User email")
    name: str | None = Field(None, description="User display name")
    picture: str | None = Field(None, description="Avatar URL")
