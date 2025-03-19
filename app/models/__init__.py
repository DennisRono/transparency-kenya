from typing import TYPE_CHECKING

# Import Base first
from app.models.base import Base

# Import models without circular dependencies first
from app.models.employee import (
    Gender, EmploymentStatus, MaritalStatus, EducationLevel,
    QualificationType, TrainingStatus, LeaveType, LeaveStatus,
    DisciplinaryType, DisciplinaryStatus, BenefitType, AllowanceType,
    Position, Role, Employee, UserAccount, EmploymentHistory,
    Qualification, Education, Training, Attendance, Leave,
    DisciplinaryAction, Benefit, Allowance, EmployeeEmergencyContact
)

# Import models with fewer dependencies
from app.models.government import (
    Ministry, Department, Division, Agency, 
    County, SubCounty, Ward, Project, Policy as GovernmentPolicy
)

from app.models.performance import (
    PerformanceRating, GoalStatus, ReviewStatus,
    PerformanceReview, PerformanceMetric, PerformanceGoal,
    TeamPerformance, DepartmentPerformance, ServiceDeliveryMetric
)

from app.models.compliance import (
    ComplianceStatus, RiskLevel, AuditStatus, InvestigationStatus,
    ComplianceRequirement, ComplianceReport, ComplianceAudit,
    Investigation, RiskAssessment, RiskRegister, Policy, Regulation
)

from app.models.finance import (
    PaymentStatus, PaymentMethod, TransactionType,
    Budget, BudgetItem, Expenditure, Salary, Payment, FinancialReport
)

from app.models.security import (
    LoginStatus, ActivityType, SeverityLevel,
    LoginAttempt, UserActivity, SecurityIncident, SecurityAudit,
    Permission, ApiKey, SecurityConfiguration, TwoFactorAuthentication
)

# Import models with more complex dependencies
from app.models.police import (
    OfficerRank, OfficerStatus, ComplaintStatus, ComplaintPriority,
    InvestigationStatus as PoliceInvestigationStatus, IncidentType, IncidentSeverity,
    IncidentStatus, DisciplinaryActionType, DisciplinaryActionStatus, EvidenceType,
    PoliceStation, PoliceOfficer, PoliceComplaint, PoliceInvestigation,
    PoliceDisciplinaryAction, Evidence, IncidentReport
)

from app.models.crime_reporting import (
    CrimeType, CrimeSeverity, CaseStatus,
    CrimeReport, CriminalCase, CaseUpdate, MissingPerson, WantedPerson
)

# Define __all__ to control what gets imported with "from app.models import *"
__all__ = [
    'Base',
    # Employee
    'Gender', 'EmploymentStatus', 'MaritalStatus', 'EducationLevel',
    'QualificationType', 'TrainingStatus', 'LeaveType', 'LeaveStatus',
    'DisciplinaryType', 'DisciplinaryStatus', 'BenefitType', 'AllowanceType',
    'Position', 'Role', 'Employee', 'UserAccount', 'EmploymentHistory',
    'Qualification', 'Education', 'Training', 'Attendance', 'Leave',
    'DisciplinaryAction', 'Benefit', 'Allowance', 'EmployeeEmergencyContact',
    # Government
    'Ministry', 'Department', 'Division', 'Agency', 
    'County', 'SubCounty', 'Ward', 'Project', 'GovernmentPolicy',
    # Performance
    'PerformanceRating', 'GoalStatus', 'ReviewStatus',
    'PerformanceReview', 'PerformanceMetric', 'PerformanceGoal',
    'TeamPerformance', 'DepartmentPerformance', 'ServiceDeliveryMetric',
    # Compliance
    'ComplianceStatus', 'RiskLevel', 'AuditStatus', 'InvestigationStatus',
    'ComplianceRequirement', 'ComplianceReport', 'ComplianceAudit',
    'Investigation', 'RiskAssessment', 'RiskRegister', 'Policy', 'Regulation',
    # Finance
    'PaymentStatus', 'PaymentMethod', 'TransactionType',
    'Budget', 'BudgetItem', 'Expenditure', 'Salary', 'Payment', 'FinancialReport',
    # Security
    'LoginStatus', 'ActivityType', 'SeverityLevel',
    'LoginAttempt', 'UserActivity', 'SecurityIncident', 'SecurityAudit',
    'Permission', 'ApiKey', 'SecurityConfiguration', 'TwoFactorAuthentication',
    # Police
    'OfficerRank', 'OfficerStatus', 'ComplaintStatus', 'ComplaintPriority',
    'PoliceInvestigationStatus', 'IncidentType', 'IncidentSeverity',
    'IncidentStatus', 'DisciplinaryActionType', 'DisciplinaryActionStatus', 'EvidenceType',
    'PoliceStation', 'PoliceOfficer', 'PoliceComplaint', 'PoliceInvestigation',
    'PoliceDisciplinaryAction', 'Evidence', 'IncidentReport',
    # Crime Reporting
    'CrimeType', 'CrimeSeverity', 'CaseStatus',
    'CrimeReport', 'CriminalCase', 'CaseUpdate', 'MissingPerson', 'WantedPerson'
]