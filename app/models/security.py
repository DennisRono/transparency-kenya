from datetime import datetime
from enum import Enum
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import String, ForeignKey, Text, DateTime, Enum as SQLEnum, Integer, Boolean, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base

if TYPE_CHECKING:
    from models.employee import UserAccount, Role

class LoginStatus(str, Enum):
    SUCCESS = "success"
    FAILED = "failed"
    LOCKED = "locked"
    PASSWORD_RESET = "password_reset"
    MFA_REQUIRED = "mfa_required"
    MFA_FAILED = "mfa_failed"

class LogSeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class IncidentSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class IncidentStatus(str, Enum):
    OPEN = "open"
    INVESTIGATING = "investigating"
    CONTAINED = "contained"
    RESOLVED = "resolved"
    CLOSED = "closed"

class BackupStatus(str, Enum):
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    RESTORED = "restored"

class LoginAttempt(Base):
    """Represents a user login attempt."""
    __tablename__ = "login_attempts"
    
    timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    status: Mapped[LoginStatus] = mapped_column(SQLEnum(LoginStatus), nullable=False)
    ip_address: Mapped[str] = mapped_column(String(50), nullable=False)
    user_agent: Mapped[str] = mapped_column(String(255), nullable=False)
    device_info: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    failure_reason: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Foreign keys
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    
    # Relationships
    user: Mapped["UserAccount"] = relationship(back_populates="login_attempts")
    
    def __repr__(self) -> str:
        return f"<LoginAttempt(user_id={self.user_id}, timestamp='{self.timestamp}', status='{self.status}')>"

class SecurityLog(Base):
    """Represents a security-related event log."""
    __tablename__ = "security_logs"
    
    timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    event_type: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    severity: Mapped[LogSeverity] = mapped_column(SQLEnum(LogSeverity), nullable=False)
    source: Mapped[str] = mapped_column(String(255), nullable=False)  # Application, System, Network, etc.
    ip_address: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    user_agent: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    affected_resource: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    action_taken: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Foreign keys
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)
    
    # Relationships
    user: Mapped[Optional["UserAccount"]] = relationship()
    
    def __repr__(self) -> str:
        return f"<SecurityLog(timestamp='{self.timestamp}', event_type='{self.event_type}', severity='{self.severity}')>"

class AccessControlList(Base):
    """Represents access control permissions for resources."""
    __tablename__ = "access_control_lists"
    
    resource_type: Mapped[str] = mapped_column(String(100), nullable=False)
    resource_id: Mapped[str] = mapped_column(String(100), nullable=False)
    permissions: Mapped[str] = mapped_column(Text, nullable=False)  # JSON string of permissions
    granted_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    
    # Foreign keys
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)
    role_id: Mapped[Optional[int]] = mapped_column(ForeignKey("roles.id"), nullable=True)
    granted_by: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    
    # Relationships
    user: Mapped[Optional["UserAccount"]] = relationship(foreign_keys=[user_id])
    role: Mapped[Optional["Role"]] = relationship()
    grantor: Mapped["UserAccount"] = relationship(foreign_keys=[granted_by])
    
    def __repr__(self) -> str:
        return f"<AccessControlList(resource_type='{self.resource_type}', resource_id='{self.resource_id}')>"

class SystemSetting(Base):
    """Represents system configuration settings."""
    __tablename__ = "system_settings"
    
    setting_key: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    setting_value: Mapped[str] = mapped_column(Text, nullable=False)
    data_type: Mapped[str] = mapped_column(String(50), nullable=False)  # string, integer, boolean, json, etc.
    description: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    is_sensitive: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_encrypted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    last_modified: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    
    # Foreign keys
    modified_by: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    
    # Relationships
    modifier: Mapped["UserAccount"] = relationship()
    
    def __repr__(self) -> str:
        return f"<SystemSetting(key='{self.setting_key}', category='{self.category}')>"

class SecurityIncident(Base):
    """Represents a security incident."""
    __tablename__ = "security_incidents"
    
    incident_number: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    incident_type: Mapped[str] = mapped_column(String(100), nullable=False)  # Data Breach, Unauthorized Access, etc.
    severity: Mapped[IncidentSeverity] = mapped_column(SQLEnum(IncidentSeverity), nullable=False)
    status: Mapped[IncidentStatus] = mapped_column(SQLEnum(IncidentStatus), nullable=False)
    reported_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    detected_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    resolved_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    affected_systems: Mapped[str] = mapped_column(Text, nullable=False)
    affected_data: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    impact_assessment: Mapped[str] = mapped_column(Text, nullable=False)
    root_cause: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    resolution: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    lessons_learned: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    preventive_measures: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Foreign keys
    reported_by: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    assigned_to: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)
    
    # Relationships
    reporter: Mapped["UserAccount"] = relationship(foreign_keys=[reported_by])
    assignee: Mapped[Optional["UserAccount"]] = relationship(foreign_keys=[assigned_to])
    
    def __repr__(self) -> str:
        return f"<SecurityIncident(incident_number='{self.incident_number}', severity='{self.severity}', status='{self.status}')>"

class DataBackup(Base):
    """Represents a system data backup."""
    __tablename__ = "data_backups"
    
    backup_id: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    backup_type: Mapped[str] = mapped_column(String(50), nullable=False)  # Full, Incremental, Differential
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[BackupStatus] = mapped_column(SQLEnum(BackupStatus), nullable=False)
    start_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_time: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    size_mb: Mapped[Optional[float]] = mapped_column(nullable=True)
    location: Mapped[str] = mapped_column(String(255), nullable=False)
    storage_type: Mapped[str] = mapped_column(String(100), nullable=False)  # Local, Cloud, Tape, etc.
    retention_period_days: Mapped[int] = mapped_column(Integer, nullable=False)
    expiry_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    is_encrypted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    encryption_method: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    is_compressed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    compression_method: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    verification_status: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    verification_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    restore_tested: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    restore_test_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    restore_test_result: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Foreign keys
    initiated_by: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    verified_by: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)
    
    # Relationships
    initiator: Mapped["UserAccount"] = relationship(foreign_keys=[initiated_by])
    verifier: Mapped[Optional["UserAccount"]] = relationship(foreign_keys=[verified_by])
    
    def __repr__(self) -> str:
        return f"<DataBackup(backup_id='{self.backup_id}', type='{self.backup_type}', status='{self.status}')>"

class SystemAuditLog(Base):
    """Represents a system audit log for tracking changes to data."""
    __tablename__ = "system_audit_logs"
    
    timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    action: Mapped[str] = mapped_column(String(50), nullable=False)  # Create, Update, Delete, View
    entity_type: Mapped[str] = mapped_column(String(100), nullable=False)
    entity_id: Mapped[str] = mapped_column(String(100), nullable=False)
    changes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON string of changes
    old_values: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON string of old values
    new_values: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON string of new values
    ip_address: Mapped[str] = mapped_column(String(50), nullable=False)
    user_agent: Mapped[str] = mapped_column(String(255), nullable=False)
    
    # Foreign keys
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    
    # Relationships
    user: Mapped["UserAccount"] = relationship()
    
    def __repr__(self) -> str:
        return f"<SystemAuditLog(timestamp='{self.timestamp}', action='{self.action}', entity_type='{self.entity_type}')>"

