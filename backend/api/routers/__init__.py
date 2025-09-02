from .health import router as health_router
from .tasks import router as tasks_router
from .auth import router as auth_router

routers = [health_router, tasks_router, auth_router]

