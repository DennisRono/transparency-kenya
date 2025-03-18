from typing import Optional, List
from datetime import date, datetime
from pydantic import BaseModel, EmailStr, validator
from enum import Enum

# Enums
class GenderEnum(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    PREFER_NOT_TO_SAY = "prefer_not_to_say"

class EmploymentStatusEnum(str, Enum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    TERMINATED = "terminated"
    ON_LEAVE = "on_leave"
    PROBATION = "probation"
    RETIRED = "retired"
    RESIGNED = "resigned"
    DECEASED = "deceased"

class MaritalStatusEnum(str, Enum):
    SINGLE = "single"
    MARRIED = "married"
    DIVORCED = "divorced"
    WIDOWED = "widowed"
    SEPARATED = "separated"

# Base schema for Employee
class EmployeeBase(BaseModel):
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    gender: GenderEnum
    date_of_birth: date
    national_id: str
    passport_number: Optional[str] = None
    tax_id: str
    email: EmailStr
    personal_email: Optional[EmailStr] = None
    phone_number: str
    alternative_phone: Optional[str] = None
    physical_address: str
    postal_address: Optional[str] = None
    marital_status: MaritalStatusEnum
    nationality: str
    ethnicity: Optional[str] = None
    religion: Optional[str] = None
    blood_group: Optional[str] = None
    disability: Optional[str] = None
    profile_photo: Optional[str] = None
    
    # Employment information
    employee_number: str
    hire_date: date
    confirmation_date: Optional[date] = None
    contract_end_date: Optional[date] = None
    status: EmploymentStatusEnum = EmploymentStatusEnum.ACTIVE
    employment_type: str
    probation_period_months: Optional[int] = None
    notice_period_days: Optional[int] = None
    
    # Banking information
    bank_name: str
    bank_branch: str
    account_number: str
    
    # Foreign keys
    position_id: int
    supervisor_id: Optional[int] = None
    ministry_id: Optional[int] = None
    department_id: Optional[int] = None
    agency_id: Optional[int] = None
    county_id: Optional[int] = None
    sub_county_id: Optional[int] = None
    ward_id: Optional[int] = None

# Schema for creating an Employee
class EmployeeCreate(EmployeeBase):
    pass

# Schema for updating an Employee
class EmployeeUpdate(BaseModel):
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    personal_email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    alternative_phone: Optional[str] = None
    physical_address: Optional[str] = None
    postal_address: Optional[str] = None
    marital_status: Optional[MaritalStatusEnum] = None
    profile_photo: Optional[str] = None
    
    # Employment information
    confirmation_date: Optional[date] = None
    contract_end_date: Optional[date] = None
    status: Optional[EmploymentStatusEnum] = None
    employment_type: Optional[str] = None
    
    # Banking information
    bank_name: Optional[str] = None
    bank_branch: Optional[str] = None
    account_number: Optional[str] = None
    
    # Foreign keys
    position_id: Optional[int] = None
    supervisor_id: Optional[int] = None
    ministry_id: Optional[int] = None
    department_id: Optional[int] = None
    agency_id: Optional[int] = None
    county_id: Optional[int] = None
    sub_county_id: Optional[int] = None
    ward_id: Optional[int] = None

# Schema for Position (simplified for Employee relationships)
class Position(BaseModel):
    id: int
    title: str
    salary_grade: str
    job_level: int

    class Config:
        orm_mode = True

# Schema for PerformanceReview (simplified for Employee relationships)
class PerformanceReview(BaseModel):
    id: int
    review_date: date
    overall_rating: str
    status: str

    class Config:
        orm_mode = True

# Schema for Employee response
class Employee(BaseModel):
    id: int
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    email: EmailStr
    phone_number: str
    employee_number: str
    status: EmploymentStatusEnum
    position_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Schema for detailed Employee response
class EmployeeDetail(Employee):
    gender: GenderEnum
    date_of_birth: date
    national_id: str
    passport_number: Optional[str] = None
    tax_id: str
    personal_email: Optional[EmailStr] = None
    alternative_phone: Optional[str] = None
    physical_address: str
    postal_address: Optional[str] = None
    marital_status: MaritalStatusEnum
    nationality: str
    ethnicity: Optional[str] = None
    religion: Optional[str] = None
    blood_group: Optional[str] = None
    disability: Optional[str] = None
    profile_photo: Optional[str] = None
    
    # Employment information
    hire_date: date
    confirmation_date: Optional[date] = None
    contract_end_date: Optional[date] = None
    employment_type: str
    probation_period_months: Optional[int] = None
    notice_period_days: Optional[int] = None
    
    # Banking information
    bank_name: str
    bank_branch: str
    account_number: str
    
    # Foreign keys
    supervisor_id: Optional[int] = None
    ministry_id: Optional[int] = None
    department_id: Optional[int] = None
    agency_id: Optional[int] = None
    county_id: Optional[int] = None
    sub_county_id: Optional[int] = None
    ward_id: Optional[int] = None
    
    # Relationships
    position: Position
    performance_reviews: List[PerformanceReview] = []

    class Config:
        orm_mode = True

