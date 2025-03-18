from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from datetime import datetime
from app.models.government import Department, Agency
from app.schemas import department_schema

async def get_department(db: AsyncSession, department_id: int):
    query = select(Department).where(Department.id == department_id, Department.is_deleted == False)
    result = await db.execute(query)
    return result.scalar_one_or_none()

async def get_departments(
    db: AsyncSession, 
    skip: int = 0, 
    limit: int = 100, 
    name: Optional[str] = None,
    ministry_id: Optional[int] = None
):
    query = select(Department).where(Department.is_deleted == False)
    
    if name:
        query = query.where(Department.name.ilike(f"%{name}%"))
    
    if ministry_id:
        query = query.where(Department.ministry_id == ministry_id)
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

async def create_department(db: AsyncSession, department: department_schema.DepartmentCreate):
    db_department = Department(
        name=department.name,
        code=department.code,
        description=department.description,
        budget_allocation=department.budget_allocation,
        establishment_date=department.establishment_date,
        website=department.website,
        physical_address=department.physical_address,
        postal_address=department.postal_address,
        phone_number=department.phone_number,
        email=department.email,
        is_active=department.is_active,
        ministry_id=department.ministry_id
    )
    db.add(db_department)
    await db.commit()
    await db.refresh(db_department)
    return db_department

async def update_department(db: AsyncSession, department_id: int, department: department_schema.DepartmentUpdate):
    db_department = await get_department(db, department_id)
    
    # Update department attributes
    for key, value in department.dict(exclude_unset=True).items():
        setattr(db_department, key, value)
    
    await db.commit()
    await db.refresh(db_department)
    return db_department

async def delete_department(db: AsyncSession, department_id: int):
    db_department = await get_department(db, department_id)
    db_department.is_deleted = True
    db_department.deleted_at = datetime.now()
    await db.commit()
    return db_department

async def get_department_agencies(db: AsyncSession, department_id: int):
    query = select(Agency).where(
        Agency.department_id == department_id,
        Agency.is_deleted == False
    )
    result = await db.execute(query)
    return result.scalars().all()

