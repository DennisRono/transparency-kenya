from datetime import date, datetime, time
from enum import Enum
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import String, ForeignKey, Text, Date, Boolean, Enum as SQLEnum, Time, Integer, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base

if TYPE_CHECKING:
    from models.performance import PerformanceReview
    from models.finance import Salary
    from models.security import LoginAttempt

class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    PREFER_NOT_TO_SAY = "prefer_not_to_say"

class EmploymentStatus(str, Enum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    TERMINATED = "terminated"
    ON_LEAVE = "on_leave"
    PROBATION = "probation"
    RETIRED = "retired"
    RESIGNED = "resigned"
    DECEASED = "deceased"

class MaritalStatus(str, Enum):
    SINGLE = "single"
    MARRIED = "married"
    DIVORCED = "divorced"
    WIDOWED = "widowed"
    SEPARATED = "separated"

class EducationLevel(str, Enum):
    PRIMARY = "primary"
    SECONDARY = "secondary"
    CERTIFICATE = "certificate"
    DIPLOMA = "diploma"
    BACHELORS = "bachelors"
    MASTERS = "masters"
    DOCTORATE = "doctorate"
    POSTDOCTORATE = "postdoctorate"

class Employee(Base):
    """Represents an employee in the government system."""
    __tablename__ = "employees"
    
    # Personal information
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    middle_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    gender: Mapped[Gender] = mapped_column(SQLEnum(Gender), nullable=False)
    date_of_birth: Mapped[date] = mapped_column(Date, nullable=False)
    national_id: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    passport_number: Mapped[Optional[str]] = mapped_column(String(20), nullable=True, unique=True)
    tax_id: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    personal_email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    phone_number: Mapped[str] = mapped_column(String(20), nullable=False)
    alternative_phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    physical_address: Mapped[str] = mapped_column(Text, nullable=False)
    postal_address: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    marital_status: Mapped[MaritalStatus] = mapped_column(SQLEnum(MaritalStatus), nullable=False)
    nationality: Mapped[str] = mapped_column(String(100), nullable=False)
    ethnicity: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    religion: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    blood_group: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    disability: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    profile_photo: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Employment information
    employee_number: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    hire_date: Mapped[date] = mapped_column(Date, nullable=False)
    confirmation_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    contract_end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    status: Mapped[EmploymentStatus] = mapped_column(
        SQLEnum(EmploymentStatus), 
        nullable=False, 
        default=EmploymentStatus.ACTIVE
    )
    employment_type: Mapped[str] = mapped_column(String(50), nullable=False)  # Permanent, Contract, Casual, etc.
    probation_period_months: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    notice_period_days: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    termination_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    termination_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    resignation_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    resignation_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    retirement_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    years_of_service: Mapped[Optional[float]] = mapped_column(nullable=True)
    
    # Banking information
    bank_name: Mapped[str] = mapped_column(String(255), nullable=False)
    bank_branch: Mapped[str] = mapped_column(String(255), nullable=False)
    account_number: Mapped[str] = mapped_column(String(50), nullable=False)
    
    # Foreign keys
    position_id: Mapped[int] = mapped_column(ForeignKey("positions.id"), nullable=False)
    supervisor_id: Mapped[Optional[int]] = mapped_column(ForeignKey("employees.id"), nullable=True)
    
    # Optional foreign keys for organizational placement
    ministry_id: Mapped[Optional[int]] = mapped_column(ForeignKey("ministries.id"), nullable=True)
    department_id: Mapped[Optional[int]] = mapped_column(ForeignKey("departments.id"), nullable=True)
    agency_id: Mapped[Optional[int]] = mapped_column(ForeignKey("agencies.id"), nullable=True)
    county_id: Mapped[Optional[int]] = mapped_column(ForeignKey("counties.id"), nullable=True)
    sub_county_id: Mapped[Optional[int]] = mapped_column(ForeignKey("sub_counties.id"), nullable=True)
    ward_id: Mapped[Optional[int]] = mapped_column(ForeignKey("wards.id"), nullable=True)
    
    # Relationships
    position: Mapped["Position"] = relationship(back_populates="employees")
    supervisor: Mapped[Optional["Employee"]] = relationship("Employee", remote_side=[id], foreign_keys=[supervisor_id], backref="subordinates")
    employment_history: Mapped[List["EmploymentHistory"]] = relationship(back_populates="employee", cascade="all, delete-orphan")
    performance_reviews: Mapped[List["PerformanceReview"]] = relationship(back_populates="employee", cascade="all, delete-orphan")
    salaries: Mapped[List["Salary"]] = relationship(back_populates="employee", cascade="all, delete-orphan")
    user_account: Mapped[Optional["UserAccount"]] = relationship(back_populates="employee", uselist=False, cascade="all, delete-orphan")
    qualifications: Mapped[List["Qualification"]] = relationship(back_populates="employee", cascade="all, delete-orphan")
    education: Mapped[List["Education"]] = relationship(back_populates="employee", cascade="all, delete-orphan")
    trainings: Mapped[List["Training"]] = relationship(back_populates="employee", cascade="all, delete-orphan")
    attendances: Mapped[List["Attendance"]] = relationship(back_populates="employee", cascade="all, delete-orphan")
    leaves: Mapped[List["Leave"]] = relationship(back_populates="employee", cascade="all, delete-orphan")
    disciplinary_actions: Mapped[List["DisciplinaryAction"]] = relationship(back_populates="employee", cascade="all, delete-orphan")
    benefits: Mapped[List["Benefit"]] = relationship(back_populates="employee", cascade="all, delete-orphan")
    allowances: Mapped[List["Allowance"]] = relationship(back_populates="employee", cascade="all, delete-orphan")
    emergency_contacts: Mapped[List["EmergencyContact"]] = relationship(back_populates="employee", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<Employee(name='{self.first_name} {self.last_name}', employee_number='{self.employee_number}')>"


class Position(Base):
    """Represents a job position in the government system."""
    __tablename__ = "positions"
    
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    code: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    salary_grade: Mapped[str] = mapped_column(String(50), nullable=False)
    min_salary: Mapped[float] = mapped_column(nullable=False)
    max_salary: Mapped[float] = mapped_column(nullable=False)
    job_level: Mapped[int] = mapped_column(Integer, nullable=False)  # Hierarchical level in the organization
    responsibilities: Mapped[str] = mapped_column(Text, nullable=False)
    qualifications_required: Mapped[str] = mapped_column(Text, nullable=False)
    experience_required: Mapped[str] = mapped_column(String(255), nullable=False)
    skills_required: Mapped[str] = mapped_column(Text, nullable=False)
    reporting_to: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)  # Position title this reports to
    is_management: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_executive: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    
    # Relationships
    employees: Mapped[List["Employee"]] = relationship(back_populates="position")
    
    def __repr__(self) -> str:
        return f"<Position(title='{self.title}', code='{self.code}')>"


class EmploymentHistory(Base):
    """Tracks an employee's position changes and organizational placements."""
    __tablename__ = "employment_history"
    
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    reason_for_change: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    change_type: Mapped[str] = mapped_column(String(50), nullable=False)  # Promotion, Transfer, Demotion, etc.
    previous_salary: Mapped[Optional[float]] = mapped_column(nullable=True)
    new_salary: Mapped[Optional[float]] = mapped_column(nullable=True)
    approved_by: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    approval_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    
    # Foreign keys
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    position_id: Mapped[int] = mapped_column(ForeignKey("positions.id"), nullable=False)
    previous_position_id: Mapped[Optional[int]] = mapped_column(ForeignKey("positions.id"), nullable=True)
    
    # Optional foreign keys for organizational placement
    ministry_id: Mapped[Optional[int]] = mapped_column(ForeignKey("ministries.id"), nullable=True)
    department_id: Mapped[Optional[int]] = mapped_column(ForeignKey("departments.id"), nullable=True)
    agency_id: Mapped[Optional[int]] = mapped_column(ForeignKey("agencies.id"), nullable=True)
    county_id: Mapped[Optional[int]] = mapped_column(ForeignKey("counties.id"), nullable=True)
    sub_county_id: Mapped[Optional[int]] = mapped_column(ForeignKey("sub_counties.id"), nullable=True)
    ward_id: Mapped[Optional[int]] = mapped_column(ForeignKey("wards.id"), nullable=True)
    
    # Relationships
    employee: Mapped["Employee"] = relationship(back_populates="employment_history")
    position: Mapped["Position"] = relationship(foreign_keys=[position_id])
    previous_position: Mapped[Optional["Position"]] = relationship(foreign_keys=[previous_position_id])
    
    def __repr__(self) -> str:
        return f"<EmploymentHistory(employee_id={self.employee_id}, start_date='{self.start_date}')>"


class Role(Base):
    """Represents a role with specific permissions in the system."""
    __tablename__ = "roles"
    
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    permissions: Mapped[str] = mapped_column(Text, nullable=False)  # JSON string of permissions
    is_system_role: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    
    # Relationships
    user_accounts: Mapped[List["UserAccount"]] = relationship(back_populates="role")
    
    def __repr__(self) -> str:
        return f"<Role(name='{self.name}')>"


class UserAccount(Base):
    """Represents a user account for system access."""
    __tablename__ = "users"
    
    username: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    is_locked: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    lock_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    password_reset_required: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    last_login: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    last_password_change: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    failed_login_attempts: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    activation_token: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    activation_token_expiry: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    
    # Foreign keys
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False, unique=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), nullable=False)
    
    # Relationships
    employee: Mapped["Employee"] = relationship(back_populates="user_account")
    role: Mapped["Role"] = relationship(back_populates="user_accounts")
    login_attempts: Mapped[List["LoginAttempt"]] = relationship(back_populates="user")
    
    def __repr__(self) -> str:
        return f"<UserAccount(username='{self.username}')>"


class QualificationType(str, Enum):
    ACADEMIC = "academic"
    PROFESSIONAL = "professional"
    TECHNICAL = "technical"
    CERTIFICATION = "certification"
    LICENSE = "license"
    AWARD = "award"


class Qualification(Base):
    """Represents a qualification held by an employee."""
    __tablename__ = "qualifications"
    
    qualification_type: Mapped[QualificationType] = mapped_column(SQLEnum(QualificationType), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    institution: Mapped[str] = mapped_column(String(255), nullable=False)
    date_obtained: Mapped[date] = mapped_column(Date, nullable=False)
    expiry_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    certificate_number: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    verification_status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    verified_by: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    verification_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    document_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Foreign keys
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    
    # Relationships
    employee: Mapped["Employee"] = relationship(back_populates="qualifications")
    
    def __repr__(self) -> str:
        return f"<Qualification(title='{self.title}', employee_id={self.employee_id})>"


class Education(Base):
    """Represents an employee's educational background."""
    __tablename__ = "education"
    
    institution: Mapped[str] = mapped_column(String(255), nullable=False)
    level: Mapped[EducationLevel] = mapped_column(SQLEnum(EducationLevel), nullable=False)
    field_of_study: Mapped[str] = mapped_column(String(255), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    is_completed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    grade: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    certificate_number: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    verification_status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    verified_by: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    verification_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    document_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Foreign keys
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    
    # Relationships
    employee: Mapped["Employee"] = relationship(back_populates="education")
    
    def __repr__(self) -> str:
        return f"<Education(institution='{self.institution}', level='{self.level}', employee_id={self.employee_id})>"


class TrainingStatus(str, Enum):
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    DEFERRED = "deferred"


class Training(Base):
    """Represents training undertaken by an employee."""
    __tablename__ = "trainings"
    
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    provider: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[TrainingStatus] = mapped_column(SQLEnum(TrainingStatus), nullable=False)
    cost: Mapped[Optional[float]] = mapped_column(nullable=True)
    funded_by: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    location: Mapped[str] = mapped_column(String(255), nullable=False)
    training_type: Mapped[str] = mapped_column(String(100), nullable=False)  # Workshop, Seminar, Course, etc.
    skills_acquired: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    certificate_issued: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    certificate_number: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    certificate_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Foreign keys
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    
    # Relationships
    employee: Mapped["Employee"] = relationship(back_populates="trainings")
    
    def __repr__(self) -> str:
        return f"<Training(title='{self.title}', employee_id={self.employee_id})>"


class Attendance(Base):
    """Represents an employee's daily attendance record."""
    __tablename__ = "attendances"
    
    current_date: Mapped[date] = mapped_column(Date, nullable=False)
    time_in: Mapped[Optional[time]] = mapped_column(Time, nullable=True)
    time_out: Mapped[Optional[time]] = mapped_column(Time, nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False)  # Present, Absent, Late, Half-day, etc.
    hours_worked: Mapped[Optional[float]] = mapped_column(nullable=True)
    overtime_hours: Mapped[Optional[float]] = mapped_column(nullable=True)
    remarks: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Foreign keys
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    
    # Relationships
    employee: Mapped["Employee"] = relationship(back_populates="attendances")
    
    def __repr__(self) -> str:
        return f"<Attendance(employee_id={self.employee_id}, date='{self.date}', status='{self.status}')>"


class LeaveType(str, Enum):
    ANNUAL = "annual"
    SICK = "sick"
    MATERNITY = "maternity"
    PATERNITY = "paternity"
    COMPASSIONATE = "compassionate"
    STUDY = "study"
    UNPAID = "unpaid"
    OTHER = "other"


class LeaveStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


class Leave(Base):
    """Represents an employee's leave request."""
    __tablename__ = "leaves"
    
    leave_type: Mapped[LeaveType] = mapped_column(SQLEnum(LeaveType), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    total_days: Mapped[int] = mapped_column(Integer, nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[LeaveStatus] = mapped_column(SQLEnum(LeaveStatus), nullable=False, default=LeaveStatus.PENDING)
    application_date: Mapped[date] = mapped_column(Date, nullable=False)
    approved_by: Mapped[Optional[int]] = mapped_column(ForeignKey("employees.id"), nullable=True)
    approval_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    rejection_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    cancellation_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    attachments: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON string of attachment URLs
    
    # Foreign keys
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    
    # Relationships
    employee: Mapped["Employee"] = relationship(back_populates="leaves", foreign_keys=[employee_id])
    approver: Mapped[Optional["Employee"]] = relationship(foreign_keys=[approved_by])
    
    def __repr__(self) -> str:
        return f"<Leave(employee_id={self.employee_id}, type='{self.leave_type}', status='{self.status}')>"


class DisciplinaryType(str, Enum):
    VERBAL_WARNING = "verbal_warning"
    WRITTEN_WARNING = "written_warning"
    FINAL_WARNING = "final_warning"
    SUSPENSION = "suspension"
    DEMOTION = "demotion"
    TERMINATION = "termination"


class DisciplinaryStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    APPEALED = "appealed"
    CLOSED = "closed"


class DisciplinaryAction(Base):
    """Represents a disciplinary action taken against an employee."""
    __tablename__ = "disciplinary_actions"
    
    action_type: Mapped[DisciplinaryType] = mapped_column(SQLEnum(DisciplinaryType), nullable=False)
    incident_date: Mapped[date] = mapped_column(Date, nullable=False)
    reported_date: Mapped[date] = mapped_column(Date, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    violation: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[DisciplinaryStatus] = mapped_column(SQLEnum(DisciplinaryStatus), nullable=False)
    action_taken: Mapped[str] = mapped_column(Text, nullable=False)
    action_date: Mapped[date] = mapped_column(Date, nullable=False)
    duration: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # In days, for suspension
    initiated_by: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    witnesses: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    employee_response: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    resolution: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    resolution_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    appeal_filed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    appeal_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    appeal_outcome: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    documents: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON string of document URLs
    
    # Foreign keys
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    
    # Relationships
    employee: Mapped["Employee"] = relationship(back_populates="disciplinary_actions", foreign_keys=[employee_id])
    initiator: Mapped["Employee"] = relationship(foreign_keys=[initiated_by])
    
    def __repr__(self) -> str:
        return f"<DisciplinaryAction(employee_id={self.employee_id}, type='{self.action_type}', status='{self.status}')>"


class BenefitType(str, Enum):
    HEALTH_INSURANCE = "health_insurance"
    LIFE_INSURANCE = "life_insurance"
    PENSION = "pension"
    HOUSING = "housing"
    TRANSPORT = "transport"
    EDUCATION = "education"
    OTHER = "other"


class Benefit(Base):
    """Represents benefits provided to an employee."""
    __tablename__ = "benefits"
    
    benefit_type: Mapped[BenefitType] = mapped_column(SQLEnum(BenefitType), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    provider: Mapped[str] = mapped_column(String(255), nullable=False)
    policy_number: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    cost: Mapped[float] = mapped_column(nullable=False)
    employer_contribution: Mapped[float] = mapped_column(nullable=False)
    employee_contribution: Mapped[float] = mapped_column(nullable=False)
    dependents_covered: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    coverage_details: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Foreign keys
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    
    # Relationships
    employee: Mapped["Employee"] = relationship(back_populates="benefits")
    
    def __repr__(self) -> str:
        return f"<Benefit(employee_id={self.employee_id}, type='{self.benefit_type}')>"


class AllowanceType(str, Enum):
    HOUSING = "housing"
    TRANSPORT = "transport"
    MEAL = "meal"
    TELEPHONE = "telephone"
    HARDSHIP = "hardship"
    ENTERTAINMENT = "entertainment"
    RESPONSIBILITY = "responsibility"
    OTHER = "other"


class Allowance(Base):
    """Represents allowances paid to an employee."""
    __tablename__ = "allowances"
    
    allowance_type: Mapped[AllowanceType] = mapped_column(SQLEnum(AllowanceType), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    amount: Mapped[float] = mapped_column(nullable=False)
    frequency: Mapped[str] = mapped_column(String(50), nullable=False)  # Monthly, Quarterly, Annual, One-time
    taxable: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    
    # Foreign keys
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    
    # Relationships
    employee: Mapped["Employee"] = relationship(back_populates="allowances")
    
    def __repr__(self) -> str:
        return f"<Allowance(employee_id={self.employee_id}, type='{self.allowance_type}', amount={self.amount})>"


class EmergencyContact(Base):
    """Represents an emergency contact for an employee."""
    __tablename__ = "emergency_contacts"
    
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    relationship: Mapped[str] = mapped_column(String(100), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(20), nullable=False)
    alternative_phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_primary: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    
    # Foreign keys
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    
    # Relationships
    employee: Mapped["Employee"] = relationship(back_populates="emergency_contacts")
    
    def __repr__(self) -> str:
        return f"<EmergencyContact(name='{self.name}', relationship='{self.relationship}', employee_id={self.employee_id})>"

