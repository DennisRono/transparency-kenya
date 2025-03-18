from typing import Optional, List
from datetime import datetime, date
from pydantic import BaseModel, EmailStr, HttpUrl, validator

# Base schema for Ministry
class MinistryBase(BaseModel):
    name: str
    code: str
    description: Optional[str] = None
    budget_allocation: float
    establishment_date: Optional[date] = None
    website: Optional[HttpUrl] = None
    physical_address: Optional[str] = None
    postal_address: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: bool = True

# Schema for creating a Ministry
class MinistryCreate(MinistryBase):
    pass

# Schema for updating a Ministry
class MinistryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    budget_allocation: Optional[float] = None
    website: Optional[HttpUrl] = None
    physical_address: Optional[str] = None
    postal_address: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None

# Schema for Department (simplified for Ministry relationships)
class Department(BaseModel):
    id: int
    name: str
    code: str
    description: Optional[str] = None
    budget_allocation: float
    is_active: bool

    class Config:
        orm_mode = True

# Schema for Ministry response
class Ministry(MinistryBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Schema for detailed Ministry response
class MinistryDetail(Ministry):
    departments: List[Department] = []

    class Config:
        orm_mode = True

