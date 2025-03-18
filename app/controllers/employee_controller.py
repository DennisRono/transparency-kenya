from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from datetime import datetime
from app.models.employee import Employee
from app.models.performance import PerformanceReview
from app.schemas import employee_schema

async def get_employee(db: AsyncSession, employee_id: int):
    query = select(Employee).where(
        Employee.id == employee_id,
        Employee.is_deleted == False
    )
    result = await db.execute(query)
    return result.scalar_one_or_none()

async def get_employees(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
    name: Optional[str] = None,
    position_id: Optional[int] = None,
    ministry_id: Optional[int] = None,
    department_id: Optional[int] = None,
    status: Optional[str] = None
):
    query = select(Employee).where(Employee.is_deleted == False)
    
    if name:
        query = query.where(
            or_(
                Employee.first_name.ilike(f"%{name}%"),
                Employee.last_name.ilike(f"%{name}%")
            )
        )
    
    if position_id:
        query = query.where(Employee.position_id == position_id)
    
    if ministry_id:
        query = query.where(Employee.ministry_id == ministry_id)
    
    if department_id:
        query = query.where(Employee.department_id == department_id)
    
    if status:
        query = query.where(Employee.status == status)
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

async def create_employee(db: AsyncSession, employee: employee_schema.EmployeeCreate):
    db_employee = Employee(
        first_name=employee.first_name,
        middle_name=employee.middle_name,
        last_name=employee.last_name,
        gender=employee.gender,
        date_of_birth=employee.date_of_birth,
        national_id=employee.national_id,
        passport_number=employee.passport_number,
        tax_id=employee.tax_id,
        email=employee.email,
        personal_email=employee.personal_email,
        phone_number=employee.phone_number,
        alternative_phone=employee.alternative_phone,
        physical_address=employee.physical_address,
        postal_address=employee.postal_address,
        marital_status=employee.marital_status,
        nationality=employee.nationality,
        ethnicity=employee.ethnicity,
        religion=employee.religion,
        blood_group=employee.blood_group,
        disability=employee.disability,
        profile_photo=employee.profile_photo,
        
        # Employment information
        employee_number=employee.employee_number,
        hire_date=employee.hire_date,
        confirmation_date=employee.confirmation_date,
        contract_end_date=employee.contract_end_date,
        status=employee.status,
        employment_type=employee.employment_type,
        probation_period_months=employee.probation_period_months,
        notice_period_days=employee.notice_period_days,
        
        # Banking information
        bank_name=employee.bank_name,
        bank_branch=employee.bank_branch,
        account_number=employee.account_number,
        
        # Foreign keys
        position_id=employee.position_id,
        supervisor_id=employee.supervisor_id,
        ministry_id=employee.ministry_id,
        department_id=employee.department_id,
        agency_id=employee.agency_id,
        county_id=employee.county_id,
        sub_county_id=employee.sub_county_id,
        ward_id=employee.ward_id
    )
    
    db.add(db_employee)
    await db.commit()
    await db.refresh(db_employee)
    return db_employee

async def update_employee(db: AsyncSession, employee_id: int, employee: employee_schema.EmployeeUpdate):
    db_employee = await get_employee(db, employee_id)
    
    # Update employee attributes
    for key, value in employee.dict(exclude_unset=True).items():
        setattr(db_employee, key, value)
    
    await db.commit()
    await db.refresh(db_employee)
    return db_employee

async def delete_employee(db: AsyncSession, employee_id: int):
    db_employee = await get_employee(db, employee_id)
    db_employee.is_deleted = True
    db_employee.deleted_at = datetime.now()
    await db.commit()
    return db_employee

async def get_employee_performance_reviews(db: AsyncSession, employee_id: int):
    query = select(PerformanceReview).where(
        PerformanceReview.employee_id == employee_id,
        PerformanceReview.is_deleted == False
    )
    result = await db.execute(query)
    return result.scalars().all()

