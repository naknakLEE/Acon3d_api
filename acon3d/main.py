from fastapi import FastAPI
from router.index import router

# from api.routes.api import router as api_router
from core.config import get_app_settings

def get_application() -> FastAPI:
    settings = get_app_settings()

    settings.configure_logging()

    application = FastAPI(**settings.fastapi_kwargs)

    # application.include_router(router, prefix=settings.api_prefix)
    application.include_router(router)

    return application


app = get_application()