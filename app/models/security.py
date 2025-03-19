from datetime import datetime
from enum import Enum
from typing import Optional, List, TYPE_CHECKING
import uuid
from sqlalchemy import String, ForeignKey, Text, DateTime, Enum as SQLEnum, Integer, Boolean, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

if TYPE_CHECKING:
    from app.models.employee import UserAccount

class LoginStatus(str, Enum):
    SUCCESS = "success"
    FAILED = "failed"
    LOCKED = "locked"
    PASSWORD_EXPIRED = "password_expired"
    ACCOUNT_DISABLED = "account_disabled"
    SUSPICIOUS = "suspicious"

class ActivityType(str, Enum):
    LOGIN = "login"
    LOGOUT = "logout"
    PASSWORD_CHANGE = "password_change"
    PASSWORD_RESET = "password_reset"
    PROFILE_UPDATE = "profile_update"
    DATA_ACCESS = "data_access"
    DATA_MODIFICATION = "data_modification"
    REPORT_GENERATION = "report_generation"
    SYSTEM_CONFIGURATION = "system_configuration"
    API_ACCESS = "api_access"
    FILE_UPLOAD = "file_upload"
    FILE_DOWNLOAD = "file_download"
    PERMISSION_CHANGE = "permission_change"
    OTHER = "other"

class SeverityLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class LoginAttempt(Base):
    """Represents a user login attempt."""
    __tablename__ = "login_attempts"
    
    timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    ip_address: Mapped[str] = mapped_column(String(50), nullable=False)
    user_agent: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[LoginStatus] = mapped_column(SQLEnum(LoginStatus), nullable=False)
    failure_reason: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    device_info: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Foreign keys
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    
    # Relationships
    user: Mapped["UserAccount"] = relationship(back_populates="login_attempts")
    
    def __repr__(self) -> str:
        return f"<LoginAttempt(user_id={self.user_id}, timestamp='{self.timestamp}', status='{self.status}')>"

class UserActivity(Base):
    """Represents a user activity in the system."""
    __tablename__ = "user_activities"
    
    timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    activity_type: Mapped[ActivityType] = mapped_column(SQLEnum(ActivityType), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    ip_address: Mapped[str] = mapped_column(String(50), nullable=False)
    user_agent: Mapped[str] = mapped_column(String(255), nullable=False)
    module: Mapped[str] = mapped_column(String(100), nullable=False)
    action: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)  # Success, Failed, etc.
    details: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Foreign keys
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    
    # Relationships
    user: Mapped["UserAccount"] = relationship("UserAccount")
    
    def __repr__(self) -> str:
        return f"<UserActivity(user_id={self.user_id}, timestamp='{self.timestamp}', type='{self.activity_type}')>"

class SecurityIncident(Base):
    """Represents a security incident in the system."""
    __tablename__ = "security_incidents"
    
    incident_number: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    incident_type: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    severity: Mapped[SeverityLevel] = mapped_column(SQLEnum(SeverityLevel), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)  # Open, In Progress, Resolved, Closed
    reported_by: Mapped[str] = mapped_column(String(255), nullable=False)
    assigned_to: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    resolution: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    resolution_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    affected_systems: Mapped[str] = mapped_column(Text, nullable=False)
    affected_users: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    impact: Mapped[str] = mapped_column(Text, nullable=False)
    root_cause: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    mitigation_steps: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    lessons_learned: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Foreign keys
    reported_by_user_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("users.id"), nullable=True)
    
    # Relationships
    reported_by_user: Mapped[Optional["UserAccount"]] = relationship("UserAccount")
    
    def __repr__(self) -> str:
        return f"<SecurityIncident(incident_number='{self.incident_number}', type='{self.incident_type}', severity='{self.severity}')>"

class SecurityAudit(Base):
    """Represents a security audit of the system."""
    __tablename__ = "security_audits"
    
    audit_number: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    audit_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    audit_type: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    auditor: Mapped[str] = mapped_column(String(255), nullable=False)
    scope: Mapped[str] = mapped_column(Text, nullable=False)
    findings: Mapped[str] = mapped_column(Text, nullable=False)
    recommendations: Mapped[str] = mapped_column(Text, nullable=False)
    risk_level: Mapped[SeverityLevel] = mapped_column(SQLEnum(SeverityLevel), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)  # Open, In Progress, Closed
    action_plan: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    action_plan_due_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    action_plan_status: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    follow_up_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    follow_up_findings: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    def __repr__(self) -> str:
        return f"<SecurityAudit(audit_number='{self.audit_number}', type='{self.audit_type}', risk_level='{self.risk_level}')>"

class Permission(Base):
    """Represents a permission in the system."""
    __tablename__ = "permissions"
    
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    module: Mapped[str] = mapped_column(String(100), nullable=False)
    action: Mapped[str] = mapped_column(String(100), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    
    def __repr__(self) -> str:
        return f"<Permission(name='{self.name}', module='{self.module}', action='{self.action}')>"

class ApiKey(Base):
    """Represents an API key for external system integration."""
    __tablename__ = "api_keys"
    
    key_name: Mapped[str] = mapped_column(String(100), nullable=False)
    key_value: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    created_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    expiry_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    permissions: Mapped[str] = mapped_column(Text, nullable=False)  # JSON string of permissions
    rate_limit: Mapped[int] = mapped_column(Integer, nullable=False, default=100)  # Requests per minute
    last_used: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_by: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    
    # Relationships
    creator: Mapped["UserAccount"] = relationship("UserAccount")
    
    def __repr__(self) -> str:
        return f"<ApiKey(key_name='{self.key_name}', is_active={self.is_active})>"

class SecurityConfiguration(Base):
    """Represents security configuration settings."""
    __tablename__ = "security_configurations"
    
    config_key: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    config_value: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    is_encrypted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    last_updated: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    updated_by: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    
    # Relationships
    updater: Mapped["UserAccount"] = relationship("UserAccount")
    
    def __repr__(self) -> str:
        return f"<SecurityConfiguration(config_key='{self.config_key}', category='{self.category}')>"

class TwoFactorAuthentication(Base):
    """Represents two-factor authentication settings for a user."""
    __tablename__ = "two_factor_authentications"
    
    method: Mapped[str] = mapped_column(String(50), nullable=False)  # SMS, Email, Authenticator App, etc.
    is_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    phone_number: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    secret_key: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    backup_codes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON string of backup codes
    last_verified: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    # Foreign keys
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False, unique=True)
    
    # Relationships
    user: Mapped["UserAccount"] = relationship("UserAccount")
    
    def __repr__(self) -> str:
        return f"<TwoFactorAuthentication(user_id={self.user_id}, method='{self.method}', is_enabled={self.is_enabled})>"