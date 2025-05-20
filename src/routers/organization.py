from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from crud import *
from database import get_session
from schemas import Organization
from dependecies.api_key import verify_api_key

router = APIRouter(
    prefix="/organizations",
    tags=["organizations"],
    dependencies=[Depends(verify_api_key)]
)

from fastapi import APIRouter, Query, Depends, HTTPException
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/organizations", tags=["Organizations"])


@router.get("/area", response_model=List[Organization], summary="Search organizations by area")
async def read_organizations_by_area(
    lat: float = Query(..., description="Latitude of center point, e.g. 55.75"),
    lon: float = Query(..., description="Longitude of center point, e.g. 37.62"),
    radius: Optional[float] = Query(None, description="Search radius in degrees (approximate)"),
    min_lat: Optional[float] = Query(None, description="Minimum latitude for bounding box"),
    max_lat: Optional[float] = Query(None, description="Maximum latitude for bounding box"),
    min_lon: Optional[float] = Query(None, description="Minimum longitude for bounding box"),
    max_lon: Optional[float] = Query(None, description="Maximum longitude for bounding box"),
    db: AsyncSession = Depends(get_session)
):
    """
    Search organizations within a geographical area.

    You can specify either a radius (distance from point) or bounding box (min/max lat/lon).
    """
    return await get_organizations_by_area(db, lat, lon, radius, min_lat, max_lat, min_lon, max_lon)


@router.get("/building/{building_id}", response_model=List[Organization], summary="Get organizations by building ID")
async def read_organizations_by_building(
    building_id: int,
    db: AsyncSession = Depends(get_session)
):
    """
    Retrieve all organizations located in a specific building.
    """
    return await get_organizations_by_building(db, building_id)



@router.get("/activity/{activity_id}", response_model=List[Organization], summary="Get organizations by activity ID")
async def read_organizations_by_activity(
    activity_id: int,
    db: AsyncSession = Depends(get_session)
):
    """
    Retrieve organizations linked to a specific activity or its sub-activities.
    """
    return await get_organizations_by_activity(db, activity_id)


@router.get("/search_by_activity", response_model=List[Organization], summary="Search organizations by activity name")
async def search_orgs_by_activity(
    activity_name: str = Query(..., description="Partial or full name of the activity to search"),
    db: AsyncSession = Depends(get_session)
):
    """
    Search organizations by activity name (supports partial matches).
    """
    return await search_organizations_by_activity(db, activity_name)


@router.get("/search_by_name", response_model=List[Organization], summary="Search organizations by name")
async def search_orgs_by_name(
    name: str = Query(..., description="Partial or full name of the organization to search"),
    db: AsyncSession = Depends(get_session)
):
    """
    Search organizations by their name (supports partial matches).
    """
    return await search_organizations_by_name(db, name)


@router.get("/{organization_id}", response_model=Organization, summary="Get organization by ID")
async def read_organization(
    organization_id: int,
    db: AsyncSession = Depends(get_session)
):
    """
    Retrieve a single organization by its unique ID.
    """
    organization = await get_organization(db, organization_id)
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    return organization
