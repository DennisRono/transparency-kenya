from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, update, delete
from datetime import datetime
from app.models.government import Ministry, Department
from app.schemas import ministry_schema

async def get_ministry(db: AsyncSession, ministry_id: int):
    query = select(Ministry).where(Ministry.id == ministry_id, Ministry.is_deleted == False)
    result = await db.execute(query)
    return result.scalar_one_or_none()

async def get_ministries(db: AsyncSession, skip: int = 0, limit: int = 100, name: Optional[str] = None):
    query = select(Ministry).where(Ministry.is_deleted == False)
    
    if name:
        query = query.where(Ministry.name.ilike(f"%{name}%"))
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

async def create_ministry(db: AsyncSession, ministry: ministry_schema.MinistryCreate):
    db_ministry = Ministry(
        name=ministry.name,
        code=ministry.code,
        description=ministry.description,
        budget_allocation=ministry.budget_allocation,
        establishment_date=ministry.establishment_date,
        website=ministry.website,
        physical_address=ministry.physical_address,
        postal_address=ministry.postal_address,
        phone_number=ministry.phone_number,
        email=ministry.email,
        is_active=ministry.is_active
    )
    db.add(db_ministry)
    await db.commit()
    await db.refresh(db_ministry)
    return db_ministry

async def update_ministry(db: AsyncSession, ministry_id: int, ministry: ministry_schema.MinistryUpdate):
    db_ministry = await get_ministry(db, ministry_id)
    
    # Update ministry attributes
    for key, value in ministry.dict(exclude_unset=True).items():
        setattr(db_ministry, key, value)
    
    await db.commit()
    await db.refresh(db_ministry)
    return db_ministry

async def delete_ministry(db: AsyncSession, ministry_id: int):
    db_ministry = await get_ministry(db, ministry_id)
    db_ministry.is_deleted = True
    db_ministry.deleted_at = datetime.now()
    await db.commit()
    return db_ministry

async def get_ministry_departments(db: AsyncSession, ministry_id: int):
    query = select(Department).where(
        Department.ministry_id == ministry_id,
        Department.is_deleted == False
    )
    result = await db.execute(query)
    return result.scalars().all()

