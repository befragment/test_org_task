from typing import Optional
from pydantic import BaseModel

class ActivityBase(BaseModel):
    name: str
    parent_id: Optional[int]

class ActivityCreate(ActivityBase):
    pass

class Activity(ActivityBase):
    id: int
    class Config:
        orm_mode = True