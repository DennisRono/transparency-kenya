from datetime import date, datetime, time
from enum import Enum
from typing import Optional, List, TYPE_CHECKING
import uuid
from sqlalchemy import String, ForeignKey, Text, Date, DateTime, Time, Enum as SQLEnum, Integer, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

if TYPE_CHECKING:
    from app.models.police import PoliceOfficer, PoliceStation

class CrimeType(str, Enum):
    THEFT = "theft"
    ASSAULT = "assault"
    ROBBERY = "robbery"
    BURGLARY = "burglary"
    FRAUD = "fraud"
    VANDALISM = "vandalism"
    DRUG_RELATED = "drug_related"
    TRAFFIC_OFFENSE = "traffic_offense"
    DOMESTIC_VIOLENCE = "domestic_violence"
    HOMICIDE = "homicide"
    KIDNAPPING = "kidnapping"
    SEXUAL_ASSAULT = "sexual_assault"
    CYBERCRIME = "cybercrime"
    TERRORISM = "terrorism"
    OTHER = "other"

class CrimeSeverity(str, Enum):
    MINOR = "minor"
    MODERATE = "moderate"
    SERIOUS = "serious"
    SEVERE = "severe"
    CRITICAL = "critical"

class CaseStatus(str, Enum):
    REPORTED = "reported"
    UNDER_INVESTIGATION = "under_investigation"
    SUSPECT_IDENTIFIED = "suspect_identified"
    SUSPECT_ARRESTED = "suspect_arrested"
    CHARGED = "charged"
    COURT_PROCEEDINGS = "court_proceedings"
    CLOSED = "closed"
    REOPENED = "reopened"
    UNSOLVED = "unsolved"

class CrimeReport(Base):
    """Represents a crime report filed by a citizen."""
    __tablename__ = "crime_reports"
    
    report_number: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    crime_type: Mapped[CrimeType] = mapped_column(SQLEnum(CrimeType), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    incident_date: Mapped[date] = mapped_column(Date, nullable=False)
    incident_time: Mapped[Optional[time]] = mapped_column(Time, nullable=True)
    report_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    location: Mapped[str] = mapped_column(String(255), nullable=False)
    gps_coordinates: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    severity: Mapped[CrimeSeverity] = mapped_column(SQLEnum(CrimeSeverity), nullable=False)
    
    # Victim information
    victim_name: Mapped[str] = mapped_column(String(255), nullable=False)
    victim_contact: Mapped[str] = mapped_column(String(100), nullable=False)
    victim_address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    victim_id_number: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    
    # Reporter information (if different from victim)
    reporter_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    reporter_contact: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    reporter_address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    reporter_id_number: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    anonymous_report: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    
    # Suspect information (if known)
    suspect_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    suspect_description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Additional information
    witnesses: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    evidence_description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    property_involved: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    estimated_loss: Mapped[Optional[float]] = mapped_column(nullable=True)
    
    # Case management
    case_opened: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    case_number: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    case_status: Mapped[CaseStatus] = mapped_column(SQLEnum(CaseStatus), nullable=False, default=CaseStatus.REPORTED)
    assigned_officer_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("police_officers.id"), nullable=True)
    station_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("police_stations.id"), nullable=False)
    
    # Relationships
    assigned_officer: Mapped[Optional["PoliceOfficer"]] = relationship("PoliceOfficer")
    station: Mapped["PoliceStation"] = relationship("PoliceStation")
    case: Mapped[Optional["CriminalCase"]] = relationship(back_populates="crime_report")
    
    def __repr__(self) -> str:
        return f"<CrimeReport(report_number='{self.report_number}', crime_type='{self.crime_type}', status='{self.case_status}')>"

class CriminalCase(Base):
    """Represents a criminal case opened based on a crime report."""
    __tablename__ = "criminal_cases"
    
    case_number: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    open_date: Mapped[date] = mapped_column(Date, nullable=False)
    close_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    status: Mapped[CaseStatus] = mapped_column(SQLEnum(CaseStatus), nullable=False)
    crime_type: Mapped[CrimeType] = mapped_column(SQLEnum(CrimeType), nullable=False)
    severity: Mapped[CrimeSeverity] = mapped_column(SQLEnum(CrimeSeverity), nullable=False)
    
    # Case details
    investigation_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    evidence_collected: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    witnesses_interviewed: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    suspects: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    arrests_made: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    charges_filed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    charges_description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    court_case_number: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    court_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    prosecutor: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    judge: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    verdict: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    sentence: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    closing_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Foreign keys
    crime_report_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("crime_reports.id"), nullable=False)
    lead_investigator_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("police_officers.id"), nullable=False)
    station_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("police_stations.id"), nullable=False)
    
    # Relationships
    crime_report: Mapped["CrimeReport"] = relationship(back_populates="case")
    lead_investigator: Mapped["PoliceOfficer"] = relationship("PoliceOfficer")
    station: Mapped["PoliceStation"] = relationship("PoliceStation")
    case_updates: Mapped[List["CaseUpdate"]] = relationship(back_populates="case", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<CriminalCase(case_number='{self.case_number}', status='{self.status}')>"

class CaseUpdate(Base):
    """Represents an update to a criminal case."""
    __tablename__ = "case_updates"
    
    update_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    update_type: Mapped[str] = mapped_column(String(100), nullable=False)  # Investigation, Evidence, Arrest, Court, etc.
    status_change: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    previous_status: Mapped[Optional[CaseStatus]] = mapped_column(SQLEnum(CaseStatus), nullable=True)
    new_status: Mapped[Optional[CaseStatus]] = mapped_column(SQLEnum(CaseStatus), nullable=True)
    
    # Foreign keys
    case_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("criminal_cases.id"), nullable=False)
    officer_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("police_officers.id"), nullable=False)
    
    # Relationships
    case: Mapped["CriminalCase"] = relationship(back_populates="case_updates")
    officer: Mapped["PoliceOfficer"] = relationship("PoliceOfficer")
    
    def __repr__(self) -> str:
        return f"<CaseUpdate(case_id={self.case_id}, update_date='{self.update_date}', title='{self.title}')>"

class MissingPerson(Base):
    """Represents a missing person report."""
    __tablename__ = "missing_persons"
    
    report_number: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    middle_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    gender: Mapped[str] = mapped_column(String(20), nullable=False)
    height: Mapped[Optional[float]] = mapped_column(nullable=True)  # In cm
    weight: Mapped[Optional[float]] = mapped_column(nullable=True)  # In kg
    eye_color: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    hair_color: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    distinguishing_features: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    last_seen_date: Mapped[date] = mapped_column(Date, nullable=False)
    last_seen_time: Mapped[Optional[time]] = mapped_column(Time, nullable=True)
    last_seen_location: Mapped[str] = mapped_column(String(255), nullable=False)
    last_seen_wearing: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    possible_destinations: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    medical_conditions: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    medications: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    circumstances: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Reporter information
    reporter_name: Mapped[str] = mapped_column(String(255), nullable=False)
    reporter_contact: Mapped[str] = mapped_column(String(100), nullable=False)
    reporter_relationship: Mapped[str] = mapped_column(String(100), nullable=False)
    reporter_address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    reporter_id_number: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    
    # Case management
    report_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)  # Missing, Found Safe, Found Deceased, etc.
    is_vulnerable: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)  # Child, elderly, disabled, etc.
    is_high_risk: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    photo_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    assigned_officer_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("police_officers.id"), nullable=True)
    station_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("police_stations.id"), nullable=False)
    
    # Relationships
    assigned_officer: Mapped[Optional["PoliceOfficer"]] = relationship("PoliceOfficer")
    station: Mapped["PoliceStation"] = relationship("PoliceStation")
    
    def __repr__(self) -> str:
        return f"<MissingPerson(report_number='{self.report_number}', name='{self.first_name} {self.last_name}', status='{self.status}')>"

class WantedPerson(Base):
    """Represents a wanted person alert."""
    __tablename__ = "wanted_persons"
    
    alert_number: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    middle_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    aliases: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    date_of_birth: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    gender: Mapped[str] = mapped_column(String(20), nullable=False)
    height: Mapped[Optional[float]] = mapped_column(nullable=True)  # In cm
    weight: Mapped[Optional[float]] = mapped_column(nullable=True)  # In kg
    eye_color: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    hair_color: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    distinguishing_features: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    nationality: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    last_known_location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Criminal information
    wanted_for: Mapped[str] = mapped_column(Text, nullable=False)
    crime_type: Mapped[CrimeType] = mapped_column(SQLEnum(CrimeType), nullable=False)
    severity: Mapped[CrimeSeverity] = mapped_column(SQLEnum(CrimeSeverity), nullable=False)
    caution_level: Mapped[str] = mapped_column(String(50), nullable=False)  # Low, Medium, High, Armed and Dangerous
    warrant_number: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    issuing_authority: Mapped[str] = mapped_column(String(255), nullable=False)
    issue_date: Mapped[date] = mapped_column(Date, nullable=False)
    expiry_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    
    # Alert management
    status: Mapped[str] = mapped_column(String(50), nullable=False)  # Active, Apprehended, Expired, Cancelled
    photo_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    reward_amount: Mapped[Optional[float]] = mapped_column(nullable=True)
    contact_information: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Foreign keys
    case_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("criminal_cases.id"), nullable=True)
    issuing_officer_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("police_officers.id"), nullable=False)
    station_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("police_stations.id"), nullable=False)
    
    # Relationships
    case: Mapped[Optional["CriminalCase"]] = relationship("CriminalCase")
    issuing_officer: Mapped["PoliceOfficer"] = relationship("PoliceOfficer")
    station: Mapped["PoliceStation"] = relationship("PoliceStation")
    
    def __repr__(self) -> str:
        return f"<WantedPerson(alert_number='{self.alert_number}', name='{self.first_name} {self.last_name}', status='{self.status}')>"