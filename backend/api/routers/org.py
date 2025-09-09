from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api-v1/org", tags=["org"])


class OrgPatch(BaseModel):
    plan: Optional[str] = None
    acknowledge: Optional[bool] = None
    teamMembers: Optional[int] = None


org_state = {"plan": "free", "acknowledge": False, "teamMembers": 0}


@router.get("/me")
def get_org():
    return org_state


@router.patch("")
def patch_org(data: OrgPatch):
    for k, v in data.model_dump(exclude_unset=True).items():
        org_state[k] = v
    return org_state
