from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/api-v1/team", tags=["team"])

TEAM_MEMBERS: dict[int, dict] = {}
NEXT_ID = 1


class TeamCreate(BaseModel):
    orgId: int
    name: str
    email: str
    role: str


class TeamUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    role: str | None = None
    active: bool | None = None


@router.get("")
def list_team(orgId: int):  # noqa: N803 (FastAPI query param style)
    return list(TEAM_MEMBERS.values())


@router.post("")
def create_team_member(member: TeamCreate):
    global NEXT_ID
    data = member.model_dump()
    data.update({"id": NEXT_ID, "active": True})
    TEAM_MEMBERS[NEXT_ID] = data
    NEXT_ID += 1
    return data


@router.patch("/{member_id}")
def update_team_member(member_id: int, patch: TeamUpdate):
    member = TEAM_MEMBERS.get(member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    for key, value in patch.model_dump(exclude_unset=True).items():
        member[key] = value
    return member


@router.delete("/{member_id}")
def delete_team_member(member_id: int):
    TEAM_MEMBERS.pop(member_id, None)
    return {"status": "deleted"}
