from datetime import date
from enum import Enum
from typing import Optional, List, TYPE_CHECKING
import uuid
from sqlalchemy import String, ForeignKey, Text, Date, Enum as SQLEnum, Integer, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

if TYPE_CHECKING:
    from app.models.employee import Employee

class Ministry(Base):
    """Represents a government ministry."""
    __tablename__ = "ministries"
    
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    code: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    mission: Mapped[str] = mapped_column(Text, nullable=False)
    vision: Mapped[str] = mapped_column(Text, nullable=False)
    functions: Mapped[str] = mapped_column(Text, nullable=False)
    establishment_date: Mapped[date] = mapped_column(Date, nullable=False)
    website: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    physical_address: Mapped[str] = mapped_column(Text, nullable=False)
    postal_address: Mapped[str] = mapped_column(String(100), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    
    # Foreign keys with use_alter=True to avoid circular dependencies
    minister_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("employees.id", use_alter=True, name="fk_ministry_minister"),
        nullable=True
    )
    permanent_secretary_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("employees.id", use_alter=True, name="fk_ministry_permanent_secretary"),
        nullable=True
    )
    
    # Relationships
    minister: Mapped[Optional["Employee"]] = relationship(
        "Employee", 
        foreign_keys=[minister_id],
        post_update=True
    )
    permanent_secretary: Mapped[Optional["Employee"]] = relationship(
        "Employee", 
        foreign_keys=[permanent_secretary_id],
        post_update=True
    )
    departments: Mapped[List["Department"]] = relationship(back_populates="ministry", cascade="all, delete-orphan")
    agencies: Mapped[List["Agency"]] = relationship(back_populates="ministry")
    
    def __repr__(self) -> str:
        return f"<Ministry(name='{self.name}', code='{self.code}')>"

class Department(Base):
    """Represents a department within a ministry."""
    __tablename__ = "departments"
    
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    code: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    functions: Mapped[str] = mapped_column(Text, nullable=False)
    establishment_date: Mapped[date] = mapped_column(Date, nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    physical_address: Mapped[str] = mapped_column(Text, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    
    # Foreign keys
    ministry_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("ministries.id"), nullable=False)
    director_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("employees.id", use_alter=True, name="fk_department_director"),
        nullable=True
    )
    
    # Relationships
    ministry: Mapped["Ministry"] = relationship(back_populates="departments")
    director: Mapped[Optional["Employee"]] = relationship(
        "Employee", 
        foreign_keys=[director_id],
        post_update=True
    )
    divisions: Mapped[List["Division"]] = relationship(back_populates="department", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<Department(name='{self.name}', code='{self.code}', ministry_id={self.ministry_id})>"

class Division(Base):
    """Represents a division within a department."""
    __tablename__ = "divisions"
    
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    code: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    functions: Mapped[str] = mapped_column(Text, nullable=False)
    establishment_date: Mapped[date] = mapped_column(Date, nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    
    # Foreign keys
    department_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("departments.id"), nullable=False)
    head_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("employees.id", use_alter=True, name="fk_division_head"),
        nullable=True
    )
    
    # Relationships
    department: Mapped["Department"] = relationship(back_populates="divisions")
    head: Mapped[Optional["Employee"]] = relationship(
        "Employee", 
        foreign_keys=[head_id],
        post_update=True
    )
    
    def __repr__(self) -> str:
        return f"<Division(name='{self.name}', code='{self.code}', department_id={self.department_id})>"

class Agency(Base):
    """Represents a government agency or parastatal."""
    __tablename__ = "agencies"
    
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    code: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    mission: Mapped[str] = mapped_column(Text, nullable=False)
    vision: Mapped[str] = mapped_column(Text, nullable=False)
    functions: Mapped[str] = mapped_column(Text, nullable=False)
    establishment_date: Mapped[date] = mapped_column(Date, nullable=False)
    legal_mandate: Mapped[str] = mapped_column(Text, nullable=False)
    website: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    physical_address: Mapped[str] = mapped_column(Text, nullable=False)
    postal_address: Mapped[str] = mapped_column(String(100), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    
    # Foreign keys
    ministry_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("ministries.id"), nullable=True)
    ceo_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("employees.id", use_alter=True, name="fk_agency_ceo"),
        nullable=True
    )
    
    # Relationships
    ministry: Mapped[Optional["Ministry"]] = relationship(back_populates="agencies")
    ceo: Mapped[Optional["Employee"]] = relationship(
        "Employee", 
        foreign_keys=[ceo_id],
        post_update=True
    )
    
    def __repr__(self) -> str:
        return f"<Agency(name='{self.name}', code='{self.code}')>"

class County(Base):
    """Represents a county government."""
    __tablename__ = "counties"
    
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    code: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    region: Mapped[str] = mapped_column(String(100), nullable=False)
    capital: Mapped[str] = mapped_column(String(100), nullable=False)
    area: Mapped[float] = mapped_column(nullable=False)  # In square kilometers
    population: Mapped[int] = mapped_column(Integer, nullable=False)
    website: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    physical_address: Mapped[str] = mapped_column(Text, nullable=False)
    postal_address: Mapped[str] = mapped_column(String(100), nullable=False)
    
    # Foreign keys
    governor_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("employees.id", use_alter=True, name="fk_county_governor"),
        nullable=True
    )
    deputy_governor_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("employees.id", use_alter=True, name="fk_county_deputy_governor"),
        nullable=True
    )
    
    # Relationships
    governor: Mapped[Optional["Employee"]] = relationship(
        "Employee", 
        foreign_keys=[governor_id],
        post_update=True
    )
    deputy_governor: Mapped[Optional["Employee"]] = relationship(
        "Employee", 
        foreign_keys=[deputy_governor_id],
        post_update=True
    )
    sub_counties: Mapped[List["SubCounty"]] = relationship(back_populates="county", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<County(name='{self.name}', code='{self.code}')>"

class SubCounty(Base):
    """Represents a sub-county within a county."""
    __tablename__ = "sub_counties"
    
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    code: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    area: Mapped[Optional[float]] = mapped_column(nullable=True)  # In square kilometers
    population: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    headquarters: Mapped[str] = mapped_column(String(100), nullable=False)
    
    # Foreign keys
    county_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("counties.id"), nullable=False)
    administrator_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("employees.id", use_alter=True, name="fk_subcounty_administrator"),
        nullable=True
    )
    
    # Relationships
    county: Mapped["County"] = relationship(back_populates="sub_counties")
    administrator: Mapped[Optional["Employee"]] = relationship(
        "Employee", 
        foreign_keys=[administrator_id],
        post_update=True
    )
    wards: Mapped[List["Ward"]] = relationship(back_populates="sub_county", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<SubCounty(name='{self.name}', code='{self.code}', county_id={self.county_id})>"

class Ward(Base):
    """Represents a ward within a sub-county."""
    __tablename__ = "wards"
    
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    code: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    area: Mapped[Optional[float]] = mapped_column(nullable=True)  # In square kilometers
    population: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    # Foreign keys
    sub_county_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("sub_counties.id"), nullable=False)
    administrator_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("employees.id", use_alter=True, name="fk_ward_administrator"),
        nullable=True
    )
    
    # Relationships
    sub_county: Mapped["SubCounty"] = relationship(back_populates="wards")
    administrator: Mapped[Optional["Employee"]] = relationship(
        "Employee", 
        foreign_keys=[administrator_id],
        post_update=True
    )
    
    def __repr__(self) -> str:
        return f"<Ward(name='{self.name}', code='{self.code}', sub_county_id={self.sub_county_id})>"

class Project(Base):
    """Represents a government project."""
    __tablename__ = "projects"
    
    project_number: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    objectives: Mapped[str] = mapped_column(Text, nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)  # Planning, Implementation, Completed, On Hold, Cancelled
    budget: Mapped[float] = mapped_column(nullable=False)
    funding_source: Mapped[str] = mapped_column(String(255), nullable=False)
    location: Mapped[str] = mapped_column(String(255), nullable=False)
    beneficiaries: Mapped[str] = mapped_column(Text, nullable=False)
    key_deliverables: Mapped[str] = mapped_column(Text, nullable=False)
    risks: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    mitigation_measures: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    progress: Mapped[int] = mapped_column(Integer, nullable=False, default=0)  # Percentage complete
    
    # Foreign keys
    project_manager_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("employees.id", use_alter=True, name="fk_project_manager"),
        nullable=False
    )
    
    # Optional foreign keys for organizational placement
    ministry_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("ministries.id"), nullable=True)
    department_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("departments.id"), nullable=True)
    agency_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("agencies.id"), nullable=True)
    county_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("counties.id"), nullable=True)
    
    # Relationships
    project_manager: Mapped["Employee"] = relationship(
        "Employee", 
        foreign_keys=[project_manager_id],
        post_update=True
    )
    
    def __repr__(self) -> str:
        return f"<Project(project_number='{self.project_number}', title='{self.title}', status='{self.status}')>"

class Policy(Base):
    """Represents a government policy."""
    __tablename__ = "government_policies"
    
    policy_number: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    objectives: Mapped[str] = mapped_column(Text, nullable=False)
    effective_date: Mapped[date] = mapped_column(Date, nullable=False)
    expiry_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False)  # Draft, Approved, Implemented, Superseded, Archived
    target_audience: Mapped[str] = mapped_column(Text, nullable=False)
    implementation_strategy: Mapped[str] = mapped_column(Text, nullable=False)
    monitoring_framework: Mapped[str] = mapped_column(Text, nullable=False)
    evaluation_criteria: Mapped[str] = mapped_column(Text, nullable=False)
    document_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Foreign keys
    author_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("employees.id", use_alter=True, name="fk_policy_author"),
        nullable=False
    )
    approved_by: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("employees.id", use_alter=True, name="fk_policy_approver"),
        nullable=True
    )
    
    # Optional foreign keys for organizational placement
    ministry_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("ministries.id"), nullable=True)
    department_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("departments.id"), nullable=True)
    agency_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("agencies.id"), nullable=True)
    county_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("counties.id"), nullable=True)
    
    # Relationships
    author: Mapped["Employee"] = relationship(
        "Employee", 
        foreign_keys=[author_id],
        post_update=True
    )
    approver: Mapped[Optional["Employee"]] = relationship(
        "Employee", 
        foreign_keys=[approved_by],
        post_update=True
    )
    
    def __repr__(self) -> str:
        return f"<Policy(policy_number='{self.policy_number}', title='{self.title}', status='{self.status}')>"