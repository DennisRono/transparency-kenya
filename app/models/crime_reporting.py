from datetime import datetime
from enum import Enum
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import String, ForeignKey, Text, DateTime, Enum as SQLEnum, Integer, Float, Boolean, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base

if TYPE_CHECKING:
    from models.police import PoliceOfficer
    from models.employee import Employee

class CrimeType(str, Enum):
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

class ReportStatus(str, Enum):
    SUBMITTED = "submitted"
    RECEIVED = "received"
    UNDER_REVIEW = "under_review"
    INVESTIGATING = "investigating"
    RESOLVED = "resolved"
    CLOSED = "closed"
    REQUIRES_MORE_INFO = "requires_more_info"
    FORWARDED = "forwarded"

class ReportPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    EMERGENCY = "emergency"

class MediaType(str, Enum):
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    DOCUMENT = "document"
    OTHER = "other"

class CrimeReport(Base):
    """Represents a real-time crime report submitted by a citizen."""
    __tablename__ = "crime_reports"
    
    report_number: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    crime_type: Mapped[CrimeType] = mapped_column(SQLEnum(CrimeType), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    report_datetime: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    incident_datetime: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    location_description: Mapped[str] = mapped_column(String(255), nullable=False)
    latitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    longitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    status: Mapped[ReportStatus] = mapped_column(SQLEnum(ReportStatus), nullable=False, default=ReportStatus.SUBMITTED)
    priority: Mapped[ReportPriority] = mapped_column(SQLEnum(ReportPriority), nullable=False, default=ReportPriority.MEDIUM)
    
    # Reporter information
    reporter_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    reporter_contact: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    reporter_email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    reporter_id_number: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    anonymous: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    
    # Additional information
    suspects_description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    victims_information: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    emergency_services_needed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    emergency_services_details: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Processing information
    assigned_to: Mapped[Optional[int]] = mapped_column(ForeignKey("police_officers.id"), nullable=True)
    assignment_datetime: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    response_time_minutes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    resolution_details: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    resolution_datetime: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    feedback_requested: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    feedback_provided: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Metadata
    ip_address: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    device_info: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    app_version: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    
    # Relationships
    media_evidence: Mapped[List["MediaEvidence"]] = relationship(back_populates="crime_report", cascade="all, delete-orphan")
    witness_statements: Mapped[List["WitnessStatement"]] = relationship(back_populates="crime_report", cascade="all, delete-orphan")
    status_updates: Mapped[List["ReportStatusUpdate"]] = relationship(back_populates="crime_report", cascade="all, delete-orphan")
    assigned_officer: Mapped[Optional["PoliceOfficer"]] = relationship(foreign_keys=[assigned_to])
    
    def __repr__(self) -> str:
        return f"<CrimeReport(report_number='{self.report_number}', type='{self.crime_type}', status='{self.status}')>"

class MediaEvidence(Base):
    """Represents media evidence submitted with a crime report."""
    __tablename__ = "media_evidence"
    
    evidence_id: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    media_type: Mapped[MediaType] = mapped_column(SQLEnum(MediaType), nullable=False)
    file_url: Mapped[str] = mapped_column(String(255), nullable=False)
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    file_size_kb: Mapped[int] = mapped_column(Integer, nullable=False)
    mime_type: Mapped[str] = mapped_column(String(100), nullable=False)
    upload_datetime: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Metadata for media
    duration_seconds: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # For video/audio
    width: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # For images/videos
    height: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # For images/videos
    latitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)  # Geotag
    longitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)  # Geotag
    timestamp: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)  # When the media was created
    
    # Verification
    verified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    verified_by: Mapped[Optional[int]] = mapped_column(ForeignKey("employees.id"), nullable=True)
    verification_datetime: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    verification_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Foreign keys
    crime_report_id: Mapped[int] = mapped_column(ForeignKey("crime_reports.id"), nullable=False)
    
    # Relationships
    crime_report: Mapped["CrimeReport"] = relationship(back_populates="media_evidence")
    verifier: Mapped[Optional["Employee"]] = relationship(foreign_keys=[verified_by])
    
    def __repr__(self) -> str:
        return f"<MediaEvidence(evidence_id='{self.evidence_id}', type='{self.media_type}')>"

class WitnessStatement(Base):
    """Represents a witness statement for a crime report."""
    __tablename__ = "witness_statements"
    
    statement_id: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    statement_text: Mapped[str] = mapped_column(Text, nullable=False)
    statement_datetime: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    
    # Witness information
    witness_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    witness_contact: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    witness_email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    witness_id_number: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    anonymous: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    
    # Verification
    verified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    verified_by: Mapped[Optional[int]] = mapped_column(ForeignKey("employees.id"), nullable=True)
    verification_datetime: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    verification_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Foreign keys
    crime_report_id: Mapped[int] = mapped_column(ForeignKey("crime_reports.id"), nullable=False)
    
    # Relationships
    crime_report: Mapped["CrimeReport"] = relationship(back_populates="witness_statements")
    verifier: Mapped[Optional["Employee"]] = relationship(foreign_keys=[verified_by])
    
    def __repr__(self) -> str:
        return f"<WitnessStatement(statement_id='{self.statement_id}', crime_report_id={self.crime_report_id})>"

class ReportStatusUpdate(Base):
    """Represents status updates for a crime report."""
    __tablename__ = "report_status_updates"
    
    status: Mapped[ReportStatus] = mapped_column(SQLEnum(ReportStatus), nullable=False)
    update_datetime: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    public_note: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # Note visible to the reporter
    notify_reporter: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    notification_sent: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    notification_datetime: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    # Foreign keys
    crime_report_id: Mapped[int] = mapped_column(ForeignKey("crime_reports.id"), nullable=False)
    updated_by: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    
    # Relationships
    crime_report: Mapped["CrimeReport"] = relationship(back_populates="status_updates")
    updater: Mapped["Employee"] = relationship(foreign_keys=[updated_by])
    
    def __repr__(self) -> str:
        return f"<ReportStatusUpdate(crime_report_id={self.crime_report_id}, status='{self.status}', datetime='{self.update_datetime}')>"

class EmergencyContact(Base):
    """Represents emergency contacts for the crime reporting system."""
    __tablename__ = "emergency_contacts"
    
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    service_type: Mapped[str] = mapped_column(String(100), nullable=False)  # Police, Ambulance, Fire, etc.
    phone_number: Mapped[str] = mapped_column(String(50), nullable=False)
    alternative_phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    address: Mapped[str] = mapped_column(Text, nullable=False)
    jurisdiction: Mapped[str] = mapped_column(String(255), nullable=False)
    operating_hours: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    
    # Optional foreign keys for organizational placement
    county_id: Mapped[Optional[int]] = mapped_column(ForeignKey("counties.id"), nullable=True)
    sub_county_id: Mapped[Optional[int]] = mapped_column(ForeignKey("sub_counties.id"), nullable=True)
    ward_id: Mapped[Optional[int]] = mapped_column(ForeignKey("wards.id"), nullable=True)
    
    def __repr__(self) -> str:
        return f"<EmergencyContact(name='{self.name}', service_type='{self.service_type}', phone='{self.phone_number}')>"

class SafetyAlert(Base):
    """Represents safety alerts sent to citizens in specific areas."""
    __tablename__ = "safety_alerts"
    
    alert_id: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    alert_type: Mapped[str] = mapped_column(String(100), nullable=False)  # Crime, Weather, Traffic, etc.
    severity: Mapped[str] = mapped_column(String(50), nullable=False)  # Low, Medium, High, Critical
    start_datetime: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_datetime: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    
    # Location information
    affected_area: Mapped[str] = mapped_column(Text, nullable=False)
    latitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    longitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    radius_km: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    
    # Foreign keys
    issued_by: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    
    # Optional foreign keys for organizational placement
    county_id: Mapped[Optional[int]] = mapped_column(ForeignKey("counties.id"), nullable=True)
    sub_county_id: Mapped[Optional[int]] = mapped_column(ForeignKey("sub_counties.id"), nullable=True)
    ward_id: Mapped[Optional[int]] = mapped_column(ForeignKey("wards.id"), nullable=True)
    
    # Relationships
    issuer: Mapped["Employee"] = relationship(foreign_keys=[issued_by])
    
    def __repr__(self) -> str:
        return f"<SafetyAlert(alert_id='{self.alert_id}', title='{self.title}', is_active={self.is_active})>"
