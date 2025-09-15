# backend/api/main.py
from fastapi import FastAPI

from backend.core.database import Base, engine

# Import your routers
from backend.api.routers import (
    health,
    tasks,
    auth,
    contact,
    pricing,
    organization,
    team,
    settings,
)

app = FastAPI(title="Tradex Backend")


@app.on_event("startup")
def on_startup() -> None:
    """Ensure database tables exist."""
    Base.metadata.create_all(bind=engine)


# Mount routers (adjust prefixes/tags if your router files define them differently)
app.include_router(health.router)   # e.g., GET /health
app.include_router(tasks.router)    # e.g., /tasks
app.include_router(auth.router)     # e.g., /auth
app.include_router(contact.router)  # e.g., /contact
app.include_router(pricing.router)  # e.g., /api-v1/pricing
app.include_router(organization.router)
app.include_router(team.router)
app.include_router(settings.router)


@app.get("/")
def root() -> dict[str, str]:
    return {"status": "ok"}

