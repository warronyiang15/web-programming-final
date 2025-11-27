from pydantic import BaseModel, ConfigDict, Field

from datetime import datetime

# For OAuth data
class UserProfile(BaseModel):

    model_config = ConfigDict(extra="ignore")

    provider: str = Field(..., description="OAuth provider (google/github)")
    provider_id: str = Field(..., description="Unique ID from the provider")
    email: str | None = Field(None, description="User email")
    name: str | None = Field(None, description="User display name")
    picture: str | None = Field(None, description="Avatar URL")

# For database schema
class UserModel(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str = Field(..., description="Internal Firestore document ID")
    provider_id: str = Field(..., description="Unique ID from the provider")
    provider: str = Field(..., descrioption="OAuth provider (google/github)")
    email: str = Field(..., description="User email")
    name: str | None = Field(None, description="User display name")
    picture: str | None = Field(None, description="Avatar URL")
    created_at: datetime = Field(..., description="Timestamp of user creation")
    updated_at: datetime = Field(..., description="Timestamp of user last update")
