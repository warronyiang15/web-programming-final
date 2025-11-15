from fastapi import FastAPI

from config.settings import get_settings
from controllers.health_controller import router as health_router
from controllers.upload_controller import router as upload_router


def create_app() -> FastAPI:
    
    settings = get_settings()
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
    )
    app.include_router(health_router, prefix=settings.api_prefix)
    app.include_router(upload_router, prefix=settings.api_prefix)

    return app


app = create_app()