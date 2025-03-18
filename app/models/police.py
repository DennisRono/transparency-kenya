from datetime import date, datetime
from enum import Enum
from typing import Optional, List
from sqlalchemy import String, ForeignKey, Text, Date, DateTime, Enum as SQLEnum, Integer, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base

class PoliceRank(str, Enum):
    CONSTABLE = "constable"
    CORPORAL = "corporal"
    SERGEANT = "sergeant"
    INSPECTOR = "inspector"
    CHIEF_INSPECTOR = "chief_inspector"
    SUPERINTENDENT = "superintendent"
    SENIOR_SUPERINTENDENT = "senior_superintendent"
    COMMISSIONER = "commissioner"
    SENIOR_COMMISSIONER = "senior_commissioner"
    ASSISTANT_INSPECTOR_GENERAL = "assistant_inspector_general"
    DEPUTY_INSPECTOR_GENERAL = "deputy_inspector_general"
    INSPECTOR_GENERAL = "inspector_general"


class PoliceOfficer(Base):
    """Represents a police officer."""
    __tablename__ = "police_officers"
    
    officer_number: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    middle_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    rank: Mapped[PoliceRank] = mapped_column(SQLEnum(PoliceRank), nullable=False)
    date_of_birth: Mapped[date] = mapped_column(Date, nullable=False)
    hire_date: Mapped[date] = mapped_column(Date, nullable=False)
    badge_number: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, unique=True)
    precinct: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    
    # Relationships
    incidents: Mapped[List["IncidentReport"]] = relationship(back_populates="officer")
    complaints: Mapped[List["Complaint"]] = relationship(back_populates="officer")
    investigations: Mapped[List["Investigation"]] = relationship(back_populates="officer")
    disciplinary_actions: Mapped[List["DisciplinaryAction"]] = relationship(back_populates="officer")
    
    def __repr__(self) -> str:
        return f"<PoliceOfficer(name='{self.first_name} {self.last_name}', officer_number='{self.officer_number}')>"


class IncidentType(str, Enum):
    ARREST = "arrest"
    TRAFFIC_STOP = "traffic_stop"
    USE_OF_FORCE = "use_of_force"
    SEARCH = "search"
    SEIZURE = "seizure"
    INVESTIGATION = "investigation"
    OTHER = "other"


class IncidentReport(Base):
    """Represents a reported incident involving a police officer."""
    __tablename__ = "incident_reports"
    
    report_number: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    incident_type: Mapped[IncidentType] = mapped_column(SQLEnum(IncidentType), nullable=False)
    incident_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    location: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Text] = mapped_column(nullable=False)
    suspect_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    suspect_contact: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    suspect_id_number: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    witnesses: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON string of witnesses
    attachments: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON string of attachment URLs
    
    # Foreign keys
    officer_id: Mapped[int] = mapped_column(ForeignKey("police_officers.id"), nullable=False)
    
    # Relationships
    officer: Mapped["PoliceOfficer"] = relationship(back_populates="incidents")
    complaints: Mapped[List["Complaint"]] = relationship(back_populates="incident")
    
    def __repr__(self) -> str:
        return f"<IncidentReport(report_number='{self.report_number}', type='{self.incident_type}')>"


class ComplaintStatus(str, Enum):
    SUBMITTED = "submitted"
    UNDER_INVESTIGATION = "under_investigation"
    RESOLVED = "resolved"
    DISMISSED = "dismissed"
    FORWARDED = "forwarded"


class Complaint(Base):
    """Represents a complaint against a police officer."""
    __tablename__ = "police_complaints"
    
    complaint_number: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    complaint_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    complainant_name: Mapped[str] = mapped_column(String(255), nullable=False)
    complainant_contact: Mapped[str] = mapped_column(String(100), nullable=False)
    complainant_email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    complainant_id_number: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    description: Mapped[Text] = mapped_column(nullable=False)
    status: Mapped[ComplaintStatus] = mapped_column(SQLEnum(ComplaintStatus), nullable=False, default=ComplaintStatus.SUBMITTED)
    allegation: Mapped[str] = mapped_column(Text, nullable=False)
    attachments: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON string of attachment URLs
    
    # Foreign keys
    officer_id: Mapped[int] = mapped_column(ForeignKey("police_officers.id"), nullable=False)
    incident_id: Mapped[Optional[int]] = mapped_column(ForeignKey("incident_reports.id"), nullable=True)
    
    # Relationships
    officer: Mapped["PoliceOfficer"] = relationship(back_populates="complaints")
    incident: Mapped[Optional["IncidentReport"]] = relationship(back_populates="complaints")
    investigation: Mapped[Optional["Investigation"]] = relationship(back_populates="complaint", uselist=False)
    
    def __repr__(self) -> str:
        return f"<Complaint(complaint_number='{self.complaint_number}', status='{self.status}')>"


class InvestigationStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CLOSED = "closed"


class Investigation(Base):
    """Represents an investigation into a complaint."""
    __tablename__ = "police_investigations"
    
    investigation_number: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    start_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    investigator_name: Mapped[str] = mapped_column(String(255), nullable=False)
    investigator_contact: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[InvestigationStatus] = mapped_column(SQLEnum(InvestigationStatus), nullable=False, default=InvestigationStatus.OPEN)
    findings: Mapped[Optional[Text]] = mapped_column(nullable=True)
    recommendations: Mapped[Optional[Text]] = mapped_column(nullable=True)
    evidence: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON string of evidence URLs
    
    # Foreign keys
    officer_id: Mapped[int] = mapped_column(ForeignKey("police_officers.id"), nullable=False)
    complaint_id: Mapped[int] = mapped_column(ForeignKey("police_complaints.id"), nullable=False, unique=True)
    
    # Relationships
    officer: Mapped["PoliceOfficer"] = relationship(back_populates="investigations")
    complaint: Mapped["Complaint"] = relationship(back_populates="investigation")
    disciplinary_action: Mapped[Optional["DisciplinaryAction"]] = relationship(back_populates="investigation", uselist=False)
    
    def __repr__(self) -> str:
        return f"<Investigation(investigation_number='{self.investigation_number}', status='{self.status}')>"


class DisciplinaryActionType(str, Enum):
    WARNING = "warning"
    SUSPENSION = "suspension"
    DEMOTION = "demotion"
    TERMINATION = "termination"
    OTHER = "other"


class DisciplinaryAction(Base):
    """Represents a disciplinary action taken against a police officer."""
    __tablename__ = "disciplinary_actions"
    
    action_number: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    action_type: Mapped[DisciplinaryActionType] = mapped_column(SQLEnum(DisciplinaryActionType), nullable=False)
    action_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    description: Mapped[Text] = mapped_column(nullable=False)
    sanctions: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    appeal_filed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    appeal_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    appeal_outcome: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Foreign keys
    officer_id: Mapped[int] = mapped_column(ForeignKey("police_officers.id"), nullable=False)
    investigation_id: Mapped[int] = mapped_column(ForeignKey("police_investigations.id"), nullable=False, unique=True)
    
    # Relationships
    officer: Mapped["PoliceOfficer"] = relationship(back_populates="disciplinary_actions")
    investigation: Mapped["Investigation"] = relationship(back_populates="disciplinary_action")
    
    def __repr__(self) -> str:
        return f"<DisciplinaryAction(action_number='{self.action_number}', type='{self.action_type}')>"


class EvidenceType(str, Enum):
    VIDEO = "video"
    AUDIO = "audio"
    DOCUMENT = "document"
    PHOTO = "photo"
    TESTIMONY = "testimony"
    OTHER = "other"


class Evidence(Base):
    """Represents evidence collected during an investigation."""
    __tablename__ = "evidence"
    
    evidence_number: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    evidence_type: Mapped[EvidenceType] = mapped_column(SQLEnum(EvidenceType), nullable=False)
    description: Mapped[Text] = mapped_column(nullable=False)
    collection_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    custodian: Mapped[str] = mapped_column(String(255), nullable=False)
    location: Mapped[str] = mapped_column(String(255), nullable=False)
    url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Foreign keys
    investigation_id: Mapped[int] = mapped_column(ForeignKey("police_investigations.id"), nullable=False)
    
    # Relationships
    investigation: Mapped["Investigation"] = relationship()
    
    def __repr__(self) -> str:
        return f"<Evidence(evidence_number='{self.evidence_number}', type='{self.evidence_type}')>"
    