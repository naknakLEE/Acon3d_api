from fastapi.routing import APIRouter
from acon3d.web.api import echo
from acon3d.web.api import dummy
from acon3d.web.api import docs
from acon3d.web.api import monitoring

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(docs.router)
api_router.include_router(echo.router, prefix="/echo", tags=["echo"])
api_router.include_router(dummy.router, prefix="/dummy", tags=["dummy"])
