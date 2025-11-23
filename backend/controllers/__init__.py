from .firestore_controller import router as firestore_router
from .health_controller import router as health_router
from .upload_controller import router as upload_router

__all__ = ["firestore_router", "health_router", "upload_router"]

