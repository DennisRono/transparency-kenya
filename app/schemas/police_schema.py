from typing import Optional, List
from datetime import date, datetime
from pydantic import BaseModel, EmailStr
from enum import Enum

# Enums
class ComplaintStatusEnum(str, Enum):
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    INVESTIGATING = "investigating"
    RESOLVED = "resolved"
    CLOSED = "closed"
    REJECTED = "rejected"
    ESCALATED = "escalated"

class ComplaintPriorityEnum(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class InvestigationStatusEnum(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CLOSED = "closed"
    REOPENED = "reopened"

# Base schema for PoliceOfficer
class PoliceOfficerBase(BaseModel):
    service_number: str
    rank: str
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    gender: str
    date_of_birth: date
    national_id: str
    email: EmailStr
    phone_number: str
    physical_address: str
    date_of_enlistment: date
    station_id: Optional[int] = None
    department: Optional[str] = None
    supervisor_id: Optional[int] = None
    status: str = "active"

# Schema for creating a PoliceOfficer
class PoliceOfficerCreate(PoliceOfficerBase):
    pass

# Schema for updating a PoliceOfficer
class PoliceOfficerUpdate(BaseModel):
    rank: Optional[str] = None
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    physical_address: Optional[str] = None
    station_id: Optional[int] = None
    department: Optional[str] = None
    supervisor_id: Optional[int] = None
    status: Optional[str] = None

# Base schema for PoliceComplaint
class PoliceComplaintBase(BaseModel):
    subject: str
    description: str
    incident_date: datetime
    location: str
    complainant_name: str
    complainant_contact: str
    complainant_email: Optional[EmailStr] = None
    complainant_id_number: Optional[str] = None
    anonymous: bool = False
    priority: ComplaintPriorityEnum = ComplaintPriorityEnum.MEDIUM
    officer_id: Optional[int] = None
    witnesses: Optional[str] = None

# Schema for creating a PoliceComplaint
class PoliceComplaintCreate(PoliceComplaintBase):
    pass

# Schema for updating a PoliceComplaint
class PoliceComplaintUpdate(BaseModel):
    subject: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[ComplaintPriorityEnum] = None
    status: Optional[ComplaintStatusEnum] = None
    assigned_to: Optional[int] = None
    resolution_details: Optional[str] = None
    rejection_reason: Optional[str] = None

# Schema for PoliceOfficer response
class PoliceOfficer(BaseModel):
    id: int
    service_number: str
    rank: str
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    email: EmailStr
    phone_number: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Schema for detailed PoliceOfficer response
class PoliceOfficerDetail(PoliceOfficer):
    gender: str
    date_of_birth: date
    national_id: str
    physical_address: str
    date_of_enlistment: date
    station_id: Optional[int] = None
    department: Optional[str] = None
    supervisor_id: Optional[int] = None

    class Config:
        orm_mode = True

# Schema for PoliceComplaint response
class PoliceComplaint(BaseModel):
    id: int
    reference_number: str
    subject: str
    description: str
    incident_date: datetime
    location: str
    status: ComplaintStatusEnum
    priority: ComplaintPriorityEnum
    complainant_name: str
    complainant_contact: str
    anonymous: bool
    officer_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Schema for detailed PoliceComplaint response
class PoliceComplaintDetail(PoliceComplaint):
    complainant_email: Optional[EmailStr] = None
    complainant_id_number: Optional[str] = None
    witnesses: Optional[str] = None
    assigned_to: Optional[int] = None
    assignment_date: Optional[datetime] = None
    resolution_details: Optional[str] = None
    resolution_date: Optional[datetime] = None
    rejection_reason: Optional[str] = None

    class Config:
        orm_mode = True

