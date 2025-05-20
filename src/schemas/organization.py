from typing import List
from pydantic import BaseModel

from schemas import Activity, Building

class OrganizationBase(BaseModel):
    name: str
    building_id: int
    phone_numbers: List[str]

class OrganizationCreate(OrganizationBase):
    activity_ids: List[int] = []

class Organization(OrganizationBase):
    id: int
    activities: List[Activity] = []
    building: Building

    class Config:
        orm_mode = True