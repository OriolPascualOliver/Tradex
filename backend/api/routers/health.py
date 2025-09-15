from fastapi import APIRouter, status

router = APIRouter(prefix="/api-v1/health", tags=["health"])

@router.get("/", status_code=status.HTTP_200_OK)
def health():
    return {"status": "ok"}

@router.post("/postHealth", status_code=status.HTTP_200_OK)
@router.post("/post", status_code=status.HTTP_200_OK)
async def health_post():
    return {"status": "ok"}