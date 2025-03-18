import json
from sqlalchemy.orm import Session
from datetime import datetime
import os
import sys
import logging

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import SessionLocal, engine, Base
from app.models.employee import Role, UserAccount, Employee, Position, MaritalStatus, Gender, EmploymentStatus
from app.auth.security import get_password_hash
from app.auth.permissions import ADMIN_PERMISSIONS, MANAGER_PERMISSIONS, OFFICER_PERMISSIONS, PUBLIC_PERMISSIONS
from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create tables
Base.metadata.create_all(bind=engine)

def init_db() -> None:
    """
    Initialize database with initial roles and admin user.
    """
    db = SessionLocal()
    try:
        # Create roles if they don't exist
        create_roles(db)
        
        # Create admin position if it doesn't exist
        admin_position = get_or_create_admin_position(db)
        
        # Create admin employee if it doesn't exist
        admin_employee = get_or_create_admin_employee(db, admin_position.id)
        
        # Create admin user if it doesn't exist
        get_or_create_admin_user(db, admin_employee.id)
        
        logger.info("Initial database setup completed successfully")
    except Exception as e:
        logger.error(f"Error during database initialization: {e}")
    finally:
        db.close()

def create_roles(db: Session) -> None:
    """
    Create default roles.
    """
    # Check if roles already exist
    if db.query(Role).count() > 0:
        logger.info("Roles already exist, skipping role creation")
        return
    
    # Create admin role
    admin_role = Role(
        name="Administrator",
        description="System administrator with full access to all functionality",
        permissions=json.dumps(ADMIN_PERMISSIONS),
        is_system_role=True,
        is_active=True
    )
    db.add(admin_role)
    
    # Create manager role
    manager_role = Role(
        name="Manager",
        description="Department or unit manager with access to manage their areas",
        permissions=json.dumps(MANAGER_PERMISSIONS),
        is_system_role=True,
        is_active=True
    )
    db.add(manager_role)
    
    # Create officer role
    officer_role = Role(
        name="Officer",
        description="Regular government officer with standard access",
        permissions=json.dumps(OFFICER_PERMISSIONS),
        is_system_role=True,
        is_active=True
    )
    db.add(officer_role)
    
    # Create public role
    public_role = Role(
        name="Public",
        description="Public user with limited access",
        permissions=json.dumps(PUBLIC_PERMISSIONS),
        is_system_role=True,
        is_active=True
    )
    db.add(public_role)
    
    db.commit()
    logger.info("Created default roles")

def get_or_create_admin_position(db: Session) -> Position:
    """
    Get or create the admin position.
    """
    # Check if position already exists
    admin_position = db.query(Position).filter(Position.code == "ADMIN").first()
    if admin_position:
        return admin_position
    
    # Create position
    admin_position = Position(
        title="System Administrator",
        code="ADMIN",
        description="System administrator with technical responsibilities",
        salary_grade="ADMIN-1",
        min_salary=100000,
        max_salary=200000,
        job_level=1,
        responsibilities="Manage the system and its users",
        qualifications_required="Technical expertise in system administration",
        experience_required="5+ years",
        skills_required="Technical and leadership skills",
        is_management=True,
        is_executive=True
    )
    db.add(admin_position)
    db.commit()
    db.refresh(admin_position)
    logger.info("Created admin position")
    return admin_position

def get_or_create_admin_employee(db: Session, position_id: int) -> Employee:
    """
    Get or create the admin employee.
    """
    # Check if employee already exists
    admin_employee = db.query(Employee).filter(Employee.employee_number == "ADMIN-001").first()
    if admin_employee:
        return admin_employee
    
    # Create employee
    admin_employee = Employee(
        first_name="System",
        last_name="Administrator",
        gender=Gender.OTHER,
        date_of_birth=datetime(1990, 1, 1),
        national_id="ADMIN-ID",
        tax_id="ADMIN-TAX",
        email="admin@example.com",
        phone_number="123456789",
        physical_address="System Address",
        marital_status=MaritalStatus.SINGLE,
        nationality="Kenyan",
        
        # Employment information
        employee_number="ADMIN-001",
        hire_date=datetime.now().date(),
        status=EmploymentStatus.ACTIVE,
        employment_type="Permanent",
        
        # Banking information
        bank_name="Admin Bank",
        bank_branch="Admin Branch",
        account_number="ADMIN-ACCOUNT",
        
        # Foreign keys
        position_id=position_id
    )
    db.add(admin_employee)
    db.commit()
    db.refresh(admin_employee)
    logger.info("Created admin employee")
    return admin_employee

def get_or_create_admin_user(db: Session, employee_id: int) -> UserAccount:
    """
    Get or create the admin user.
    """
    # Check if user already exists
    admin_user = db.query(UserAccount).filter(UserAccount.username == "admin").first()
    if admin_user:
        return admin_user
    
    # Get admin role
    admin_role = db.query(Role).filter(Role.name == "Administrator").first()
    if not admin_role:
        raise Exception("Admin role not found")
    
    # Create user
    hashed_password = get_password_hash("admin123") # Default password, should be changed
    admin_user = UserAccount(
        username="admin",
        email="admin@example.com",
        password_hash=hashed_password,
        is_active=True,
        is_locked=False,
        password_reset_required=True,
        failed_login_attempts=0,
        employee_id=employee_id,
        role_id=admin_role.id
    )
    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)
    logger.info("Created admin user with username 'admin' and password 'admin123'")
    logger.warning("PLEASE CHANGE THE DEFAULT ADMIN PASSWORD IMMEDIATELY!")
    return admin_user

if __name__ == "__main__":
    logger.info("Creating initial database data...")
    init_db()
    logger.info("Initial database data created successfully")

