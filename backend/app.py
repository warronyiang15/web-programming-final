from fastapi import FastAPI

from config.settings import get_settings
from controllers.firestore_controller import router as firestore_router
from controllers.health_controller import router as health_router
from controllers.llm import ingest_router as llm_ingest_router
from controllers.upload_controller import router as upload_router


def create_app() -> FastAPI:
    
    settings = get_settings()
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
    )
    app.include_router(health_router, prefix=settings.api_prefix)
    app.include_router(firestore_router, prefix=settings.api_prefix)
    app.include_router(llm_ingest_router, prefix=settings.api_prefix)
    app.include_router(upload_router, prefix=settings.api_prefix)

    return app


app = create_app()
