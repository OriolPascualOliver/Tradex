from fastapi import APIRouter

router = APIRouter(prefix="/api-v1/health")


@router.get("")
def health():
    return {"status": "ok"}

@router.post("/post")
async def health_post():
    return {"status": "ok"}