from .auth import router as auth_router
from .health import router as health_router
from .tasks import router as tasks_router
from .contact import router as contact_router
from .pricing import router as pricing_router
from .organization import router as organization_router
from .team import router as team_router
from .settings import router as settings_router

routers = [
    health_router,
    tasks_router,
    auth_router,
    contact_router,
    pricing_router,
    organization_router,
    team_router,
    settings_router,
]

