from .auth import router as auth_router
from .health import router as health_router
from .tasks import router as tasks_router
from .contact import router as contact_router

routers = [health_router, tasks_router, auth_router, contact_router]

