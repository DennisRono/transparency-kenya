from datetime import date, datetime
from enum import Enum
from typing import Optional, List
from sqlalchemy import String, ForeignKey, Text, Date, DateTime, Enum as SQLEnum, Integer, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

class OfficerRank(str, Enum):
    CONSTABLE = "constable"
    CORPORAL = "corporal"
    SERGEANT = "sergeant"
    INSPECTOR = "inspector"
    CHIEF_INSPECTOR = "chief_inspector"
    SUPERINTENDENT = "superintendent"
    SENIOR_SUPERINTENDENT = "senior_superintendent"
    ASSISTANT_COMMISSIONER = "assistant_commissioner"
    COMMISSIONER = "commissioner"
    DEPUTY_INSPECTOR_GENERAL = "deputy_inspector_general"
    INSPECTOR_GENERAL = "inspector_general"

class OfficerStatus(str, Enum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    ON_LEAVE = "on_leave"
    TRANSFERRED = "transferred"
    RETIRED = "retired"
    DISMISSED = "dismissed"
    DECEASED = "deceased"

class ComplaintStatus(str, Enum):
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    INVESTIGATING = "investigating"
    RESOLVED = "resolved"
    CLOSED = "closed"
    REJECTED = "rejected"
    ESCALATED = "escalated"

class ComplaintPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class InvestigationStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CLOSED = "closed"
    REOPENED = "reopened"

class IncidentType(str, Enum):
    THEFT = "theft"
    ASSAULT = "assault"
    ROBBERY = "robbery"
    BURGLARY = "burglary"
    FRAUD = "fraud"
    VANDALISM = "vandalism"
    DRUG_RELATED = "drug_related"
    TRAFFIC_ACCIDENT = "traffic_accident"
    DOMESTIC_VIOLENCE = "domestic_violence"
    HOMICIDE = "homicide"
    KIDNAPPING = "kidnapping"
    SEXUAL_ASSAULT = "sexual_assault"
    PUBLIC_DISTURBANCE = "public_disturbance"
    MISSING_PERSON = "missing_person"
    OTHER = "other"

class IncidentSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class IncidentStatus(str, Enum):
    REPORTED = "reported"
    UNDER_INVESTIGATION = "under_investigation"
    PENDING_REVIEW = "pending_review"
    CLOSED = "closed"
    REFERRED = "referred"
    REOPENED = "reopened"

class PoliceOfficer(Base):
    """Represents a police officer."""
    __tablename__ = "police_officers"
    
    service_number: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    rank: Mapped[str] = mapped_column(String(100), nullable=False)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    middle_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    gender: Mapped[str] = mapped_column(String(20), nullable=False)
    date_of_birth: Mapped[date] = mapped_column(Date, nullable=False)
    national_id: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(20), nullable=False)
    physical_address: Mapped[str] = mapped_column(Text, nullable=False)
    date_of_enlistment: Mapped[date] = mapped_column(Date, nullable=False)
    station_id: Mapped[Optional[int]] = mapped_column(ForeignKey("police_stations.id"), nullable=True)
    department: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    supervisor_id: Mapped[Optional[int]] = mapped_column(ForeignKey("police_officers.id"), nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active")
    badge_number: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    firearm_serial: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    last_promotion_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    
    # Relationships
    supervisor: Mapped[Optional["PoliceOfficer"]] = relationship("PoliceOfficer", remote_side=[id], foreign_keys=[supervisor_id], backref="subordinates")
    complaints: Mapped[List["PoliceComplaint"]] = relationship(back_populates="officer", foreign_keys="[PoliceComplaint.officer_id]")
    assigned_complaints: Mapped[List["PoliceComplaint"]] = relationship(back_populates="assigned_officer", foreign_keys="[PoliceComplaint.assigned_to]")
    investigations: Mapped[List["PoliceInvestigation"]] = relationship(back_populates="lead_investigator")
    disciplinary_actions: Mapped[List["PoliceDisciplinaryAction"]] = relationship(back_populates="officer")
    reported_incidents: Mapped[List["IncidentReport"]] = relationship("IncidentReport", foreign_keys="[IncidentReport.reporting_officer_id]", back_populates="reporting_officer")
    supervised_incidents: Mapped[List["IncidentReport"]] = relationship("IncidentReport", foreign_keys="[IncidentReport.supervisor_id]", back_populates="supervisor")
    
    def __repr__(self) -> str:
        return f"<PoliceOfficer(service_number='{self.service_number}', name='{self.first_name} {self.last_name}', rank='{self.rank}')>"

class PoliceComplaint(Base):
    """Represents a complaint against a police officer."""
    __tablename__ = "police_complaints"
    
    reference_number: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    subject: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    submission_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    incident_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    location: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[ComplaintStatus] = mapped_column(SQLEnum(ComplaintStatus), nullable=False, default=ComplaintStatus.SUBMITTED)
    priority: Mapped[ComplaintPriority] = mapped_column(SQLEnum(ComplaintPriority), nullable=False, default=ComplaintPriority.MEDIUM)
    
    # Complainant information
    complainant_name: Mapped[str] = mapped_column(String(255), nullable=False)
    complainant_contact: Mapped[str] = mapped_column(String(100), nullable=False)
    complainant_email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    complainant_id_number: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    anonymous: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    
    # Additional information
    witnesses: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    evidence_description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Processing information
    assigned_to: Mapped[Optional[int]] = mapped_column(ForeignKey("police_officers.id"), nullable=True)
    assignment_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    resolution_details: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    resolution_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    rejection_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    escalation_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Foreign keys
    officer_id: Mapped[Optional[int]] = mapped_column(ForeignKey("police_officers.id"), nullable=True)
    
    # Relationships
    officer: Mapped[Optional["PoliceOfficer"]] = relationship(back_populates="complaints", foreign_keys=[officer_id])
    assigned_officer: Mapped[Optional["PoliceOfficer"]] = relationship(back_populates="assigned_complaints", foreign_keys=[assigned_to])
    investigation: Mapped[Optional["PoliceInvestigation"]] = relationship(back_populates="complaint")
    
    def __repr__(self) -> str:
        return f"<PoliceComplaint(reference_number='{self.reference_number}', subject='{self.subject}', status='{self.status}')>"

class PoliceInvestigation(Base):
    """Represents an investigation into a police complaint."""
    __tablename__ = "police_investigations"
    
    case_number: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    start_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    status: Mapped[InvestigationStatus] = mapped_column(SQLEnum(InvestigationStatus), nullable=False, default=InvestigationStatus.OPEN)
    findings: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    recommendations: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    action_taken: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Foreign keys
    complaint_id: Mapped[int] = mapped_column(ForeignKey("police_complaints.id"), nullable=False)
    lead_investigator_id: Mapped[int] = mapped_column(ForeignKey("police_officers.id"), nullable=False)
    
    # Relationships
    complaint: Mapped["PoliceComplaint"] = relationship(back_populates="investigation")
    lead_investigator: Mapped["PoliceOfficer"] = relationship(back_populates="investigations")
    evidence_items: Mapped[List["Evidence"]] = relationship(back_populates="investigation")
    
    def __repr__(self) -> str:
        return f"<PoliceInvestigation(case_number='{self.case_number}', status='{self.status}')>"

class DisciplinaryActionType(str, Enum):
    VERBAL_WARNING = "verbal_warning"
    WRITTEN_WARNING = "written_warning"
    SUSPENSION = "suspension"
    DEMOTION = "demotion"
    DISMISSAL = "dismissal"
    TRANSFER = "transfer"
    OTHER = "other"

class DisciplinaryActionStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    APPEALED = "appealed"
    OVERTURNED = "overturned"

class PoliceDisciplinaryAction(Base):
    """Represents a disciplinary action against a police officer."""
    __tablename__ = "police_disciplinary_actions"
    
    action_number: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    action_type: Mapped[DisciplinaryActionType] = mapped_column(SQLEnum(DisciplinaryActionType), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    incident_date: Mapped[date] = mapped_column(Date, nullable=False)
    action_date: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[DisciplinaryActionStatus] = mapped_column(SQLEnum(DisciplinaryActionStatus), nullable=False)
    duration_days: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # For suspensions
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    imposed_by: Mapped[str] = mapped_column(String(255), nullable=False)
    appeal_filed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    appeal_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    appeal_outcome: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Foreign keys
    officer_id: Mapped[int] = mapped_column(ForeignKey("police_officers.id"), nullable=False)
    investigation_id: Mapped[Optional[int]] = mapped_column(ForeignKey("police_investigations.id"), nullable=True)
    
    # Relationships
    officer: Mapped["PoliceOfficer"] = relationship(back_populates="disciplinary_actions")
    
    def __repr__(self) -> str:
        return f"<PoliceDisciplinaryAction(action_number='{self.action_number}', type='{self.action_type}', status='{self.status}')>"

class EvidenceType(str, Enum):
    DOCUMENT = "document"
    PHOTO = "photo"
    VIDEO = "video"
    AUDIO = "audio"
    PHYSICAL = "physical"
    TESTIMONY = "testimony"
    OTHER = "other"

class Evidence(Base):
    """Represents evidence in a police investigation."""
    __tablename__ = "evidence"
    
    evidence_number: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    evidence_type: Mapped[EvidenceType] = mapped_column(SQLEnum(EvidenceType), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    collection_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    collection_location: Mapped[str] = mapped_column(String(255), nullable=False)
    collected_by: Mapped[str] = mapped_column(String(255), nullable=False)
    chain_of_custody: Mapped[str] = mapped_column(Text, nullable=False)  # JSON string of custody changes
    storage_location: Mapped[str] = mapped_column(String(255), nullable=False)
    file_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)  # For digital evidence
    
    # Foreign keys
    investigation_id: Mapped[int] = mapped_column(ForeignKey("police_investigations.id"), nullable=False)
    
    # Relationships
    investigation: Mapped["PoliceInvestigation"] = relationship(back_populates="evidence_items")
    
    def __repr__(self) -> str:
        return f"<Evidence(evidence_number='{self.evidence_number}', type='{self.evidence_type}')>"

class IncidentReport(Base):
    """Represents an incident report filed by a police officer."""
    __tablename__ = "incident_reports"
    
    report_number: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    incident_datetime: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    report_datetime: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    location: Mapped[str] = mapped_column(String(255), nullable=False)
    gps_coordinates: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    incident_type: Mapped[IncidentType] = mapped_column(SQLEnum(IncidentType), nullable=False)
    severity: Mapped[IncidentSeverity] = mapped_column(SQLEnum(IncidentSeverity), nullable=False)
    status: Mapped[IncidentStatus] = mapped_column(SQLEnum(IncidentStatus), nullable=False, default=IncidentStatus.REPORTED)
    
    # Involved parties
    victims: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON string of victim information
    suspects: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON string of suspect information
    witnesses: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON string of witness information
    
    # Additional information
    property_involved: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    estimated_damages: Mapped[Optional[float]] = mapped_column(nullable=True)
    weapons_involved: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    injuries: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Case management
    case_opened: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    case_number: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    follow_up_actions: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    follow_up_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    resolution_details: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    resolution_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    
    # Foreign keys
    reporting_officer_id: Mapped[int] = mapped_column(ForeignKey("police_officers.id"), nullable=False)
    supervisor_id: Mapped[Optional[int]] = mapped_column(ForeignKey("police_officers.id"), nullable=True)
    station_id: Mapped[int] = mapped_column(ForeignKey("police_stations.id"), nullable=False)
    
    # Relationships
    reporting_officer: Mapped["PoliceOfficer"] = relationship("PoliceOfficer", foreign_keys=[reporting_officer_id])
    supervisor: Mapped[Optional["PoliceOfficer"]] = relationship("PoliceOfficer", foreign_keys=[supervisor_id])
    
    def __repr__(self) -> str:
        return f"<IncidentReport(report_number='{self.report_number}', type='{self.incident_type}', status='{self.status}')>"

