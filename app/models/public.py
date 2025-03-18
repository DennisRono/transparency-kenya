from datetime import date, datetime
from enum import Enum
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import String, ForeignKey, Text, Date, DateTime, Enum as SQLEnum, Integer, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base

if TYPE_CHECKING:
    from models.employee import Employee

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


class Complaint(Base):
    """Represents a complaint submitted by a citizen."""
    __tablename__ = "complaints"
    
    reference_number: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    subject: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    submission_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    status: Mapped[ComplaintStatus] = mapped_column(SQLEnum(ComplaintStatus), nullable=False, default=ComplaintStatus.SUBMITTED)
    priority: Mapped[ComplaintPriority] = mapped_column(SQLEnum(ComplaintPriority), nullable=False, default=ComplaintPriority.MEDIUM)
    complainant_name: Mapped[str] = mapped_column(String(255), nullable=False)
    complainant_contact: Mapped[str] = mapped_column(String(100), nullable=False)
    complainant_email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    complainant_id_number: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    anonymous: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    incident_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    assigned_to: Mapped[Optional[int]] = mapped_column(ForeignKey("employees.id"), nullable=True)
    assignment_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    resolution_details: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    resolution_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    rejection_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    escalation_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    escalated_to: Mapped[Optional[int]] = mapped_column(ForeignKey("employees.id"), nullable=True)
    escalation_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    feedback_requested: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    feedback_provided: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    satisfaction_rating: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # 1-5 scale
    attachments: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON string of attachment URLs
    
    # Optional foreign keys for organizational placement
    ministry_id: Mapped[Optional[int]] = mapped_column(ForeignKey("ministries.id"), nullable=True)
    department_id: Mapped[Optional[int]] = mapped_column(ForeignKey("departments.id"), nullable=True)
    agency_id: Mapped[Optional[int]] = mapped_column(ForeignKey("agencies.id"), nullable=True)
    county_id: Mapped[Optional[int]] = mapped_column(ForeignKey("counties.id"), nullable=True)
    sub_county_id: Mapped[Optional[int]] = mapped_column(ForeignKey("sub_counties.id"), nullable=True)
    ward_id: Mapped[Optional[int]] = mapped_column(ForeignKey("wards.id"), nullable=True)
    
    # Relationships
    assignee: Mapped[Optional["Employee"]] = relationship(foreign_keys=[assigned_to])
    escalated_officer: Mapped[Optional["Employee"]] = relationship(foreign_keys=[escalated_to])
    
    def __repr__(self) -> str:
        return f"<Complaint(reference_number='{self.reference_number}', status='{self.status}')>"


class FeedbackType(str, Enum):
    SUGGESTION = "suggestion"
    COMPLIMENT = "compliment"
    GENERAL = "general"
    SERVICE_QUALITY = "service_quality"
    WEBSITE = "website"
    OTHER = "other"


class Feedback(Base):
    """Represents feedback provided by a citizen."""
    __tablename__ = "feedback"
    
    reference_number: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    feedback_type: Mapped[FeedbackType] = mapped_column(SQLEnum(FeedbackType), nullable=False)
    subject: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    submission_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    provider_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    provider_contact: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    provider_email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    anonymous: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    service_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    service_location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    satisfaction_rating: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # 1-5 scale
    reviewed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    reviewed_by: Mapped[Optional[int]] = mapped_column(ForeignKey("employees.id"), nullable=True)
    review_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    response_required: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    response_provided: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    response_details: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    response_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    # Optional foreign keys for organizational placement
    ministry_id: Mapped[Optional[int]] = mapped_column(ForeignKey("ministries.id"), nullable=True)
    department_id: Mapped[Optional[int]] = mapped_column(ForeignKey("departments.id"), nullable=True)
    agency_id: Mapped[Optional[int]] = mapped_column(ForeignKey("agencies.id"), nullable=True)
    county_id: Mapped[Optional[int]] = mapped_column(ForeignKey("counties.id"), nullable=True)
    sub_county_id: Mapped[Optional[int]] = mapped_column(ForeignKey("sub_counties.id"), nullable=True)
    ward_id: Mapped[Optional[int]] = mapped_column(ForeignKey("wards.id"), nullable=True)
    
    # Relationships
    reviewer: Mapped[Optional["Employee"]] = relationship(foreign_keys=[reviewed_by])
    
    def __repr__(self) -> str:
        return f"<Feedback(reference_number='{self.reference_number}', type='{self.feedback_type}')>"


class ParticipationType(str, Enum):
    PUBLIC_FORUM = "public_forum"
    TOWN_HALL = "town_hall"
    CONSULTATION = "consultation"
    SURVEY = "survey"
    FOCUS_GROUP = "focus_group"
    COMMITTEE = "committee"
    ONLINE_ENGAGEMENT = "online_engagement"
    OTHER = "other"


class PublicParticipation(Base):
    """Represents a public participation event or activity."""
    __tablename__ = "public_participation"
    
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    participation_type: Mapped[ParticipationType] = mapped_column(SQLEnum(ParticipationType), nullable=False)
    start_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    location: Mapped[str] = mapped_column(String(255), nullable=False)
    target_audience: Mapped[str] = mapped_column(Text, nullable=False)
    expected_participants: Mapped[int] = mapped_column(Integer, nullable=False)
    actual_participants: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    objectives: Mapped[str] = mapped_column(Text, nullable=False)
    agenda: Mapped[str] = mapped_column(Text, nullable=False)
    outcome: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    feedback_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    action_items: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    budget_allocation: Mapped[float] = mapped_column(nullable=False)
    actual_expenditure: Mapped[Optional[float]] = mapped_column(nullable=True)
    organized_by: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    facilitator: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    documentation: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON string of document URLs
    published: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    publication_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    # Optional foreign keys for organizational placement
    ministry_id: Mapped[Optional[int]] = mapped_column(ForeignKey("ministries.id"), nullable=True)
    department_id: Mapped[Optional[int]] = mapped_column(ForeignKey("departments.id"), nullable=True)
    agency_id: Mapped[Optional[int]] = mapped_column(ForeignKey("agencies.id"), nullable=True)
    county_id: Mapped[Optional[int]] = mapped_column(ForeignKey("counties.id"), nullable=True)
    sub_county_id: Mapped[Optional[int]] = mapped_column(ForeignKey("sub_counties.id"), nullable=True)
    ward_id: Mapped[Optional[int]] = mapped_column(ForeignKey("wards.id"), nullable=True)
    project_id: Mapped[Optional[int]] = mapped_column(ForeignKey("projects.id"), nullable=True)
    program_id: Mapped[Optional[int]] = mapped_column(ForeignKey("programs.id"), nullable=True)
    
    # Relationships
    organizer: Mapped["Employee"] = relationship(foreign_keys=[organized_by])
    public_meetings: Mapped[List["PublicMeeting"]] = relationship(back_populates="participation_event", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<PublicParticipation(title='{self.title}', type='{self.participation_type}')>"


class InformationRequestStatus(str, Enum):
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    PARTIALLY_APPROVED = "partially_approved"
    REJECTED = "rejected"
    INFORMATION_PROVIDED = "information_provided"
    CLOSED = "closed"
    APPEALED = "appealed"


class InformationRequest(Base):
    """Represents a request for information from a citizen."""
    __tablename__ = "information_requests"
    
    reference_number: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    subject: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    submission_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    status: Mapped[InformationRequestStatus] = mapped_column(SQLEnum(InformationRequestStatus), nullable=False, default=InformationRequestStatus.SUBMITTED)
    requester_name: Mapped[str] = mapped_column(String(255), nullable=False)
    requester_contact: Mapped[str] = mapped_column(String(100), nullable=False)
    requester_email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    requester_id_number: Mapped[str] = mapped_column(String(50), nullable=False)
    purpose: Mapped[str] = mapped_column(Text, nullable=False)
    assigned_to: Mapped[Optional[int]] = mapped_column(ForeignKey("employees.id"), nullable=True)
    assignment_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    due_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    review_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    approval_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    approved_by: Mapped[Optional[int]] = mapped_column(ForeignKey("employees.id"), nullable=True)
    rejection_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    information_provided: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    provision_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    appeal_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    appeal_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    appeal_decision: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    appeal_decision_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    satisfaction_rating: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # 1-5 scale
    
    # Optional foreign keys for organizational placement
    ministry_id: Mapped[Optional[int]] = mapped_column(ForeignKey("ministries.id"), nullable=True)
    department_id: Mapped[Optional[int]] = mapped_column(ForeignKey("departments.id"), nullable=True)
    agency_id: Mapped[Optional[int]] = mapped_column(ForeignKey("agencies.id"), nullable=True)
    county_id: Mapped[Optional[int]] = mapped_column(ForeignKey("counties.id"), nullable=True)
    
    # Relationships
    assignee: Mapped[Optional["Employee"]] = relationship(foreign_keys=[assigned_to])
    approver: Mapped[Optional["Employee"]] = relationship(foreign_keys=[approved_by])
    
    def __repr__(self) -> str:
        return f"<InformationRequest(reference_number='{self.reference_number}', status='{self.status}')>"


class ServiceRating(Base):
    """Represents a rating for a government service."""
    __tablename__ = "service_ratings"
    
    service_name: Mapped[str] = mapped_column(String(255), nullable=False)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)  # 1-5 scale
    comments: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    submission_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    rater_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    rater_contact: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    rater_email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    anonymous: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    service_date: Mapped[date] = mapped_column(Date, nullable=False)
    service_location: Mapped[str] = mapped_column(String(255), nullable=False)
    wait_time_minutes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    staff_courtesy_rating: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # 1-5 scale
    process_efficiency_rating: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # 1-5 scale
    information_clarity_rating: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # 1-5 scale
    overall_satisfaction_rating: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # 1-5 scale
    reviewed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    reviewed_by: Mapped[Optional[int]] = mapped_column(ForeignKey("employees.id"), nullable=True)
    review_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    # Optional foreign keys for organizational placement
    ministry_id: Mapped[Optional[int]] = mapped_column(ForeignKey("ministries.id"), nullable=True)
    department_id: Mapped[Optional[int]] = mapped_column(ForeignKey("departments.id"), nullable=True)
    agency_id: Mapped[Optional[int]] = mapped_column(ForeignKey("agencies.id"), nullable=True)
    county_id: Mapped[Optional[int]] = mapped_column(ForeignKey("counties.id"), nullable=True)
    sub_county_id: Mapped[Optional[int]] = mapped_column(ForeignKey("sub_counties.id"), nullable=True)
    ward_id: Mapped[Optional[int]] = mapped_column(ForeignKey("wards.id"), nullable=True)
    
    # Relationships
    reviewer: Mapped[Optional["Employee"]] = relationship(foreign_keys=[reviewed_by])
    
    def __repr__(self) -> str:
        return f"<ServiceRating(service_name='{self.service_name}', rating={self.rating})>"


class CitizenSatisfactionSurvey(Base):
    """Represents a comprehensive citizen satisfaction survey."""
    __tablename__ = "citizen_satisfaction_surveys"
    
    survey_title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    target_population: Mapped[str] = mapped_column(Text, nullable=False)
    methodology: Mapped[str] = mapped_column(Text, nullable=False)
    sample_size: Mapped[int] = mapped_column(Integer, nullable=False)
    actual_respondents: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    questions: Mapped[str] = mapped_column(Text, nullable=False)  # JSON string of questions
    results_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    average_satisfaction_score: Mapped[Optional[float]] = mapped_column(nullable=True)  # 1-5 scale
    key_findings: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    recommendations: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    action_plan: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    published: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    publication_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    conducted_by: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    approved_by: Mapped[Optional[int]] = mapped_column(ForeignKey("employees.id"), nullable=True)
    
    # Optional foreign keys for organizational placement
    ministry_id: Mapped[Optional[int]] = mapped_column(ForeignKey("ministries.id"), nullable=True)
    department_id: Mapped[Optional[int]] = mapped_column(ForeignKey("departments.id"), nullable=True)
    agency_id: Mapped[Optional[int]] = mapped_column(ForeignKey("agencies.id"), nullable=True)
    county_id: Mapped[Optional[int]] = mapped_column(ForeignKey("counties.id"), nullable=True)
    
    # Relationships
    conductor: Mapped["Employee"] = relationship(foreign_keys=[conducted_by])
    approver: Mapped[Optional["Employee"]] = relationship(foreign_keys=[approved_by])
    
    def __repr__(self) -> str:
        return f"<CitizenSatisfactionSurvey(title='{self.survey_title}', respondents={self.actual_respondents})>"


class PublicMeeting(Base):
    """Represents a public meeting or forum."""
    __tablename__ = "public_meetings"
    
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    meeting_date: Mapped[date] = mapped_column(Date, nullable=False)
    start_time: Mapped[str] = mapped_column(String(20), nullable=False)  # Format: HH:MM
    end_time: Mapped[str] = mapped_column(String(20), nullable=False)  # Format: HH:MM
    venue: Mapped[str] = mapped_column(String(255), nullable=False)
    agenda: Mapped[str] = mapped_column(Text, nullable=False)
    target_audience: Mapped[str] = mapped_column(Text, nullable=False)
    expected_attendees: Mapped[int] = mapped_column(Integer, nullable=False)
    actual_attendees: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    minutes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    resolutions: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    action_items: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    chairperson: Mapped[str] = mapped_column(String(255), nullable=False)
    secretary: Mapped[str] = mapped_column(String(255), nullable=False)
    published: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    publication_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    
    # Foreign keys
    participation_id: Mapped[Optional[int]] = mapped_column(ForeignKey("public_participation.id"), nullable=True)
    organized_by: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    
    # Optional foreign keys for organizational placement
    ministry_id: Mapped[Optional[int]] = mapped_column(ForeignKey("ministries.id"), nullable=True)
    department_id: Mapped[Optional[int]] = mapped_column(ForeignKey("departments.id"), nullable=True)
    agency_id: Mapped[Optional[int]] = mapped_column(ForeignKey("agencies.id"), nullable=True)
    county_id: Mapped[Optional[int]] = mapped_column(ForeignKey("counties.id"), nullable=True)
    sub_county_id: Mapped[Optional[int]] = mapped_column(ForeignKey("sub_counties.id"), nullable=True)
    ward_id: Mapped[Optional[int]] = mapped_column(ForeignKey("wards.id"), nullable=True)
    
    # Relationships
    participation_event: Mapped[Optional["PublicParticipation"]] = relationship(back_populates="public_meetings")
    organizer: Mapped["Employee"] = relationship(foreign_keys=[organized_by])
    
    def __repr__(self) -> str:
        return f"<PublicMeeting(title='{self.title}', date='{self.date}')>"

