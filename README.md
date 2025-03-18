# Transparency Kenya

## Project Overview

Transparency Kenya is a comprehensive government management system designed to enhance transparency, accountability, and efficiency in public administration. The system provides a robust platform for tracking government resources, personnel, finances, and operations while preventing corruption and ensuring public oversight.

## Purpose

The primary goals of this system are to:

1. **Enhance Transparency**: Make government operations and resource allocation visible to the public
2. **Prevent Corruption**: Implement robust tracking and audit mechanisms to deter misuse of public resources
3. **Improve Accountability**: Track performance and responsibility at all levels of government
4. **Increase Efficiency**: Streamline government operations and resource management
5. **Empower Citizens**: Provide mechanisms for public participation, feedback, and oversight
6. **Ensure Police Accountability**: Monitor police conduct and prevent abuse of power
7. **Enable Real-time Crime Reporting**: Allow citizens to report crimes and submit evidence directly

## System Architecture

The Transparency Kenya system is built using:

- **Backend**: Python with SQLAlchemy ORM for database interactions
- **Database**: Relational database (compatible with PostgreSQL, MySQL, SQLite)
- **API Layer**: RESTful API for frontend and mobile app integration
- **Authentication**: Role-based access control with secure authentication

## Database Schema Overview

The database is organized into the following modules:

1. **Government Structure**: Ministries, departments, agencies, counties, etc.
2. **Employee Management**: Personnel records, positions, qualifications, etc.
3. **Finance**: Budgets, expenditures, revenues, assets, procurement, etc.
4. **Performance**: Reviews, metrics, goals, service delivery measurements
5. **Public Interaction**: Complaints, feedback, public participation
6. **Compliance**: Requirements, reports, audits, risk assessments
7. **Security**: System access, logs, incidents
8. **Police Accountability**: Officers, incidents, complaints, investigations
9. **Crime Reporting**: Citizen reports, media evidence, witness statements

## Detailed Module Descriptions

### 1. Government Structure Module

This module tracks the organizational structure of the government.

#### Key Tables:

- **Ministries**: Government ministries with budget allocations and contact information
- **Departments**: Departments within ministries
- **Agencies**: Agencies under departments
- **Counties**: County governments with demographic and budget information
- **SubCounties**: Administrative divisions within counties
- **Wards**: Smallest administrative units
- **Projects**: Government projects with status, budget, and outcomes
- **Programs**: Collections of related projects or initiatives
- **Committees**: Standing or ad-hoc committees
- **TaskForces**: Special working groups
- **PublicAssets**: Government-owned assets
- **Infrastructure**: Public infrastructure like roads, buildings, etc.

### 2. Employee Management Module

This module manages government employees and their information.

#### Key Tables:

- **Employees**: Comprehensive employee information
- **Positions**: Job positions with responsibilities and qualifications
- **EmploymentHistory**: Track position changes and transfers
- **Roles**: System roles with permissions
- **UserAccounts**: System access accounts
- **Qualifications**: Professional qualifications
- **Education**: Educational background
- **Training**: Training programs attended
- **Attendance**: Work attendance records
- **Leave**: Leave requests and approvals
- **DisciplinaryActions**: Workplace disciplinary measures
- **Benefits**: Employee benefits
- **Allowances**: Additional payments
- **EmergencyContacts**: Emergency contact information

### 3. Finance Module

This module tracks all financial aspects of government operations.

#### Key Tables:

- **Salaries**: Employee salary records
- **Budgets**: Budget allocations
- **Expenditures**: Spending records
- **Revenues**: Income and revenue collection
- **Transactions**: Financial transactions
- **Audits**: Financial audit records
- **Grants**: External funding received
- **Donations**: Donations received
- **Loans**: Loans taken by government entities
- **DebtPayments**: Loan repayments
- **Investments**: Government investments
- **TaxCollection**: Tax revenue records
- **Assets**: Government assets
- **AssetCategories**: Categories of assets
- **AssetMovements**: Asset transfers
- **AssetMaintenance**: Maintenance records
- **Procurement**: Procurement processes
- **Contracts**: Vendor contracts
- **ContractPayments**: Payments against contracts
- **Vendors**: Supplier information
- **Invoices**: Bills from vendors

### 4. Performance Module

This module tracks performance at individual and organizational levels.

#### Key Tables:

- **PerformanceReviews**: Employee performance evaluations
- **PerformanceMetrics**: Specific metrics for evaluation
- **PerformanceGoals**: Individual performance targets
- **TeamPerformance**: Team-level performance
- **DepartmentPerformance**: Department-level performance
- **ServiceDeliveryMetrics**: Public service performance metrics

### 5. Public Interaction Module

This module manages interactions with the public.

#### Key Tables:

- **Complaints**: Public complaints
- **Feedback**: General feedback
- **PublicParticipation**: Citizen participation in government
- **InformationRequests**: Freedom of information requests
- **ServiceRatings**: Ratings of government services
- **CitizenSatisfactionSurveys**: Survey results
- **PublicMeetings**: Community engagement events

### 6. Compliance Module

This module ensures adherence to laws, regulations, and policies.

#### Key Tables:

- **ComplianceRequirements**: Legal and regulatory requirements
- **ComplianceReports**: Compliance status reports
- **Audits**: Compliance audits
- **Investigations**: Investigations into non-compliance
- **RiskAssessments**: Evaluation of compliance risks
- **RiskRegisters**: Documented risks
- **Policies**: Internal policies
- **Regulations**: Applicable regulations

### 7. Security Module

This module manages system security and access.

#### Key Tables:

- **LoginAttempts**: System access attempts
- **SecurityLogs**: Security-related events
- **AccessControlLists**: Permission settings
- **SystemSettings**: Configuration settings
- **SecurityIncidents**: Security breaches or issues
- **DataBackups**: Backup records
- **SystemAuditLogs**: System activity logs

### 8. Police Accountability Module

This module tracks police conduct and accountability.

#### Key Tables:

- **PoliceOfficers**: Officer information and service records
- **IncidentReports**: Reports of police incidents
- **Complaints**: Complaints against officers
- **Investigations**: Internal investigations
- **DisciplinaryActions**: Actions taken against officers
- **Evidence**: Evidence in investigations

### 9. Crime Reporting Module

This module enables citizen reporting of crimes.

#### Key Tables:

- **CrimeReports**: Citizen-reported crimes
- **MediaEvidence**: Photos, videos, audio, and documents submitted as evidence
- **WitnessStatements**: Statements from witnesses
- **ReportStatusUpdates**: Updates on report processing
- **EmergencyContacts**: Emergency service information
- **SafetyAlerts**: Public safety notifications

## Installation and Setup

1. Clone the repository
2. Install dependencies:

