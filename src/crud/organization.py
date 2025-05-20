from typing import List, Optional

from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models import Organization, Activity, Building, association_org_activity


async def get_organization(db: AsyncSession, organization_id: int) -> Optional[Organization]:
    stmt = select(Organization).options(
        selectinload(Organization.activities),
        selectinload(Organization.building)
    ).where(Organization.id == organization_id)
    result = await db.execute(stmt)
    return result.scalars().first()


async def get_organizations_by_building(db: AsyncSession, building_id: int) -> List[Organization]:
    stmt = select(Organization).options(
        selectinload(Organization.activities),
        selectinload(Organization.building)
    ).where(Organization.building_id == building_id)
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_organizations_by_activity(db: AsyncSession, activity_id: int) -> List[Organization]:
    stmt = select(Activity).where(
        or_(
            Activity.id == activity_id,
            Activity.parent_id == activity_id,
            Activity.parent.has(parent_id=activity_id)
        )
    )
    activities = await db.execute(stmt)
    activity_ids = [a.id for a in activities.scalars().all()]

    if not activity_ids:
        return []

    stmt_org = (
        select(Organization)
        .options(
            selectinload(Organization.activities),
            selectinload(Organization.building)
        )
        .join(Organization.activities)
        .where(Activity.id.in_(activity_ids))
        .distinct()
    )
    result = await db.execute(stmt_org)
    return result.scalars().all()


async def get_organizations_by_area(
    db: AsyncSession,
    lat: float,
    lon: float,
    radius: Optional[float],
    min_lat: Optional[float],
    max_lat: Optional[float],
    min_lon: Optional[float],
    max_lon: Optional[float]
) -> List[Organization]:
    query = select(Organization).options(
        selectinload(Organization.activities),
        selectinload(Organization.building)
    ).join(Building).where(Building.latitude.isnot(None), Building.longitude.isnot(None))

    if radius:
        query = query.where(
            func.sqrt(
                func.pow(Building.latitude - lat, 2) +
                func.pow(Building.longitude - lon, 2)
            ) <= radius
        )
    elif all(v is not None for v in [min_lat, max_lat, min_lon, max_lon]):
        query = query.where(
            Building.latitude.between(min_lat, max_lat),
            Building.longitude.between(min_lon, max_lon)
        )
    else:
        return []

    result = await db.execute(query)
    return result.scalars().all()


async def search_organizations_by_activity(db: AsyncSession, activity_name: str) -> List[Organization]:
    subq = select(Activity.id).where(Activity.name.ilike(f"%{activity_name}%"))
    activities = await db.execute(subq)
    ids = activities.scalars().all()

    if not ids:
        return []

    sub_tree = select(Activity.id).where(
        or_(
            Activity.parent_id.in_(ids),
            Activity.parent.has(parent_id=ids[0]) 
        )
    )
    children = await db.execute(sub_tree)
    all_ids = ids + children.scalars().all()

    stmt = (
        select(Organization)
        .join(association_org_activity)
        .where(association_org_activity.c.activity_id.in_(all_ids))
        .options(
            selectinload(Organization.activities),
            selectinload(Organization.building)
        )
        .distinct()
    )
    result = await db.execute(stmt)
    return result.scalars().all()


async def search_organizations_by_name(db: AsyncSession, name: str) -> List[Organization]:
    stmt = select(Organization).options(
        selectinload(Organization.activities),
        selectinload(Organization.building)
    ).where(Organization.name.ilike(f"%{name}%"))
    result = await db.execute(stmt)
    return result.scalars().all()
