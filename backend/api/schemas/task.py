from pydantic import BaseModel, ConfigDict
from typing import Optional


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


class TaskRead(TaskBase):
    id: int
    owner_id: int

    model_config = ConfigDict(from_attributes=True)
