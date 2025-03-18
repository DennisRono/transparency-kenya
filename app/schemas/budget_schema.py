from typing import Optional, List
from datetime import date, datetime
from pydantic import BaseModel, validator
from enum import Enum

# Enums
class BudgetTypeEnum(str, Enum):
    OPERATIONAL = "operational"
    CAPITAL = "capital"
    DEVELOPMENT = "development"
    RECURRENT = "recurrent"
    SPECIAL = "special"

class BudgetStatusEnum(str, Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    APPROVED = "approved"
    REJECTED = "rejected"
    REVISED = "revised"
    ACTIVE = "active"
    CLOSED = "closed"

class ExpenditureCategoryEnum(str, Enum):
    SALARIES = "salaries"
    OPERATIONS = "operations"
    MAINTENANCE = "maintenance"
    UTILITIES = "utilities"
    SUPPLIES = "supplies"
    EQUIPMENT = "equipment"
    TRAVEL = "travel"
    TRAINING = "training"
    CONSULTANCY = "consultancy"
    INFRASTRUCTURE = "infrastructure"
    OTHER = "other"

class ExpenditureStatusEnum(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    PAID = "paid"
    CANCELLED = "cancelled"

# Base schema for Budget
class BudgetBase(BaseModel):
    fiscal_year: str
    budget_type: BudgetTypeEnum
    amount: float
    description: Optional[str] = None
    start_date: date
    end_date: date
    status: BudgetStatusEnum = BudgetStatusEnum.DRAFT
    approved_amount: Optional[float] = None
    approval_date: Optional[date] = None
    approved_by: Optional[int] = None
    rejection_reason: Optional[str] = None
    revision_number: int = 1
    previous_budget_id: Optional[int] = None
    currency: str = "KES"
    
    # Foreign keys
    ministry_id: Optional[int] = None
    department_id: Optional[int] = None
    agency_id: Optional[int] = None
    county_id: Optional[int] = None
    sub_county_id: Optional[int] = None
    ward_id: Optional[int] = None
    project_id: Optional[int] = None
    program_id: Optional[int] = None

# Schema for creating a Budget
class BudgetCreate(BudgetBase):
    pass

# Schema for updating a Budget
class BudgetUpdate(BaseModel):
    amount: Optional[float] = None
    description: Optional[str] = None
    end_date: Optional[date] = None
    status: Optional[BudgetStatusEnum] = None
    approved_amount: Optional[float] = None
    approval_date: Optional[date] = None
    approved_by: Optional[int] = None
    rejection_reason: Optional[str] = None
    revision_number: Optional[int] = None
    currency: Optional[str] = None

# Base schema for Expenditure
class ExpenditureBase(BaseModel):
    amount: float
    date: date
    description: str
    receipt_number: Optional[str] = None
    category: ExpenditureCategoryEnum
    status: ExpenditureStatusEnum = ExpenditureStatusEnum.PENDING
    payment_method: str
    payment_reference: Optional[str] = None
    payment_date: Optional[date] = None
    vendor_name: Optional[str] = None
    vendor_id: Optional[int] = None
    invoice_number: Optional[str] = None
    invoice_date: Optional[date] = None
    tax_amount: Optional[float] = None
    currency: str = "KES"
    exchange_rate: Optional[float] = None
    requested_by: int
    approved_by: Optional[int] = None
    approval_date: Optional[date] = None
    rejection_reason: Optional[str] = None
    supporting_documents: Optional[str] = None
    
    # Foreign keys
    budget_id: int
    ministry_id: Optional[int] = None
    department_id: Optional[int] = None
    agency_id: Optional[int] = None
    county_id: Optional[int] = None
    sub_county_id: Optional[int] = None
    ward_id: Optional[int] = None
    project_id: Optional[int] = None
    program_id: Optional[int] = None

# Schema for creating an Expenditure
class ExpenditureCreate(ExpenditureBase):
    pass

# Schema for updating an Expenditure
class ExpenditureUpdate(BaseModel):
    amount: Optional[float] = None
    description: Optional[str] = None
    receipt_number: Optional[str] = None
    status: Optional[ExpenditureStatusEnum] = None
    payment_method: Optional[str] = None
    payment_reference: Optional[str] = None
    payment_date: Optional[date] = None
    vendor_name: Optional[str] = None
    vendor_id: Optional[int] = None
    invoice_number: Optional[str] = None
    invoice_date: Optional[date] = None
    tax_amount: Optional[float] = None
    approved_by: Optional[int] = None
    approval_date: Optional[date] = None
    rejection_reason: Optional[str] = None
    supporting_documents: Optional[str] = None

# Schema for Budget response
class Budget(BudgetBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Schema for Expenditure response
class Expenditure(ExpenditureBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Schema for detailed Budget response
class BudgetDetail(Budget):
    expenditures: List[Expenditure] = []

    class Config:
        orm_mode = True

