from typing import Optional, List
from datetime import datetime
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

# Base schema for Complaint
class ComplaintBase(BaseModel):
    subject: str
    description: str
    priority: ComplaintPriorityEnum = ComplaintPriorityEnum.MEDIUM
    complainant_name: str
    complainant_contact: str
    complainant_email: Optional[EmailStr] = None
    complainant_id_number: Optional[str] = None
    anonymous: bool = False
    location: Optional[str] = None
    incident_date: Optional[datetime] = None

# Schema for creating a Complaint
class ComplaintCreate(ComplaintBase):
    pass

# Schema for updating a Complaint
class ComplaintUpdate(BaseModel):
    subject: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[ComplaintPriorityEnum] = None
    status: Optional[ComplaintStatusEnum] = None
    resolution_details: Optional[str] = None
    rejection_reason: Optional[str] = None

# Schema for assigning a Complaint
class ComplaintAssignment(BaseModel):
    assigned_to: int
    notes: Optional[str] = None

# Schema for Complaint response
class Complaint(BaseModel):
    id: int
    reference_number: str
    subject: str
    description: str
    submission_date: datetime
    status: ComplaintStatusEnum
    priority: ComplaintPriorityEnum
    complainant_name: str
    complainant_contact: str
    anonymous: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Schema for detailed Complaint response
class ComplaintDetail(Complaint):
    complainant_email: Optional[EmailStr] = None
    complainant_id_number: Optional[str] = None
    location: Optional[str] = None
    incident_date: Optional[datetime] = None
    assigned_to: Optional[int] = None
    assignment_date: Optional[datetime] = None
    resolution_details: Optional[str] = None
    resolution_date: Optional[datetime] = None
    rejection_reason: Optional[str] = None
    escalation_reason: Optional[str] = None
    escalated_to: Optional[int] = None

    class Config:
        orm_mode = True

