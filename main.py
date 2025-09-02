from fastapi import FastAPI

from backend.api.routers import routers

app = FastAPI()
for router in routers:
    app.include_router(router)
