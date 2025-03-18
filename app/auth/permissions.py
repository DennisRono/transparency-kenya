class Permissions:
    # Employee permissions
    EMPLOYEE_CREATE = "employee:create"
    EMPLOYEE_READ = "employee:read"
    EMPLOYEE_UPDATE = "employee:update"
    EMPLOYEE_DELETE = "employee:delete"
    
    # Ministry permissions
    MINISTRY_CREATE = "ministry:create"
    MINISTRY_READ = "ministry:read"
    MINISTRY_UPDATE = "ministry:update"
    MINISTRY_DELETE = "ministry:delete"
    
    # Department permissions
    DEPARTMENT_CREATE = "department:create"
    DEPARTMENT_READ = "department:read"
    DEPARTMENT_UPDATE = "department:update"
    DEPARTMENT_DELETE = "department:delete"
    
    # Budget permissions
    BUDGET_CREATE = "budget:create"
    BUDGET_READ = "budget:read"
    BUDGET_UPDATE = "budget:update"
    BUDGET_DELETE = "budget:delete"
    BUDGET_APPROVE = "budget:approve"
    
    # Complaint permissions
    COMPLAINT_CREATE = "complaint:create"
    COMPLAINT_READ = "complaint:read"
    COMPLAINT_UPDATE = "complaint:update"
    COMPLAINT_DELETE = "complaint:delete"
    COMPLAINT_RESOLVE = "complaint:resolve"
    
    # Police permissions
    POLICE_CREATE = "police:create"
    POLICE_READ = "police:read"
    POLICE_UPDATE = "police:update"
    POLICE_DELETE = "police:delete"
    
    # Crime report permissions
    CRIME_REPORT_CREATE = "crime_report:create"
    CRIME_REPORT_READ = "crime_report:read"
    CRIME_REPORT_UPDATE = "crime_report:update"
    CRIME_REPORT_DELETE = "crime_report:delete"
    CRIME_REPORT_ASSIGN = "crime_report:assign"
    
    # User permissions
    USER_CREATE = "user:create"
    USER_READ = "user:read"
    USER_UPDATE = "user:update"
    USER_DELETE = "user:delete"
    
    # Role permissions
    ROLE_CREATE = "role:create"
    ROLE_READ = "role:read"
    ROLE_UPDATE = "role:update"
    ROLE_DELETE = "role:delete"

# Default permission sets for different roles
ADMIN_PERMISSIONS = [
    # Admin has all permissions
    Permissions.EMPLOYEE_CREATE, Permissions.EMPLOYEE_READ, Permissions.EMPLOYEE_UPDATE, Permissions.EMPLOYEE_DELETE,
    Permissions.MINISTRY_CREATE, Permissions.MINISTRY_READ, Permissions.MINISTRY_UPDATE, Permissions.MINISTRY_DELETE,
    Permissions.DEPARTMENT_CREATE, Permissions.DEPARTMENT_READ, Permissions.DEPARTMENT_UPDATE, Permissions.DEPARTMENT_DELETE,
    Permissions.BUDGET_CREATE, Permissions.BUDGET_READ, Permissions.BUDGET_UPDATE, Permissions.BUDGET_DELETE, Permissions.BUDGET_APPROVE,
    Permissions.COMPLAINT_CREATE, Permissions.COMPLAINT_READ, Permissions.COMPLAINT_UPDATE, Permissions.COMPLAINT_DELETE, Permissions.COMPLAINT_RESOLVE,
    Permissions.POLICE_CREATE, Permissions.POLICE_READ, Permissions.POLICE_UPDATE, Permissions.POLICE_DELETE,
    Permissions.CRIME_REPORT_CREATE, Permissions.CRIME_REPORT_READ, Permissions.CRIME_REPORT_UPDATE, Permissions.CRIME_REPORT_DELETE, Permissions.CRIME_REPORT_ASSIGN,
    Permissions.USER_CREATE, Permissions.USER_READ, Permissions.USER_UPDATE, Permissions.USER_DELETE,
    Permissions.ROLE_CREATE, Permissions.ROLE_READ, Permissions.ROLE_UPDATE, Permissions.ROLE_DELETE,
]

MANAGER_PERMISSIONS = [
    # Managers can read most things and manage their department
    Permissions.EMPLOYEE_READ, Permissions.EMPLOYEE_UPDATE,
    Permissions.MINISTRY_READ,
    Permissions.DEPARTMENT_READ, Permissions.DEPARTMENT_UPDATE,
    Permissions.BUDGET_READ, Permissions.BUDGET_CREATE, Permissions.BUDGET_UPDATE,
    Permissions.COMPLAINT_READ, Permissions.COMPLAINT_UPDATE, Permissions.COMPLAINT_RESOLVE,
    Permissions.POLICE_READ,
    Permissions.CRIME_REPORT_READ, Permissions.CRIME_REPORT_UPDATE,
    Permissions.USER_READ,
    Permissions.ROLE_READ,
]

OFFICER_PERMISSIONS = [
    # Regular officers have limited permissions
    Permissions.EMPLOYEE_READ,
    Permissions.MINISTRY_READ,
    Permissions.DEPARTMENT_READ,
    Permissions.BUDGET_READ,
    Permissions.COMPLAINT_READ, Permissions.COMPLAINT_CREATE, Permissions.COMPLAINT_UPDATE,
    Permissions.POLICE_READ,
    Permissions.CRIME_REPORT_READ, Permissions.CRIME_REPORT_CREATE, Permissions.CRIME_REPORT_UPDATE,
    Permissions.USER_READ,
]

PUBLIC_PERMISSIONS = [
    # Public users can only create complaints and crime reports and read limited info
    Permissions.COMPLAINT_CREATE, Permissions.COMPLAINT_READ,
    Permissions.CRIME_REPORT_CREATE, Permissions.CRIME_REPORT_READ,
    Permissions.MINISTRY_READ,
    Permissions.DEPARTMENT_READ,
]
