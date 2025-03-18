from datetime import date
from enum import Enum
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import String, ForeignKey, Text, Date, Integer, Enum as SQLEnum, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

if TYPE_CHECKING:
    from app.models.employee import Employee

class PerformanceRating(str, Enum):
    EXCELLENT = "excellent"
    GOOD = "good"
    SATISFACTORY = "satisfactory"
    NEEDS_IMPROVEMENT = "needs_improvement"
    UNSATISFACTORY = "unsatisfactory"

class GoalStatus(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class ReviewStatus(str, Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    COMPLETED = "completed"
    ACKNOWLEDGED = "acknowledged"
    DISPUTED = "disputed"
    REVISED = "revised"

class PerformanceReview(Base):
    """Represents a performance review for an employee."""
    __tablename__ = "performance_reviews"
    
    review_date: Mapped[date] = mapped_column(Date, nullable=False)
    review_period_start: Mapped[date] = mapped_column(Date, nullable=False)
    review_period_end: Mapped[date] = mapped_column(Date, nullable=False)
    overall_rating: Mapped[PerformanceRating] = mapped_column(SQLEnum(PerformanceRating), nullable=False)
    strengths: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    areas_for_improvement: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    reviewer_comments: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    employee_comments: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[ReviewStatus] = mapped_column(SQLEnum(ReviewStatus), nullable=False, default=ReviewStatus.DRAFT)
    submission_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    completion_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    acknowledgment_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    dispute_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    dispute_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    dispute_resolution: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    dispute_resolution_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    next_review_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    
    # Foreign keys
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    reviewer_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    
    # Relationships
    employee: Mapped["Employee"] = relationship(back_populates="performance_reviews", foreign_keys=[employee_id])
    reviewer: Mapped["Employee"] = relationship(foreign_keys=[reviewer_id])
    performance_metrics: Mapped[List["PerformanceMetric"]] = relationship(back_populates="performance_review", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<PerformanceReview(employee_id={self.employee_id}, review_date='{self.review_date}', rating='{self.overall_rating}')>"


class PerformanceMetric(Base):
    """Represents a specific metric evaluated in a performance review."""
    __tablename__ = "performance_metrics"
    
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    weight: Mapped[float] = mapped_column(nullable=False)  # Percentage weight of this metric in the overall review
    rating: Mapped[PerformanceRating] = mapped_column(SQLEnum(PerformanceRating), nullable=False)
    comments: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    target: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    actual_achievement: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    evidence: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Foreign keys
    performance_review_id: Mapped[int] = mapped_column(ForeignKey("performance_reviews.id"), nullable=False)
    
    # Relationships
    performance_review: Mapped["PerformanceReview"] = relationship(back_populates="performance_metrics")
    
    def __repr__(self) -> str:
        return f"<PerformanceMetric(name='{self.name}', rating='{self.rating}')>"


class PerformanceGoal(Base):
    """Represents a performance goal set for an employee."""
    __tablename__ = "performance_goals"
    
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    target_date: Mapped[date] = mapped_column(Date, nullable=False)
    completion_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    status: Mapped[GoalStatus] = mapped_column(SQLEnum(GoalStatus), nullable=False, default=GoalStatus.NOT_STARTED)
    priority: Mapped[int] = mapped_column(Integer, nullable=False)  # 1 = highest priority
    progress: Mapped[int] = mapped_column(Integer, nullable=False, default=0)  # Percentage complete
    measurement_criteria: Mapped[str] = mapped_column(Text, nullable=False)
    resources_required: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    challenges: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    achievements: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    feedback: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    linked_to_strategic_objective: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    strategic_objective: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Foreign keys
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    supervisor_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    
    # Relationships
    employee: Mapped["Employee"] = relationship(foreign_keys=[employee_id])
    supervisor: Mapped["Employee"] = relationship(foreign_keys=[supervisor_id])
    
    def __repr__(self) -> str:
        return f"<PerformanceGoal(title='{self.title}', status='{self.status}', progress={self.progress}%)>"


class TeamPerformance(Base):
    """Represents performance metrics for a team or department."""
    __tablename__ = "team_performances"
    
    period_start: Mapped[date] = mapped_column(Date, nullable=False)
    period_end: Mapped[date] = mapped_column(Date, nullable=False)
    team_name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    overall_rating: Mapped[PerformanceRating] = mapped_column(SQLEnum(PerformanceRating), nullable=False)
    achievements: Mapped[str] = mapped_column(Text, nullable=False)
    challenges: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    improvement_areas: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    action_plan: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Foreign keys
    team_lead_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    evaluator_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    
    # Optional foreign keys for organizational placement
    ministry_id: Mapped[Optional[int]] = mapped_column(ForeignKey("ministries.id"), nullable=True)
    department_id: Mapped[Optional[int]] = mapped_column(ForeignKey("departments.id"), nullable=True)
    agency_id: Mapped[Optional[int]] = mapped_column(ForeignKey("agencies.id"), nullable=True)
    county_id: Mapped[Optional[int]] = mapped_column(ForeignKey("counties.id"), nullable=True)
    
    # Relationships
    team_lead: Mapped["Employee"] = relationship(foreign_keys=[team_lead_id])
    evaluator: Mapped["Employee"] = relationship(foreign_keys=[evaluator_id])
    
    def __repr__(self) -> str:
        return f"<TeamPerformance(team_name='{self.team_name}', period='{self.period_start} to {self.period_end}', rating='{self.overall_rating}')>"


class DepartmentPerformance(Base):
    """Represents performance metrics for an entire department."""
    __tablename__ = "department_performances"
    
    fiscal_year: Mapped[str] = mapped_column(String(10), nullable=False)
    period_start: Mapped[date] = mapped_column(Date, nullable=False)
    period_end: Mapped[date] = mapped_column(Date, nullable=False)
    overall_rating: Mapped[PerformanceRating] = mapped_column(SQLEnum(PerformanceRating), nullable=False)
    key_achievements: Mapped[str] = mapped_column(Text, nullable=False)
    budget_performance: Mapped[float] = mapped_column(nullable=False)  # Percentage of budget utilized effectively
    targets_met: Mapped[int] = mapped_column(Integer, nullable=False)  # Number of targets met
    total_targets: Mapped[int] = mapped_column(Integer, nullable=False)  # Total number of targets
    challenges: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    recommendations: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    action_plan: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Foreign keys
    department_head_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    evaluator_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    
    # Optional foreign keys for organizational placement
    ministry_id: Mapped[Optional[int]] = mapped_column(ForeignKey("ministries.id"), nullable=True)
    department_id: Mapped[Optional[int]] = mapped_column(ForeignKey("departments.id"), nullable=True)
    agency_id: Mapped[Optional[int]] = mapped_column(ForeignKey("agencies.id"), nullable=True)
    county_id: Mapped[Optional[int]] = mapped_column(ForeignKey("counties.id"), nullable=True)
    
    # Relationships
    department_head: Mapped["Employee"] = relationship(foreign_keys=[department_head_id])
    evaluator: Mapped["Employee"] = relationship(foreign_keys=[evaluator_id])
    
    def __repr__(self) -> str:
        return f"<DepartmentPerformance(fiscal_year='{self.fiscal_year}', rating='{self.overall_rating}')>"


class ServiceDeliveryMetric(Base):
    """Represents metrics for service delivery performance."""
    __tablename__ = "service_delivery_metrics"
    
    service_name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    period_start: Mapped[date] = mapped_column(Date, nullable=False)
    period_end: Mapped[date] = mapped_column(Date, nullable=False)
    target_value: Mapped[float] = mapped_column(nullable=False)
    actual_value: Mapped[float] = mapped_column(nullable=False)
    unit_of_measure: Mapped[str] = mapped_column(String(50), nullable=False)
    performance_percentage: Mapped[float] = mapped_column(nullable=False)
    rating: Mapped[PerformanceRating] = mapped_column(SQLEnum(PerformanceRating), nullable=False)
    data_source: Mapped[str] = mapped_column(String(255), nullable=False)
    data_collection_method: Mapped[str] = mapped_column(String(255), nullable=False)
    challenges: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    improvement_actions: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Foreign keys
    responsible_officer_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    
    # Optional foreign keys for organizational placement
    ministry_id: Mapped[Optional[int]] = mapped_column(ForeignKey("ministries.id"), nullable=True)
    department_id: Mapped[Optional[int]] = mapped_column(ForeignKey("departments.id"), nullable=True)
    agency_id: Mapped[Optional[int]] = mapped_column(ForeignKey("agencies.id"), nullable=True)
    county_id: Mapped[Optional[int]] = mapped_column(ForeignKey("counties.id"), nullable=True)
    sub_county_id: Mapped[Optional[int]] = mapped_column(ForeignKey("sub_counties.id"), nullable=True)
    ward_id: Mapped[Optional[int]] = mapped_column(ForeignKey("wards.id"), nullable=True)
    
    # Relationships
    responsible_officer: Mapped["Employee"] = relationship(foreign_keys=[responsible_officer_id])
    
    def __repr__(self) -> str:
        return f"<ServiceDeliveryMetric(service_name='{self.service_name}', performance_percentage={self.performance_percentage}%, rating='{self.rating}')>"

