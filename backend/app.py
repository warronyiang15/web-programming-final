from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware

from config.settings import get_settings
from controllers.course_controller import router as course_router
from controllers.firestore_controller import router as firestore_router
from controllers.health_controller import router as health_router
from controllers.llm import ingest_router as llm_ingest_router
from controllers.user_controller import router as user_router


def create_app() -> FastAPI:
    
    settings = get_settings()
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
    )
    
    # Trust headers from load balancers (e.g., Cloud Run)
    # This ensures request.url_for() generates https links when running behind TLS termination
    app.add_middleware(ProxyHeadersMiddleware, trusted_hosts="*")
    
    # Required for Authlib/OAuth to handle state and redirects
    app.add_middleware(SessionMiddleware, secret_key=settings.auth_secret_key)

    app.include_router(health_router, prefix=settings.api_prefix)
    app.include_router(firestore_router, prefix=settings.api_prefix)
    app.include_router(llm_ingest_router, prefix=settings.api_prefix)
    app.include_router(user_router, prefix=settings.api_prefix)
    app.include_router(course_router, prefix=settings.api_prefix)

    return app


app = create_app()
