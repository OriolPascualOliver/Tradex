from typing import Dict, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/api-v1/team", tags=["team"])


class TeamCreate(BaseModel):
    orgId: int
    name: str
    email: str
    role: str


class TeamUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None
    active: Optional[bool] = None


team_store: Dict[int, Dict] = {}
next_team_id = 1


@router.get("")
def list_team(orgId: int):
    return [m for m in team_store.values() if m["orgId"] == orgId]


@router.post("")
def create_team(member: TeamCreate):
    global next_team_id
    data = member.model_dump()
    data.update({"id": next_team_id, "active": True})
    team_store[next_team_id] = data
    next_team_id += 1
    return data


@router.patch("/{member_id}")
def update_team(member_id: int, member: TeamUpdate):
    if member_id not in team_store:
        raise HTTPException(status_code=404, detail="Member not found")
    for k, v in member.model_dump(exclude_unset=True).items():
        team_store[member_id][k] = v
    return team_store[member_id]


@router.delete("/{member_id}")
def delete_team(member_id: int):
    if member_id not in team_store:
        raise HTTPException(status_code=404, detail="Member not found")
    del team_store[member_id]
    return {"status": "deleted"}

