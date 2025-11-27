from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request, status

from config.settings import Settings, get_settings
from core.database import get_firestore_client
from models.user import UserModel, UserProfile
from repository.user_repository import UserRepository
from services.user_service import UserService

from datetime import datetime

router = APIRouter(prefix="/user", tags=["Users"])

def get_user_repository(
    settings: Settings = Depends(get_settings),
) -> UserRepository:
    client = get_firestore_client(
        project_id=settings.firebase_project_id,
        credentials_file=settings.firebase_credentials_file,
    )
    return UserRepository(client=client, collection="user")


def get_user_service(
    settings: Settings = Depends(get_settings),
    repository: UserRepository = Depends(get_user_repository),
) -> UserService:
    return UserService(settings, repository)


async def _fetch_user_info(client: Any, provider: str, token: dict[str, Any]) -> UserProfile:
    
    if provider == "google":
        user_info = token.get("userinfo", {})
        return UserProfile(
            provider=provider,
            provider_id=user_info.get("sub"),
            email=user_info.get("email"),
            name=user_info.get("name"),
            picture=user_info.get("picture"),
        )
        
    if provider == "github":
        resp = await client.get("user", token=token)
        profile = resp.json()
        return UserProfile(
            provider=provider,
            provider_id=str(profile.get("id")),
            email=profile.get("email"),
            name=profile.get("name"),
            picture=profile.get("avatar_url"),
        )
        
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"Unsupported provider: {provider}",
    )


@router.get("/login/{provider}", summary="Initiate OAuth login")
async def login(
    request: Request,
    provider: str,
    service: UserService = Depends(get_user_service),
) -> Any:
    
    client = service.oauth.create_client(provider)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Provider '{provider}' not configured.",
        )
    
    redirect_uri = request.url_for("auth_callback", provider=provider)
    return await client.authorize_redirect(request, redirect_uri)


@router.get("/callback/{provider}", name="auth_callback", summary="OAuth callback handler")
async def auth_callback(
    request: Request,
    provider: str,
    service: UserService = Depends(get_user_service),
) -> UserProfile:
    
    client = service.oauth.create_client(provider)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Provider '{provider}' not configured.",
        )

    try:
        token = await client.authorize_access_token(request)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"OAuth error: {exc}",
        ) from exc

    user_profile = await _fetch_user_info(client, provider, token)
    
    # Sync with database
    user_model = await service.get_user(user_profile)
    
    # Store dict in session, return model to API
    request.session['user'] = user_model.model_dump(mode='json')
    
    return user_model
