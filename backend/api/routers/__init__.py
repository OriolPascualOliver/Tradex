from .health import router as health_router
from .auth import router as auth_router

routers = [health_router, auth_router]
