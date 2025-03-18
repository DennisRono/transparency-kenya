from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import datetime

from app.models.government import Department, Agency
from app.schemas import department_schema

def get_department(db: Session, department_id: int):
    return db.query(Department).filter(Department.id == department_id, Department.is_deleted == False).first()

def get_departments(
    db: Session, 
    skip: int = 0, 
    limit: int = 100, 
    name: Optional[str] = None,
    ministry_id: Optional[int] = None
):
    query = db.query(Department).filter(Department.is_deleted == False)
    
    if name:
        query = query.filter(Department.name.ilike(f"%{name}%"))
    
    if ministry_id:
        query = query.filter(Department.ministry_id == ministry_id)
    
    return query.offset(skip).limit(limit).all()

def create_department(db: Session, department: department_schema.DepartmentCreate):
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
    db.commit()
    db.refresh(db_department)
    return db_department

def update_department(db: Session, department_id: int, department: department_schema.DepartmentUpdate):
    db_department = get_department(db, department_id)
    
    # Update department attributes
    for key, value in department.dict(exclude_unset=True).items():
        setattr(db_department, key, value)
    
    db.commit()
    db.refresh(db_department)
    return db_department

def delete_department(db: Session, department_id: int):
    db_department = get_department(db, department_id)
    db_department.is_deleted = True
    db_department.deleted_at = datetime.now()
    db.commit()
    return db_department

def get_department_agencies(db: Session, department_id: int):
    return db.query(Agency).filter(
        Agency.department_id == department_id,
        Agency.is_deleted == False
    ).all()

