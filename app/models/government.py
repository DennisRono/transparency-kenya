from datetime import date
from enum import Enum
from typing import Optional, List
import uuid
from sqlalchemy import String, ForeignKey, Text, Integer, Float, Date, Boolean, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

class Ministry(Base):
    """Represents a government ministry."""
    __tablename__ = "ministries"
    
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    code: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    budget_allocation: Mapped[float] = mapped_column(nullable=False, default=0.0)
    establishment_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    website: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    physical_address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    postal_address: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    
    # Relationships
    departments: Mapped[List["Department"]] = relationship(back_populates="ministry", cascade="all, delete-orphan")
    projects: Mapped[List["Project"]] = relationship(back_populates="ministry")
    programs: Mapped[List["Program"]] = relationship(back_populates="ministry")
    committees: Mapped[List["Committee"]] = relationship(back_populates="ministry")
    
    def __repr__(self) -> str:
        return f"<Ministry(name='{self.name}', code='{self.code}')>"


class Department(Base):
    """Represents a department within a ministry."""
    __tablename__ = "departments"
    
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    code: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    budget_allocation: Mapped[float] = mapped_column(nullable=False, default=0.0)
    establishment_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    website: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    physical_address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    postal_address: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    
    # Foreign keys
    ministry_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("ministries.id"), nullable=False)
    
    # Relationships
    ministry: Mapped["Ministry"] = relationship(back_populates="departments")
    agencies: Mapped[List["Agency"]] = relationship(back_populates="department", cascade="all, delete-orphan")
    projects: Mapped[List["Project"]] = relationship(back_populates="department")
    programs: Mapped[List["Program"]] = relationship(back_populates="department")
    
    def __repr__(self) -> str:
        return f"<Department(name='{self.name}', code='{self.code}')>"


class Agency(Base):
    """Represents an agency under a department."""
    __tablename__ = "agencies"
    
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    code: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    budget_allocation: Mapped[float] = mapped_column(nullable=False, default=0.0)
    establishment_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    website: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    physical_address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    postal_address: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    agency_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    regulatory_authority: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Foreign keys
    department_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("departments.id"), nullable=False)
    
    # Relationships
    department: Mapped["Department"] = relationship(back_populates="agencies")
    projects: Mapped[List["Project"]] = relationship(back_populates="agency")
    programs: Mapped[List["Program"]] = relationship(back_populates="agency")
    
    def __repr__(self) -> str:
        return f"<Agency(name='{self.name}', code='{self.code}')>"


class County(Base):
    """Represents a county in Kenya."""
    __tablename__ = "counties"
    
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    code: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    population: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    area_sq_km: Mapped[Optional[float]] = mapped_column(nullable=True)
    budget_allocation: Mapped[float] = mapped_column(nullable=False, default=0.0)
    establishment_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    website: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    headquarters: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    governor_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    deputy_governor_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    county_secretary: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    postal_address: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Relationships
    sub_counties: Mapped[List["SubCounty"]] = relationship(back_populates="county", cascade="all, delete-orphan")
    projects: Mapped[List["Project"]] = relationship(back_populates="county")
    programs: Mapped[List["Program"]] = relationship(back_populates="county")
    
    def __repr__(self) -> str:
        return f"<County(name='{self.name}', code='{self.code}')>"


class SubCounty(Base):
    """Represents a sub-county within a county."""
    __tablename__ = "sub_counties"
    
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    code: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    population: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    area_sq_km: Mapped[Optional[float]] = mapped_column(nullable=True)
    budget_allocation: Mapped[float] = mapped_column(nullable=False, default=0.0)
    headquarters: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    sub_county_administrator: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    postal_address: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Foreign keys
    county_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("counties.id"), nullable=False)
    
    # Relationships
    county: Mapped["County"] = relationship(back_populates="sub_counties")
    wards: Mapped[List["Ward"]] = relationship(back_populates="sub_county", cascade="all, delete-orphan")
    projects: Mapped[List["Project"]] = relationship(back_populates="sub_county")
    
    def __repr__(self) -> str:
        return f"<SubCounty(name='{self.name}', code='{self.code}')>"


class Ward(Base):
    """Represents a ward within a sub-county."""
    __tablename__ = "wards"
    
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    code: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    population: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    area_sq_km: Mapped[Optional[float]] = mapped_column(nullable=True)
    budget_allocation: Mapped[float] = mapped_column(nullable=False, default=0.0)
    ward_administrator: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    postal_address: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Foreign keys
    sub_county_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("sub_counties.id"), nullable=False)
    
    # Relationships
    sub_county: Mapped["SubCounty"] = relationship(back_populates="wards")
    projects: Mapped[List["Project"]] = relationship(back_populates="ward")
    
    def __repr__(self) -> str:
        return f"<Ward(name='{self.name}', code='{self.code}')>"


class ProjectStatus(str, Enum):
    PROPOSED = "proposed"
    APPROVED = "approved"
    IN_PROGRESS = "in_progress"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Project(Base):
    """Represents a government project."""
    __tablename__ = "projects"
    
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    code: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    objectives: Mapped[str] = mapped_column(Text, nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    planned_end_date: Mapped[date] = mapped_column(Date, nullable=False)
    actual_end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    status: Mapped[ProjectStatus] = mapped_column(SQLEnum(ProjectStatus), nullable=False, default=ProjectStatus.PROPOSED)
    budget_allocation: Mapped[float] = mapped_column(nullable=False)
    actual_cost: Mapped[Optional[float]] = mapped_column(nullable=True)
    funding_source: Mapped[str] = mapped_column(String(255), nullable=False)
    beneficiaries: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    expected_outcomes: Mapped[str] = mapped_column(Text, nullable=False)
    actual_outcomes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    challenges: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    lessons_learned: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Foreign keys - optional based on which level the project belongs to
    ministry_id: Mapped[Optional[int]] = mapped_column(ForeignKey("ministries.id"), nullable=True)
    department_id: Mapped[Optional[int]] = mapped_column(ForeignKey("departments.id"), nullable=True)
    agency_id: Mapped[Optional[int]] = mapped_column(ForeignKey("agencies.id"), nullable=True)
    county_id: Mapped[Optional[int]] = mapped_column(ForeignKey("counties.id"), nullable=True)
    sub_county_id: Mapped[Optional[int]] = mapped_column(ForeignKey("sub_counties.id"), nullable=True)
    ward_id: Mapped[Optional[int]] = mapped_column(ForeignKey("wards.id"), nullable=True)
    
    # Relationships
    ministry: Mapped[Optional["Ministry"]] = relationship(back_populates="projects")
    department: Mapped[Optional["Department"]] = relationship(back_populates="projects")
    agency: Mapped[Optional["Agency"]] = relationship(back_populates="projects")
    county: Mapped[Optional["County"]] = relationship(back_populates="projects")
    sub_county: Mapped[Optional["SubCounty"]] = relationship(back_populates="projects")
    ward: Mapped[Optional["Ward"]] = relationship(back_populates="projects")
    
    def __repr__(self) -> str:
        return f"<Project(name='{self.name}', code='{self.code}', status='{self.status}')>"


class ProgramStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PLANNED = "planned"
    COMPLETED = "completed"


class Program(Base):
    """Represents a government program (collection of related projects or initiatives)."""
    __tablename__ = "programs"
    
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    code: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    objectives: Mapped[str] = mapped_column(Text, nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    status: Mapped[ProgramStatus] = mapped_column(SQLEnum(ProgramStatus), nullable=False, default=ProgramStatus.PLANNED)
    budget_allocation: Mapped[float] = mapped_column(nullable=False)
    funding_source: Mapped[str] = mapped_column(String(255), nullable=False)
    target_beneficiaries: Mapped[str] = mapped_column(Text, nullable=False)
    key_performance_indicators: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Foreign keys - optional based on which level the program belongs to
    ministry_id: Mapped[Optional[int]] = mapped_column(ForeignKey("ministries.id"), nullable=True)
    department_id: Mapped[Optional[int]] = mapped_column(ForeignKey("departments.id"), nullable=True)
    agency_id: Mapped[Optional[int]] = mapped_column(ForeignKey("agencies.id"), nullable=True)
    county_id: Mapped[Optional[int]] = mapped_column(ForeignKey("counties.id"), nullable=True)
    
    # Relationships
    ministry: Mapped[Optional["Ministry"]] = relationship(back_populates="programs")
    department: Mapped[Optional["Department"]] = relationship(back_populates="programs")
    agency: Mapped[Optional["Agency"]] = relationship(back_populates="programs")
    county: Mapped[Optional["County"]] = relationship(back_populates="programs")
    
    def __repr__(self) -> str:
        return f"<Program(name='{self.name}', code='{self.code}', status='{self.status}')>"


class CommitteeType(str, Enum):
    STANDING = "standing"
    AD_HOC = "ad_hoc"
    SPECIAL = "special"
    OVERSIGHT = "oversight"
    ADVISORY = "advisory"


class Committee(Base):
    """Represents a committee or task force."""
    __tablename__ = "committees"
    
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    code: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    committee_type: Mapped[CommitteeType] = mapped_column(SQLEnum(CommitteeType), nullable=False)
    formation_date: Mapped[date] = mapped_column(Date, nullable=False)
    dissolution_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    terms_of_reference: Mapped[str] = mapped_column(Text, nullable=False)
    chairperson_name: Mapped[str] = mapped_column(String(255), nullable=False)
    secretary_name: Mapped[str] = mapped_column(String(255), nullable=False)
    budget_allocation: Mapped[Optional[float]] = mapped_column(nullable=True)
    meeting_frequency: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    # Foreign keys - optional based on which level the committee belongs to
    ministry_id: Mapped[Optional[int]] = mapped_column(ForeignKey("ministries.id"), nullable=True)
    
    # Relationships
    ministry: Mapped[Optional["Ministry"]] = relationship(back_populates="committees")
    task_forces: Mapped[List["TaskForce"]] = relationship(back_populates="committee")
    
    def __repr__(self) -> str:
        return f"<Committee(name='{self.name}', type='{self.committee_type}')>"


class TaskForce(Base):
    """Represents a task force or working group."""
    __tablename__ = "task_forces"
    
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    code: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    formation_date: Mapped[date] = mapped_column(Date, nullable=False)
    dissolution_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    objectives: Mapped[str] = mapped_column(Text, nullable=False)
    deliverables: Mapped[str] = mapped_column(Text, nullable=False)
    chairperson_name: Mapped[str] = mapped_column(String(255), nullable=False)
    secretary_name: Mapped[str] = mapped_column(String(255), nullable=False)
    budget_allocation: Mapped[Optional[float]] = mapped_column(nullable=True)
    
    # Foreign keys
    committee_id: Mapped[Optional[int]] = mapped_column(ForeignKey("committees.id"), nullable=True)
    
    # Relationships
    committee: Mapped[Optional["Committee"]] = relationship(back_populates="task_forces")
    
    def __repr__(self) -> str:
        return f"<TaskForce(name='{self.name}')>"


class AssetCondition(str, Enum):
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    UNUSABLE = "unusable"


class PublicAsset(Base):
    """Represents a public asset owned by the government."""
    __tablename__ = "public_assets"
    
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    asset_number: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    acquisition_date: Mapped[date] = mapped_column(Date, nullable=False)
    acquisition_cost: Mapped[float] = mapped_column(nullable=False)
    current_value: Mapped[float] = mapped_column(nullable=False)
    condition: Mapped[AssetCondition] = mapped_column(SQLEnum(AssetCondition), nullable=False)
    location: Mapped[str] = mapped_column(String(255), nullable=False)
    gps_coordinates: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    custodian: Mapped[str] = mapped_column(String(255), nullable=False)
    maintenance_schedule: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    last_maintenance_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    next_maintenance_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    disposal_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    disposal_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    disposal_amount: Mapped[Optional[float]] = mapped_column(nullable=True)
    
    # Foreign keys - optional based on which level the asset belongs to
    ministry_id: Mapped[Optional[int]] = mapped_column(ForeignKey("ministries.id"), nullable=True)
    department_id: Mapped[Optional[int]] = mapped_column(ForeignKey("departments.id"), nullable=True)
    agency_id: Mapped[Optional[int]] = mapped_column(ForeignKey("agencies.id"), nullable=True)
    county_id: Mapped[Optional[int]] = mapped_column(ForeignKey("counties.id"), nullable=True)
    sub_county_id: Mapped[Optional[int]] = mapped_column(ForeignKey("sub_counties.id"), nullable=True)
    ward_id: Mapped[Optional[int]] = mapped_column(ForeignKey("wards.id"), nullable=True)
    
    def __repr__(self) -> str:
        return f"<PublicAsset(name='{self.name}', asset_number='{self.asset_number}')>"


class InfrastructureType(str, Enum):
    ROAD = "road"
    BRIDGE = "bridge"
    BUILDING = "building"
    WATER_SYSTEM = "water_system"
    POWER_SYSTEM = "power_system"
    TELECOMMUNICATION = "telecommunication"
    SCHOOL = "school"
    HOSPITAL = "hospital"
    OTHER = "other"


class InfrastructureStatus(str, Enum):
    PLANNED = "planned"
    UNDER_CONSTRUCTION = "under_construction"
    OPERATIONAL = "operational"
    UNDER_MAINTENANCE = "under_maintenance"
    DECOMMISSIONED = "decommissioned"


class Infrastructure(Base):
    """Represents public infrastructure."""
    __tablename__ = "infrastructure"
    
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    code: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    infrastructure_type: Mapped[InfrastructureType] = mapped_column(SQLEnum(InfrastructureType), nullable=False)
    status: Mapped[InfrastructureStatus] = mapped_column(SQLEnum(InfrastructureStatus), nullable=False)
    location: Mapped[str] = mapped_column(String(255), nullable=False)
    gps_coordinates: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    construction_start_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    construction_end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    inauguration_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    construction_cost: Mapped[Optional[float]] = mapped_column(nullable=True)
    funding_source: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    contractor: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    capacity: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    maintenance_schedule: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    last_maintenance_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    next_maintenance_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    
    # Foreign keys - optional based on which level the infrastructure belongs to
    ministry_id: Mapped[Optional[int]] = mapped_column(ForeignKey("ministries.id"), nullable=True)
    department_id: Mapped[Optional[int]] = mapped_column(ForeignKey("departments.id"), nullable=True)
    agency_id: Mapped[Optional[int]] = mapped_column(ForeignKey("agencies.id"), nullable=True)
    county_id: Mapped[Optional[int]] = mapped_column(ForeignKey("counties.id"), nullable=True)
    sub_county_id: Mapped[Optional[int]] = mapped_column(ForeignKey("sub_counties.id"), nullable=True)
    ward_id: Mapped[Optional[int]] = mapped_column(ForeignKey("wards.id"), nullable=True)
    
    def __repr__(self) -> str:
        return f"<Infrastructure(name='{self.name}', type='{self.infrastructure_type}', status='{self.status}')>"

