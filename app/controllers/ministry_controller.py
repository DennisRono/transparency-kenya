import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.government import Ministry, Department
from app.schemas import ministry_schema

def get_ministry(db: Session, ministry_id: int):
    return db.query(Ministry).filter(Ministry.id == ministry_id, Ministry.is_deleted == False).first()

def get_ministries(db: Session, skip: int = 0, limit: int = 100, name: Optional[str] = None):
    query = db.query(Ministry).filter(Ministry.is_deleted == False)
    
    if name:
        query = query.filter(Ministry.name.ilike(f"%{name}%"))
    
    return query.offset(skip).limit(limit).all()

def create_ministry(db: Session, ministry: ministry_schema.MinistryCreate):
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
    db.commit()
    db.refresh(db_ministry)
    return db_ministry

def update_ministry(db: Session, ministry_id: int, ministry: ministry_schema.MinistryUpdate):
    db_ministry = get_ministry(db, ministry_id)
    
    # Update ministry attributes
    for key, value in ministry.dict(exclude_unset=True).items():
        setattr(db_ministry, key, value)
    
    db.commit()
    db.refresh(db_ministry)
    return db_ministry

def delete_ministry(db: Session, ministry_id: int):
    db_ministry = get_ministry(db, ministry_id)
    db_ministry.is_deleted = True
    db_ministry.deleted_at = datetime.now()
    db.commit()
    return db_ministry

def get_ministry_departments(db: Session, ministry_id: int):
    return db.query(Department).filter(
        Department.ministry_id == ministry_id,
        Department.is_deleted == False
    ).all()

