from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, validator
from enum import Enum

# Enums
class CrimeTypeEnum(str, Enum):
    THEFT = "theft"
    ASSAULT = "assault"
    ROBBERY = "robbery"
    BURGLARY = "burglary"
    FRAUD = "fraud"
    VANDALISM = "vandalism"
    DRUG_RELATED = "drug_related"
    TRAFFIC_VIOLATION = "traffic_violation"
    DOMESTIC_VIOLENCE = "domestic_violence"
    HARASSMENT = "harassment"
    CORRUPTION = "corruption"
    KIDNAPPING = "kidnapping"
    MURDER = "murder"
    SEXUAL_ASSAULT = "sexual_assault"
    OTHER = "other"

class ReportStatusEnum(str, Enum):
    SUBMITTED = "submitted"
    RECEIVED = "received"
    UNDER_REVIEW = "under_review"
    INVESTIGATING = "investigating"
    RESOLVED = "resolved"
    CLOSED = "closed"
    REQUIRES_MORE_INFO = "requires_more_info"
    FORWARDED = "forwarded"

class ReportPriorityEnum(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    EMERGENCY = "emergency"

class MediaTypeEnum(str, Enum):
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    DOCUMENT = "document"
    OTHER = "other"

# Base schema for CrimeReport
class CrimeReportBase(BaseModel):
    crime_type: CrimeTypeEnum
    description: str
    incident_datetime: Optional[datetime] = None
    location_description: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    priority: ReportPriorityEnum = ReportPriorityEnum.MEDIUM
    
    # Reporter information
    reporter_name: Optional[str] = None
    reporter_contact: Optional[str] = None
    reporter_email: Optional[str] = None
    reporter_id_number: Optional[str] = None
    anonymous: bool = False
    
    # Additional information
    suspects_description: Optional[str] = None
    victims_information: Optional[str] = None
    emergency_services_needed: bool = False
    emergency_services_details: Optional[str] = None

# Schema for creating a CrimeReport
class CrimeReportCreate(CrimeReportBase):
    pass

# Schema for updating a CrimeReport
class CrimeReportUpdate(BaseModel):
    description: Optional[str] = None
    incident_datetime: Optional[datetime] = None
    location_description: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    priority: Optional[ReportPriorityEnum] = None
    status: Optional[ReportStatusEnum] = None
    suspects_description: Optional[str] = None
    victims_information: Optional[str] = None
    emergency_services_needed: Optional[bool] = None
    emergency_services_details: Optional[str] = None
    assigned_to: Optional[int] = None
    resolution_details: Optional[str] = None

# Base schema for MediaEvidence
class MediaEvidenceBase(BaseModel):
    media_type: MediaTypeEnum
    description: Optional[str] = None

# Schema for creating MediaEvidence
class MediaEvidenceCreate(MediaEvidenceBase):
    pass

# Base schema for WitnessStatement
class WitnessStatementBase(BaseModel):
    statement_text: str
    witness_name: Optional[str] = None
    witness_contact: Optional[str] = None
    witness_email: Optional[str] = None
    witness_id_number: Optional[str] = None
    anonymous: bool = False

# Schema for creating WitnessStatement
class WitnessStatementCreate(WitnessStatementBase):
    pass

# Base schema for StatusUpdate
class StatusUpdateBase(BaseModel):
    status: ReportStatusEnum
    notes: Optional[str] = None
    public_note: Optional[str] = None
    notify_reporter: bool = False

# Schema for creating StatusUpdate
class StatusUpdateCreate(StatusUpdateBase):
    updated_by: int

# Schema for CrimeReport response
class CrimeReport(BaseModel):
    id: int
    report_number: str
    crime_type: CrimeTypeEnum
    description: str
    report_datetime: datetime
    location_description: str
    status: ReportStatusEnum
    priority: ReportPriorityEnum
    anonymous: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Schema for MediaEvidence response
class MediaEvidence(BaseModel):
    id: int
    evidence_id: str
    media_type: MediaTypeEnum
    file_url: str
    file_name: str
    file_size_kb: int
    mime_type: str
    upload_datetime: datetime
    description: Optional[str] = None
    crime_report_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Schema for WitnessStatement response
class WitnessStatement(BaseModel):
    id: int
    statement_id: str
    statement_text: str
    statement_datetime: datetime
    witness_name: Optional[str] = None
    anonymous: bool
    crime_report_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Schema for ReportStatusUpdate response
class ReportStatusUpdate(BaseModel):
    id: int
    status: ReportStatusEnum
    update_datetime: datetime
    notes: Optional[str] = None
    public_note: Optional[str] = None
    notify_reporter: bool
    notification_sent: bool
    crime_report_id: int
    updated_by: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Schema for detailed CrimeReport response
class CrimeReportDetail(CrimeReport):
    incident_datetime: Optional[datetime] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    reporter_name: Optional[str] = None
    reporter_contact: Optional[str] = None
    reporter_email: Optional[str] = None
    suspects_description: Optional[str] = None
    victims_information: Optional[str] = None
    emergency_services_needed: bool
    emergency_services_details: Optional[str] = None
    assigned_to: Optional[int] = None
    assignment_datetime: Optional[datetime] = None
    response_time_minutes: Optional[int] = None
    resolution_details: Optional[str] = None
    resolution_datetime: Optional[datetime] = None
    media_evidence: List[MediaEvidence] = []
    witness_statements: List[WitnessStatement] = []
    status_updates: List[ReportStatusUpdate] = []

    class Config:
        orm_mode = True

