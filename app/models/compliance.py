from datetime import date, datetime
from enum import Enum
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import String, ForeignKey, Text, Date, DateTime, Enum as SQLEnum, Integer, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

if TYPE_CHECKING:
    from app.models.employee import Employee

class ComplianceStatus(str, Enum):
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    PARTIALLY_COMPLIANT = "partially_compliant"
    UNDER_REVIEW = "under_review"
    EXEMPTED = "exempted"
    NOT_APPLICABLE = "not_applicable"

class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class AuditStatus(str, Enum):
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    DEFERRED = "deferred"

class InvestigationStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CLOSED = "closed"
    REOPENED = "reopened"

class ComplianceRequirement(Base):
    """Represents a legal or regulatory compliance requirement."""
    __tablename__ = "compliance_requirements"
    
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    requirement_type: Mapped[str] = mapped_column(String(100), nullable=False)  # Legal, Regulatory, Policy, etc.
    source: Mapped[str] = mapped_column(String(255), nullable=False)  # Law, Regulation, Standard, etc.
    reference_number: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    effective_date: Mapped[date] = mapped_column(Date, nullable=False)
    expiry_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    compliance_criteria: Mapped[str] = mapped_column(Text, nullable=False)
    verification_method: Mapped[str] = mapped_column(Text, nullable=False)
    reporting_frequency: Mapped[str] = mapped_column(String(50), nullable=False)  # Monthly, Quarterly, Annually, etc.
    responsible_role: Mapped[str] = mapped_column(String(255), nullable=False)
    oversight_authority: Mapped[str] = mapped_column(String(255), nullable=False)
    penalties_for_non_compliance: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    risk_level: Mapped[RiskLevel] = mapped_column(SQLEnum(RiskLevel), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Relationships
    compliance_reports: Mapped[List["ComplianceReport"]] = relationship(back_populates="requirement", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<ComplianceRequirement(name='{self.name}', type='{self.requirement_type}')>"

class ComplianceReport(Base):
    """Represents a report on compliance status for a requirement."""
    __tablename__ = "compliance_reports"
    
    report_date: Mapped[date] = mapped_column(Date, nullable=False)
    reporting_period_start: Mapped[date] = mapped_column(Date, nullable=False)
    reporting_period_end: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[ComplianceStatus] = mapped_column(SQLEnum(ComplianceStatus), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    evidence: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    action_plan: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    action_plan_due_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    action_plan_status: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    next_review_date: Mapped[date] = mapped_column(Date, nullable=False)
    
    # Foreign keys
    requirement_id: Mapped[int] = mapped_column(ForeignKey("compliance_requirements.id"), nullable=False)
    prepared_by: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    approved_by: Mapped[Optional[int]] = mapped_column(ForeignKey("employees.id"), nullable=True)
    
    # Optional foreign keys for organizational placement
    ministry_id: Mapped[Optional[int]] = mapped_column(ForeignKey("ministries.id"), nullable=True)
    department_id: Mapped[Optional[int]] = mapped_column(ForeignKey("departments.id"), nullable=True)
    agency_id: Mapped[Optional[int]] = mapped_column(ForeignKey("agencies.id"), nullable=True)
    county_id: Mapped[Optional[int]] = mapped_column(ForeignKey("counties.id"), nullable=True)
    
    # Relationships
    requirement: Mapped["ComplianceRequirement"] = relationship(back_populates="compliance_reports")
    preparer: Mapped["Employee"] = relationship(foreign_keys=[prepared_by])
    approver: Mapped[Optional["Employee"]] = relationship(foreign_keys=[approved_by])
    
    def __repr__(self) -> str:
        return f"<ComplianceReport(requirement_id={self.requirement_id}, status='{self.status}', report_date='{self.report_date}')>"

class Audit(Base):
    """Represents a compliance audit."""
    __tablename__ = "compliance_audits"
    
    audit_number: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    audit_type: Mapped[str] = mapped_column(String(100), nullable=False)  # Internal, External, Regulatory, etc.
    status: Mapped[AuditStatus] = mapped_column(SQLEnum(AuditStatus), nullable=False)
    planned_start_date: Mapped[date] = mapped_column(Date, nullable=False)
    planned_end_date: Mapped[date] = mapped_column(Date, nullable=False)
    actual_start_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    actual_end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    scope: Mapped[str] = mapped_column(Text, nullable=False)
    methodology: Mapped[str] = mapped_column(Text, nullable=False)
    findings: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    recommendations: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    management_response: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    action_plan: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    follow_up_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    follow_up_findings: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    auditor: Mapped[str] = mapped_column(String(255), nullable=False)
    auditor_contact: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Foreign keys
    lead_auditor_id: Mapped[Optional[int]] = mapped_column(ForeignKey("employees.id"), nullable=True)
    
    # Optional foreign keys for organizational placement
    ministry_id: Mapped[Optional[int]] = mapped_column(ForeignKey("ministries.id"), nullable=True)
    department_id: Mapped[Optional[int]] = mapped_column(ForeignKey("departments.id"), nullable=True)
    agency_id: Mapped[Optional[int]] = mapped_column(ForeignKey("agencies.id"), nullable=True)
    county_id: Mapped[Optional[int]] = mapped_column(ForeignKey("counties.id"), nullable=True)
    
    # Relationships
    lead_auditor: Mapped[Optional["Employee"]] = relationship(foreign_keys=[lead_auditor_id])
    
    def __repr__(self) -> str:
        return f"<Audit(audit_number='{self.audit_number}', title='{self.title}', status='{self.status}')>"

class Investigation(Base):
    """Represents an investigation into compliance issues."""
    __tablename__ = "compliance_investigations"
    
    investigation_number: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    trigger: Mapped[str] = mapped_column(String(100), nullable=False)  # Complaint, Audit Finding, Whistleblower, etc.
    status: Mapped[InvestigationStatus] = mapped_column(SQLEnum(InvestigationStatus), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    scope: Mapped[str] = mapped_column(Text, nullable=False)
    methodology: Mapped[str] = mapped_column(Text, nullable=False)
    findings: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    recommendations: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    action_taken: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    confidentiality_level: Mapped[str] = mapped_column(String(50), nullable=False)  # Public, Confidential, Restricted, etc.
    
    # Foreign keys
    lead_investigator_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    
    # Optional foreign keys for organizational placement
    ministry_id: Mapped[Optional[int]] = mapped_column(ForeignKey("ministries.id"), nullable=True)
    department_id: Mapped[Optional[int]] = mapped_column(ForeignKey("departments.id"), nullable=True)
    agency_id: Mapped[Optional[int]] = mapped_column(ForeignKey("agencies.id"), nullable=True)
    county_id: Mapped[Optional[int]] = mapped_column(ForeignKey("counties.id"), nullable=True)
    
    # Relationships
    lead_investigator: Mapped["Employee"] = relationship(foreign_keys=[lead_investigator_id])
    
    def __repr__(self) -> str:
        return f"<Investigation(investigation_number='{self.investigation_number}', title='{self.title}', status='{self.status}')>"

class RiskAssessment(Base):
    """Represents a compliance risk assessment."""
    __tablename__ = "risk_assessments"
    
    assessment_number: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    assessment_date: Mapped[date] = mapped_column(Date, nullable=False)
    next_assessment_date: Mapped[date] = mapped_column(Date, nullable=False)
    methodology: Mapped[str] = mapped_column(Text, nullable=False)
    overall_risk_level: Mapped[RiskLevel] = mapped_column(SQLEnum(RiskLevel), nullable=False)
    key_findings: Mapped[str] = mapped_column(Text, nullable=False)
    recommendations: Mapped[str] = mapped_column(Text, nullable=False)
    action_plan: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Foreign keys
    assessor_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    approved_by: Mapped[Optional[int]] = mapped_column(ForeignKey("employees.id"), nullable=True)
    
    # Optional foreign keys for organizational placement
    ministry_id: Mapped[Optional[int]] = mapped_column(ForeignKey("ministries.id"), nullable=True)
    department_id: Mapped[Optional[int]] = mapped_column(ForeignKey("departments.id"), nullable=True)
    agency_id: Mapped[Optional[int]] = mapped_column(ForeignKey("agencies.id"), nullable=True)
    county_id: Mapped[Optional[int]] = mapped_column(ForeignKey("counties.id"), nullable=True)
    
    # Relationships
    assessor: Mapped["Employee"] = relationship(foreign_keys=[assessor_id])
    approver: Mapped[Optional["Employee"]] = relationship(foreign_keys=[approved_by])
    risk_registers: Mapped[List["RiskRegister"]] = relationship(back_populates="risk_assessment", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<RiskAssessment(assessment_number='{self.assessment_number}', title='{self.title}', risk_level='{self.overall_risk_level}')>"

class RiskRegister(Base):
    """Represents a register of identified compliance risks."""
    __tablename__ = "risk_registers"
    
    risk_id: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    risk_description: Mapped[str] = mapped_column(Text, nullable=False)
    risk_category: Mapped[str] = mapped_column(String(100), nullable=False)
    likelihood: Mapped[int] = mapped_column(Integer, nullable=False)  # 1-5 scale
    impact: Mapped[int] = mapped_column(Integer, nullable=False)  # 1-5 scale
    risk_level: Mapped[RiskLevel] = mapped_column(SQLEnum(RiskLevel), nullable=False)
    existing_controls: Mapped[str] = mapped_column(Text, nullable=False)
    control_effectiveness: Mapped[int] = mapped_column(Integer, nullable=False)  # 1-5 scale
    residual_risk_level: Mapped[RiskLevel] = mapped_column(SQLEnum(RiskLevel), nullable=False)
    risk_owner: Mapped[str] = mapped_column(String(255), nullable=False)
    mitigation_strategy: Mapped[str] = mapped_column(Text, nullable=False)
    action_plan: Mapped[str] = mapped_column(Text, nullable=False)
    due_date: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)  # Open, In Progress, Closed, etc.
    review_date: Mapped[date] = mapped_column(Date, nullable=False)
    
    # Foreign keys
    risk_assessment_id: Mapped[int] = mapped_column(ForeignKey("risk_assessments.id"), nullable=False)
    risk_owner_id: Mapped[Optional[int]] = mapped_column(ForeignKey("employees.id"), nullable=True)
    
    # Relationships
    risk_assessment: Mapped["RiskAssessment"] = relationship(back_populates="risk_registers")
    owner: Mapped[Optional["Employee"]] = relationship(foreign_keys=[risk_owner_id])
    
    def __repr__(self) -> str:
        return f"<RiskRegister(risk_id='{self.risk_id}', risk_level='{self.risk_level}', status='{self.status}')>"

class Policy(Base):
    """Represents an internal policy document."""
    __tablename__ = "policies"
    
    policy_number: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    policy_type: Mapped[str] = mapped_column(String(100), nullable=False)
    version: Mapped[str] = mapped_column(String(20), nullable=False)
    effective_date: Mapped[date] = mapped_column(Date, nullable=False)
    expiry_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    review_frequency: Mapped[str] = mapped_column(String(50), nullable=False)  # Annual, Biennial, etc.
    next_review_date: Mapped[date] = mapped_column(Date, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)  # Draft, Active, Superseded, etc.
    document_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Foreign keys
    author_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    approved_by: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    
    # Optional foreign keys for organizational placement
    ministry_id: Mapped[Optional[int]] = mapped_column(ForeignKey("ministries.id"), nullable=True)
    department_id: Mapped[Optional[int]] = mapped_column(ForeignKey("departments.id"), nullable=True)
    agency_id: Mapped[Optional[int]] = mapped_column(ForeignKey("agencies.id"), nullable=True)
    county_id: Mapped[Optional[int]] = mapped_column(ForeignKey("counties.id"), nullable=True)
    
    # Relationships
    author: Mapped["Employee"] = relationship(foreign_keys=[author_id])
    approver: Mapped["Employee"] = relationship(foreign_keys=[approved_by])
    
    def __repr__(self) -> str:
        return f"<Policy(policy_number='{self.policy_number}', title='{self.title}', status='{self.status}')>"

class Regulation(Base):
    """Represents an external regulation that affects the organization."""
    __tablename__ = "regulations"
    
    regulation_number: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    issuing_authority: Mapped[str] = mapped_column(String(255), nullable=False)
    regulation_type: Mapped[str] = mapped_column(String(100), nullable=False)
    effective_date: Mapped[date] = mapped_column(Date, nullable=False)
    expiry_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    applicable_sectors: Mapped[str] = mapped_column(Text, nullable=False)
    key_requirements: Mapped[str] = mapped_column(Text, nullable=False)
    penalties: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    compliance_deadline: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    compliance_status: Mapped[ComplianceStatus] = mapped_column(SQLEnum(ComplianceStatus), nullable=False)
    responsible_department: Mapped[str] = mapped_column(String(255), nullable=False)
    document_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Foreign keys
    responsible_person_id: Mapped[Optional[int]] = mapped_column(ForeignKey("employees.id"), nullable=True)
    
    # Optional foreign keys for organizational placement
    ministry_id: Mapped[Optional[int]] = mapped_column(ForeignKey("ministries.id"), nullable=True)
    department_id: Mapped[Optional[int]] = mapped_column(ForeignKey("departments.id"), nullable=True)
    agency_id: Mapped[Optional[int]] = mapped_column(ForeignKey("agencies.id"), nullable=True)
    county_id: Mapped[Optional[int]] = mapped_column(ForeignKey("counties.id"), nullable=True)
    
    # Relationships
    responsible_person: Mapped[Optional["Employee"]] = relationship(foreign_keys=[responsible_person_id])
    
    def __repr__(self) -> str:
        return f"<Regulation(regulation_number='{self.regulation_number}', title='{self.title}', status='{self.compliance_status}')>"
