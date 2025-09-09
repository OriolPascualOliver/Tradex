from fastapi import APIRouter
from pydantic import BaseModel, Field, ConfigDict

router = APIRouter(prefix="/api-v1/org", tags=["organization"])

ORG_DATA = {"plan": "free", "acknowledge": False, "teamMembers": 1}


@router.get("/me")
def get_org_me():
    return ORG_DATA


class OrgUpdate(BaseModel):
    plan: str | None = None
    acknowledge: bool | None = None
    team_members: int | None = Field(None, alias="teamMembers")

    model_config = ConfigDict(populate_by_name=True)


@router.patch("")
def update_org(data: OrgUpdate):
    updates = data.model_dump(exclude_unset=True, by_alias=True)
    ORG_DATA.update(updates)
    return ORG_DATA
