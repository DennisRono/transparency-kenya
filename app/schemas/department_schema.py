from typing import Optional, List
from datetime import date, datetime
from pydantic import BaseModel, EmailStr, HttpUrl, validator

# Base schema for Department
class DepartmentBase(BaseModel):
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
    ministry_id: int

# Schema for creating a Department
class DepartmentCreate(DepartmentBase):
    pass

# Schema for updating a Department
class DepartmentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    budget_allocation: Optional[float] = None
    website: Optional[HttpUrl] = None
    physical_address: Optional[str] = None
    postal_address: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    ministry_id: Optional[int] = None

# Schema for Agency (simplified for Department relationships)
class Agency(BaseModel):
    id: int
    name: str
    code: str
    description: Optional[str] = None
    budget_allocation: float
    is_active: bool

    class Config:
        orm_mode = True

# Schema for Ministry (simplified for Department relationships)
class Ministry(BaseModel):
    id: int
    name: str
    code: str

    class Config:
        orm_mode = True

# Schema for Department response
class Department(DepartmentBase):
    id: int
    created_at: datetime
    updated_at: datetime
    ministry: Ministry

    class Config:
        orm_mode = True

# Schema for detailed Department response
class DepartmentDetail(Department):
    agencies: List[Agency] = []

    class Config:
        orm_mode = True

