from datetime import date, datetime
from enum import Enum
from typing import Optional, List, TYPE_CHECKING
import uuid
from sqlalchemy import String, ForeignKey, Text, Date, Enum as SQLEnum, UniqueConstraint, Integer, Float, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

if TYPE_CHECKING:
    from app.models.employee import Employee, UserAccount

class TransactionType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"
    TRANSFER = "transfer"
    ADJUSTMENT = "adjustment"

class TransactionStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class Salary(Base):
    """Represents an employee's salary record."""
    __tablename__ = "salaries"
    __table_args__ = (
        UniqueConstraint('employee_id', 'effective_date', name='uq_employee_effective_date'),
    )
    
    amount: Mapped[float] = mapped_column(nullable=False)
    effective_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    reason_for_change: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    basic_salary: Mapped[float] = mapped_column(nullable=False)
    gross_salary: Mapped[float] = mapped_column(nullable=False)
    net_salary: Mapped[float] = mapped_column(nullable=False)
    tax_deduction: Mapped[float] = mapped_column(nullable=False)
    pension_deduction: Mapped[float] = mapped_column(nullable=False)
    health_insurance_deduction: Mapped[Optional[float]] = mapped_column(nullable=True)
    other_deductions: Mapped[Optional[float]] = mapped_column(nullable=True)
    allowances_total: Mapped[Optional[float]] = mapped_column(nullable=True)
    bonuses: Mapped[Optional[float]] = mapped_column(nullable=True)
    currency: Mapped[str] = mapped_column(String(10), nullable=False, default="KES")
    payment_method: Mapped[str] = mapped_column(String(50), nullable=False)
    bank_name: Mapped[str] = mapped_column(String(255), nullable=False)
    bank_account: Mapped[str] = mapped_column(String(50), nullable=False)
    payment_date: Mapped[date] = mapped_column(Date, nullable=False)
    payment_reference: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    # Foreign keys
    employee_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("employees.id"), nullable=False)
    approved_by: Mapped[Optional[int]] = mapped_column(ForeignKey("employees.id"), nullable=True)
    
    # Relationships
    employee: Mapped["Employee"] = relationship(back_populates="salaries", foreign_keys=[employee_id])
    approver: Mapped[Optional["Employee"]] = relationship(foreign_keys=[approved_by])
    
    def __repr__(self) -> str:
        return f"<Salary(employee_id={self.employee_id}, amount={self.amount}, effective_date='{self.effective_date}')>"


class BudgetType(str, Enum):
    OPERATIONAL = "operational"
    CAPITAL = "capital"
    DEVELOPMENT = "development"
    RECURRENT = "recurrent"
    SPECIAL = "special"


class BudgetStatus(str, Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    APPROVED = "approved"
    REJECTED = "rejected"
    REVISED = "revised"
    ACTIVE = "active"
    CLOSED = "closed"


class Budget(Base):
    """Represents a budget allocation for a specific entity and fiscal year."""
    __tablename__ = "budgets"
    
    fiscal_year: Mapped[str] = mapped_column(String(10), nullable=False)
    budget_type: Mapped[BudgetType] = mapped_column(SQLEnum(BudgetType), nullable=False)
    amount: Mapped[float] = mapped_column(nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[BudgetStatus] = mapped_column(SQLEnum(BudgetStatus), nullable=False, default=BudgetStatus.DRAFT)
    approved_amount: Mapped[Optional[float]] = mapped_column(nullable=True)
    approval_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    approved_by: Mapped[Optional[int]] = mapped_column(ForeignKey("employees.id"), nullable=True)
    rejection_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    revision_number: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    previous_budget_id: Mapped[Optional[int]] = mapped_column(ForeignKey("budgets.id"), nullable=True)
    currency: Mapped[str] = mapped_column(String(10), nullable=False, default="KES")
    
    # Optional foreign keys for organizational placement
    ministry_id: Mapped[Optional[int]] = mapped_column(ForeignKey("ministries.id"), nullable=True)
    department_id: Mapped[Optional[int]] = mapped_column(ForeignKey("departments.id"), nullable=True)
    agency_id: Mapped[Optional[int]] = mapped_column(ForeignKey("agencies.id"), nullable=True)
    county_id: Mapped[Optional[int]] = mapped_column(ForeignKey("counties.id"), nullable=True)
    sub_county_id: Mapped[Optional[int]] = mapped_column(ForeignKey("sub_counties.id"), nullable=True)
    ward_id: Mapped[Optional[int]] = mapped_column(ForeignKey("wards.id"), nullable=True)
    project_id: Mapped[Optional[int]] = mapped_column(ForeignKey("projects.id"), nullable=True)
    program_id: Mapped[Optional[int]] = mapped_column(ForeignKey("programs.id"), nullable=True)
    
    # Relationships
    expenditures: Mapped[List["Expenditure"]] = relationship(back_populates="budget", cascade="all, delete-orphan")
    previous_budget: Mapped[Optional["Budget"]] = relationship("Budget", remote_side=[id], foreign_keys=[previous_budget_id])
    approver: Mapped[Optional["Employee"]] = relationship(foreign_keys=[approved_by])
    
    def __repr__(self) -> str:
        return f"<Budget(fiscal_year='{self.fiscal_year}', amount={self.amount}, status='{self.status}')>"


class ExpenditureCategory(str, Enum):
    SALARIES = "salaries"
    OPERATIONS = "operations"
    MAINTENANCE = "maintenance"
    UTILITIES = "utilities"
    SUPPLIES = "supplies"
    EQUIPMENT = "equipment"
    TRAVEL = "travel"
    TRAINING = "training"
    CONSULTANCY = "consultancy"
    INFRASTRUCTURE = "infrastructure"
    OTHER = "other"


class ExpenditureStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    PAID = "paid"
    CANCELLED = "cancelled"


class Expenditure(Base):
    """Represents an expenditure against a budget."""
    __tablename__ = "expenditures"
    
    amount: Mapped[float] = mapped_column(nullable=False)
    expenditure_date: Mapped[date] = mapped_column(Date, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    receipt_number: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    category: Mapped[ExpenditureCategory] = mapped_column(SQLEnum(ExpenditureCategory), nullable=False)
    status: Mapped[ExpenditureStatus] = mapped_column(SQLEnum(ExpenditureStatus), nullable=False, default=ExpenditureStatus.PENDING)
    payment_method: Mapped[str] = mapped_column(String(50), nullable=False)
    payment_reference: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    payment_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    vendor_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    vendor_id: Mapped[Optional[int]] = mapped_column(ForeignKey("vendors.id"), nullable=True)
    invoice_number: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    invoice_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    tax_amount: Mapped[Optional[float]] = mapped_column(nullable=True)
    currency: Mapped[str] = mapped_column(String(10), nullable=False, default="KES")
    exchange_rate: Mapped[Optional[float]] = mapped_column(nullable=True)
    requested_by: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    approved_by: Mapped[Optional[int]] = mapped_column(ForeignKey("employees.id"), nullable=True)
    approval_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    rejection_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    supporting_documents: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON string of document URLs
    
    # Foreign keys
    budget_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("budgets.id"), nullable=False)
    
    # Optional foreign keys for organizational placement
    ministry_id: Mapped[Optional[int]] = mapped_column(ForeignKey("ministries.id"), nullable=True)
    department_id: Mapped[Optional[int]] = mapped_column(ForeignKey("departments.id"), nullable=True)
    agency_id: Mapped[Optional[int]] = mapped_column(ForeignKey("agencies.id"), nullable=True)
    county_id: Mapped[Optional[int]] = mapped_column(ForeignKey("counties.id"), nullable=True)
    sub_county_id: Mapped[Optional[int]] = mapped_column(ForeignKey("sub_counties.id"), nullable=True)
    ward_id: Mapped[Optional[int]] = mapped_column(ForeignKey("wards.id"), nullable=True)
    project_id: Mapped[Optional[int]] = mapped_column(ForeignKey("projects.id"), nullable=True)
    program_id: Mapped[Optional[int]] = mapped_column(ForeignKey("programs.id"), nullable=True)
    
    # Relationships
    budget: Mapped["Budget"] = relationship(back_populates="expenditures")
    transactions: Mapped[List["Transaction"]] = relationship(back_populates="expenditure", cascade="all, delete-orphan")
    requester: Mapped["Employee"] = relationship(foreign_keys=[requested_by])
    approver: Mapped[Optional["Employee"]] = relationship(foreign_keys=[approved_by])
    vendor: Mapped[Optional["Vendor"]] = relationship()
    
    def __repr__(self) -> str:
        return f"<Expenditure(amount={self.amount}, date='{self.date}', status='{self.status}')>"


class RevenueCategory(str, Enum):
    TAX = "tax"
    FEE = "fee"
    FINE = "fine"
    GRANT = "grant"
    DONATION = "donation"
    INVESTMENT = "investment"
    SALE = "sale"
    OTHER = "other"


class RevenueStatus(str, Enum):
    PENDING = "pending"
    RECEIVED = "received"
    VERIFIED = "verified"
    DEPOSITED = "deposited"
    CANCELLED = "cancelled"


class Revenue(Base):
    """Represents revenue collected by a government entity."""
    __tablename__ = "revenues"
    
    amount: Mapped[float] = mapped_column(nullable=False)
    revenue_date: Mapped[date] = mapped_column(Date, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    receipt_number: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    source: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[RevenueCategory] = mapped_column(SQLEnum(RevenueCategory), nullable=False)
    status: Mapped[RevenueStatus] = mapped_column(SQLEnum(RevenueStatus), nullable=False, default=RevenueStatus.PENDING)
    payment_method: Mapped[str] = mapped_column(String(50), nullable=False)
    payment_reference: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    payer_name: Mapped[str] = mapped_column(String(255), nullable=False)
    payer_contact: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    payer_id_number: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    currency: Mapped[str] = mapped_column(String(10), nullable=False, default="KES")
    exchange_rate: Mapped[Optional[float]] = mapped_column(nullable=True)
    collected_by: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    verified_by: Mapped[Optional[int]] = mapped_column(ForeignKey("employees.id"), nullable=True)
    verification_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    bank_deposit_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    bank_deposit_reference: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    bank_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    bank_account: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    supporting_documents: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON string of document URLs
    
    # Optional foreign keys for organizational placement
    ministry_id: Mapped[Optional[int]] = mapped_column(ForeignKey("ministries.id"), nullable=True)
    department_id: Mapped[Optional[int]] = mapped_column(ForeignKey("departments.id"), nullable=True)
    agency_id: Mapped[Optional[int]] = mapped_column(ForeignKey("agencies.id"), nullable=True)
    county_id: Mapped[Optional[int]] = mapped_column(ForeignKey("counties.id"), nullable=True)
    sub_county_id: Mapped[Optional[int]] = mapped_column(ForeignKey("sub_counties.id"), nullable=True)
    ward_id: Mapped[Optional[int]] = mapped_column(ForeignKey("wards.id"), nullable=True)
    
    # Relationships
    transactions: Mapped[List["Transaction"]] = relationship(back_populates="revenue", cascade="all, delete-orphan")
    collector: Mapped["Employee"] = relationship(foreign_keys=[collected_by])
    verifier: Mapped[Optional["Employee"]] = relationship(foreign_keys=[verified_by])
    
    def __repr__(self) -> str:
        return f"<Revenue(amount={self.amount}, date='{self.date}', receipt_number='{self.receipt_number}')>"


class Transaction(Base):
    """Represents a financial transaction in the system."""
    __tablename__ = "transactions"
    
    amount: Mapped[float] = mapped_column(nullable=False)
    transaction_date: Mapped[datetime] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    reference_number: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    transaction_type: Mapped[TransactionType] = mapped_column(SQLEnum(TransactionType), nullable=False)
    status: Mapped[TransactionStatus] = mapped_column(
        SQLEnum(TransactionStatus), 
        nullable=False, 
        default=TransactionStatus.PENDING
    )
    payment_method: Mapped[str] = mapped_column(String(50), nullable=False)
    currency: Mapped[str] = mapped_column(String(10), nullable=False, default="KES")
    exchange_rate: Mapped[Optional[float]] = mapped_column(nullable=True)
    bank_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    bank_account: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    initiated_by: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    approved_by: Mapped[Optional[int]] = mapped_column(ForeignKey("employees.id"), nullable=True)
    approval_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    rejection_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Optional foreign keys
    revenue_id: Mapped[Optional[int]] = mapped_column(ForeignKey("revenues.id"), nullable=True)
    expenditure_id: Mapped[Optional[int]] = mapped_column(ForeignKey("expenditures.id"), nullable=True)
    grant_id: Mapped[Optional[int]] = mapped_column(ForeignKey("grants.id"), nullable=True)
    donation_id: Mapped[Optional[int]] = mapped_column(ForeignKey("donations.id"), nullable=True)
    loan_id: Mapped[Optional[int]] = mapped_column(ForeignKey("loans.id"), nullable=True)
    debt_payment_id: Mapped[Optional[int]] = mapped_column(ForeignKey("debt_payments.id"), nullable=True)
    investment_id: Mapped[Optional[int]] = mapped_column(ForeignKey("investments.id"), nullable=True)
    tax_collection_id: Mapped[Optional[int]] = mapped_column(ForeignKey("tax_collections.id"), nullable=True)
    contract_payment_id: Mapped[Optional[int]] = mapped_column(ForeignKey("contract_payments.id"), nullable=True)
    
    # Relationships
    revenue: Mapped[Optional["Revenue"]] = relationship(back_populates="transactions")
    expenditure: Mapped[Optional["Expenditure"]] = relationship(back_populates="transactions")
    grant: Mapped[Optional["Grant"]] = relationship(back_populates="transactions")
    donation: Mapped[Optional["Donation"]] = relationship(back_populates="transactions")
    loan: Mapped[Optional["Loan"]] = relationship(back_populates="transactions")
    debt_payment: Mapped[Optional["DebtPayment"]] = relationship(back_populates="transactions")
    investment: Mapped[Optional["Investment"]] = relationship(back_populates="transactions")
    tax_collection: Mapped[Optional["TaxCollection"]] = relationship(back_populates="transactions")
    contract_payment: Mapped[Optional["ContractPayment"]] = relationship(back_populates="transactions")
    audits: Mapped[List["Audit"]] = relationship(back_populates="transaction", cascade="all, delete-orphan")
    initiator: Mapped["Employee"] = relationship(foreign_keys=[initiated_by])
    approver: Mapped[Optional["Employee"]] = relationship(foreign_keys=[approved_by])
    
    def __repr__(self) -> str:
        return f"<Transaction(amount={self.amount}, reference_number='{self.reference_number}', type='{self.transaction_type}')>"


class Audit(Base):
    """Represents an audit record for financial transactions."""
    __tablename__ = "audits"
    
    action: Mapped[str] = mapped_column(String(50), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(nullable=False, default=func.now())
    details: Mapped[str] = mapped_column(Text, nullable=False)
    ip_address: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    user_agent: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Foreign keys
    transaction_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("transactions.id"), nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    
    # Relationships
    transaction: Mapped["Transaction"] = relationship(back_populates="audits")
    user: Mapped["UserAccount"] = relationship()
    
    def __repr__(self) -> str:
        return f"<Audit(action='{self.action}', transaction_id={self.transaction_id})>"


class GrantType(str, Enum):
    GOVERNMENT = "government"
    INTERNATIONAL = "international"
    NGO = "ngo"
    PRIVATE = "private"
    OTHER = "other"


class GrantStatus(str, Enum):
    APPLIED = "applied"
    APPROVED = "approved"
    REJECTED = "rejected"
    RECEIVED = "received"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Grant(Base):
    """Represents a grant received by a government entity."""
    __tablename__ = "grants"
    
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    grant_type: Mapped[GrantType] = mapped_column(SQLEnum(GrantType), nullable=False)
    donor: Mapped[str] = mapped_column(String(255), nullable=False)
    donor_contact: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    amount: Mapped[float] = mapped_column(nullable=False)
    currency: Mapped[str] = mapped_column(String(10), nullable=False, default="KES")
    exchange_rate: Mapped[Optional[float]] = mapped_column(nullable=True)
    application_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    approval_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[GrantStatus] = mapped_column(SQLEnum(GrantStatus), nullable=False)
    purpose: Mapped[str] = mapped_column(Text, nullable=False)
    conditions: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    reporting_requirements: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    disbursement_schedule: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    amount_received: Mapped[Optional[float]] = mapped_column(nullable=True)
    amount_spent: Mapped[Optional[float]] = mapped_column(nullable=True)
    amount_remaining: Mapped[Optional[float]] = mapped_column(nullable=True)
    last_report_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    next_report_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    grant_manager: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    
    # Optional foreign keys for organizational placement
    ministry_id: Mapped[Optional[int]] = mapped_column(ForeignKey("ministries.id"), nullable=True)
    department_id: Mapped[Optional[int]] = mapped_column(ForeignKey("departments.id"), nullable=True)
    agency_id: Mapped[Optional[int]] = mapped_column(ForeignKey("agencies.id"), nullable=True)
    county_id: Mapped[Optional[int]] = mapped_column(ForeignKey("counties.id"), nullable=True)
    project_id: Mapped[Optional[int]] = mapped_column(ForeignKey("projects.id"), nullable=True)
    program_id: Mapped[Optional[int]] = mapped_column(ForeignKey("programs.id"), nullable=True)
    
    # Relationships
    transactions: Mapped[List["Transaction"]] = relationship(back_populates="grant")
    manager: Mapped["Employee"] = relationship(foreign_keys=[grant_manager])
    
    def __repr__(self) -> str:
        return f"<Grant(title='{self.title}', amount={self.amount}, status='{self.status}')>"


class DonationType(str, Enum):
    CASH = "cash"
    GOODS = "goods"
    SERVICES = "services"
    LAND = "land"
    BUILDING = "building"
    EQUIPMENT = "equipment"
    OTHER = "other"


class DonationStatus(str, Enum):
    PLEDGED = "pledged"
    RECEIVED = "received"
    VERIFIED = "verified"
    REJECTED = "rejected"
    RETURNED = "returned"


class Donation(Base):
    """Represents a donation received by a government entity."""
    __tablename__ = "donations"
    
    description: Mapped[str] = mapped_column(Text, nullable=False)
    donation_type: Mapped[DonationType] = mapped_column(SQLEnum(DonationType), nullable=False)
    donor_name: Mapped[str] = mapped_column(String(255), nullable=False)
    donor_contact: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    donor_address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    amount: Mapped[Optional[float]] = mapped_column(nullable=True)  # For cash donations
    currency: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    exchange_rate: Mapped[Optional[float]] = mapped_column(nullable=True)
    item_description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # For non-cash donations
    estimated_value: Mapped[Optional[float]] = mapped_column(nullable=True)  # For non-cash donations
    quantity: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # For non-cash donations
    donation_date: Mapped[date] = mapped_column(Date, nullable=False)
    receipt_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    receipt_number: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    status: Mapped[DonationStatus] = mapped_column(SQLEnum(DonationStatus), nullable=False)
    purpose: Mapped[str] = mapped_column(Text, nullable=False)
    conditions: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    anonymous: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    tax_deductible: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    tax_receipt_issued: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    tax_receipt_number: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    tax_receipt_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    received_by: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    verified_by: Mapped[Optional[int]] = mapped_column(ForeignKey("employees.id"), nullable=True)
    verification_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    rejection_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Optional foreign keys for organizational placement
    ministry_id: Mapped[Optional[int]] = mapped_column(ForeignKey("ministries.id"), nullable=True)
    department_id: Mapped[Optional[int]] = mapped_column(ForeignKey("departments.id"), nullable=True)
    agency_id: Mapped[Optional[int]] = mapped_column(ForeignKey("agencies.id"), nullable=True)
    county_id: Mapped[Optional[int]] = mapped_column(ForeignKey("counties.id"), nullable=True)
    project_id: Mapped[Optional[int]] = mapped_column(ForeignKey("projects.id"), nullable=True)
    program_id: Mapped[Optional[int]] = mapped_column(ForeignKey("programs.id"), nullable=True)
    
    # Relationships
    transactions: Mapped[List["Transaction"]] = relationship(back_populates="donation")
    receiver: Mapped["Employee"] = relationship(foreign_keys=[received_by])
    verifier: Mapped[Optional["Employee"]] = relationship(foreign_keys=[verified_by])
    
    def __repr__(self) -> str:
        return f"<Donation(donor='{self.donor_name}', type='{self.donation_type}', status='{self.status}')>"


class LoanType(str, Enum):
    GOVERNMENT = "government"
    COMMERCIAL = "commercial"
    CONCESSIONAL = "concessional"
    BILATERAL = "bilateral"
    MULTILATERAL = "multilateral"
    BOND = "bond"
    OTHER = "other"


class LoanStatus(str, Enum):
    APPLIED = "applied"
    APPROVED = "approved"
    REJECTED = "rejected"
    DISBURSED = "disbursed"
    ACTIVE = "active"
    COMPLETED = "completed"
    DEFAULTED = "defaulted"
    RESTRUCTURED = "restructured"


class Loan(Base):
    """Represents a loan taken by a government entity."""
    __tablename__ = "loans"
    
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    loan_type: Mapped[LoanType] = mapped_column(SQLEnum(LoanType), nullable=False)
    lender: Mapped[str] = mapped_column(String(255), nullable=False)
    lender_contact: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    amount: Mapped[float] = mapped_column(nullable=False)
    currency: Mapped[str] = mapped_column(String(10), nullable=False, default="KES")
    exchange_rate: Mapped[Optional[float]] = mapped_column(nullable=True)
    interest_rate: Mapped[float] = mapped_column(nullable=False)
    interest_type: Mapped[str] = mapped_column(String(50), nullable=False)  # Fixed, Variable, etc.
    application_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    approval_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    disbursement_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    maturity_date: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[LoanStatus] = mapped_column(SQLEnum(LoanStatus), nullable=False)
    purpose: Mapped[str] = mapped_column(Text, nullable=False)
    conditions: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    collateral: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    guarantor: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    repayment_schedule: Mapped[str] = mapped_column(Text, nullable=False)
    repayment_frequency: Mapped[str] = mapped_column(String(50), nullable=False)  # Monthly, Quarterly, etc.
    grace_period_months: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    total_repayment_amount: Mapped[Optional[float]] = mapped_column(nullable=True)
    amount_disbursed: Mapped[Optional[float]] = mapped_column(nullable=True)
    amount_repaid: Mapped[Optional[float]] = mapped_column(nullable=True)
    amount_outstanding: Mapped[Optional[float]] = mapped_column(nullable=True)
    next_payment_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    next_payment_amount: Mapped[Optional[float]] = mapped_column(nullable=True)
    loan_manager: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    
    # Optional foreign keys for organizational placement
    ministry_id: Mapped[Optional[int]] = mapped_column(ForeignKey("ministries.id"), nullable=True)
    department_id: Mapped[Optional[int]] = mapped_column(ForeignKey("departments.id"), nullable=True)
    agency_id: Mapped[Optional[int]] = mapped_column(ForeignKey("agencies.id"), nullable=True)
    county_id: Mapped[Optional[int]] = mapped_column(ForeignKey("counties.id"), nullable=True)
    project_id: Mapped[Optional[int]] = mapped_column(ForeignKey("projects.id"), nullable=True)
    program_id: Mapped[Optional[int]] = mapped_column(ForeignKey("programs.id"), nullable=True)
    
    # Relationships
    transactions: Mapped[List["Transaction"]] = relationship(back_populates="loan")
    debt_payments: Mapped[List["DebtPayment"]] = relationship(back_populates="loan")
    manager: Mapped["Employee"] = relationship(foreign_keys=[loan_manager])
    
    def __repr__(self) -> str:
        return f"<Loan(title='{self.title}', amount={self.amount}, status='{self.status}')>"


class DebtPaymentStatus(str, Enum):
    SCHEDULED = "scheduled"
    PENDING = "pending"
    PAID = "paid"
    LATE = "late"
    DEFAULTED = "defaulted"
    WAIVED = "waived"


class DebtPayment(Base):
    """Represents a payment made against a loan."""
    __tablename__ = "debt_payments"
    
    payment_date: Mapped[date] = mapped_column(Date, nullable=False)
    amount: Mapped[float] = mapped_column(nullable=False)
    principal_amount: Mapped[float] = mapped_column(nullable=False)
    interest_amount: Mapped[float] = mapped_column(nullable=False)
    penalties: Mapped[Optional[float]] = mapped_column(nullable=True)
    currency: Mapped[str] = mapped_column(String(10), nullable=False, default="KES")
    exchange_rate: Mapped[Optional[float]] = mapped_column(nullable=True)
    payment_method: Mapped[str] = mapped_column(String(50), nullable=False)
    payment_reference: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[DebtPaymentStatus] = mapped_column(SQLEnum(DebtPaymentStatus), nullable=False)
    due_date: Mapped[date] = mapped_column(Date, nullable=False)
    payment_number: Mapped[int] = mapped_column(Integer, nullable=False)  # e.g., 1st payment, 2nd payment, etc.
    total_payments: Mapped[int] = mapped_column(Integer, nullable=False)  # Total number of payments scheduled
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Foreign keys
    loan_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("loans.id"), nullable=False)
    paid_by: Mapped[Optional[int]] = mapped_column(ForeignKey("employees.id"), nullable=True)
    
    # Relationships
    loan: Mapped["Loan"] = relationship(back_populates="debt_payments")
    transactions: Mapped[List["Transaction"]] = relationship(back_populates="debt_payment")
    payer: Mapped[Optional["Employee"]] = relationship(foreign_keys=[paid_by])
    
    def __repr__(self) -> str:
        return f"<DebtPayment(loan_id={self.loan_id}, payment_number={self.payment_number}, amount={self.amount}, status='{self.status}')>"


class InvestmentType(str, Enum):
    FIXED_DEPOSIT = "fixed_deposit"
    TREASURY_BILL = "treasury_bill"
    TREASURY_BOND = "treasury_bond"
    EQUITY = "equity"
    MUTUAL_FUND = "mutual_fund"
    REAL_ESTATE = "real_estate"
    OTHER = "other"


class InvestmentStatus(str, Enum):
    PLANNED = "planned"
    ACTIVE = "active"
    MATURED = "matured"
    LIQUIDATED = "liquidated"
    DEFAULTED = "defaulted"


class Investment(Base):
    """Represents an investment made by a government entity."""
    __tablename__ = "investments"
    
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    investment_type: Mapped[InvestmentType] = mapped_column(SQLEnum(InvestmentType), nullable=False)
    institution: Mapped[str] = mapped_column(String(255), nullable=False)
    institution_contact: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    amount: Mapped[float] = mapped_column(nullable=False)
    currency: Mapped[str] = mapped_column(String(10), nullable=False, default="KES")
    exchange_rate: Mapped[Optional[float]] = mapped_column(nullable=True)
    interest_rate: Mapped[Optional[float]] = mapped_column(nullable=True)
    expected_return: Mapped[Optional[float]] = mapped_column(nullable=True)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    maturity_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    status: Mapped[InvestmentStatus] = mapped_column(SQLEnum(InvestmentStatus), nullable=False)
    purpose: Mapped[str] = mapped_column(Text, nullable=False)
    risk_level: Mapped[str] = mapped_column(String(50), nullable=False)  # Low, Medium, High
    terms_and_conditions: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    certificate_number: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    account_number: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    returns_received: Mapped[Optional[float]] = mapped_column(nullable=True)
    current_value: Mapped[Optional[float]] = mapped_column(nullable=True)
    last_valuation_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    investment_manager: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    
    # Optional foreign keys for organizational placement
    ministry_id: Mapped[Optional[int]] = mapped_column(ForeignKey("ministries.id"), nullable=True)
    department_id: Mapped[Optional[int]] = mapped_column(ForeignKey("departments.id"), nullable=True)
    agency_id: Mapped[Optional[int]] = mapped_column(ForeignKey("agencies.id"), nullable=True)
    county_id: Mapped[Optional[int]] = mapped_column(ForeignKey("counties.id"), nullable=True)
    
    # Relationships
    transactions: Mapped[List["Transaction"]] = relationship(back_populates="investment")
    manager: Mapped["Employee"] = relationship(foreign_keys=[investment_manager])
    
    def __repr__(self) -> str:
        return f"<Investment(title='{self.title}', amount={self.amount}, status='{self.status}')>"


class TaxType(str, Enum):
    INCOME = "income"
    PROPERTY = "property"
    SALES = "sales"
    VALUE_ADDED = "value_added"
    EXCISE = "excise"
    IMPORT = "import"
    EXPORT = "export"
    CAPITAL_GAINS = "capital_gains"
    OTHER = "other"


class TaxCollection(Base):
    """Represents a tax collection record."""
    __tablename__ = "tax_collections"
    
    tax_type: Mapped[TaxType] = mapped_column(SQLEnum(TaxType), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    taxpayer_name: Mapped[str] = mapped_column(String(255), nullable=False)
    taxpayer_id: Mapped[str] = mapped_column(String(50), nullable=False)
    taxpayer_contact: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    amount: Mapped[float] = mapped_column(nullable=False)
    currency: Mapped[str] = mapped_column(String(10), nullable=False, default="KES")
    exchange_rate: Mapped[Optional[float]] = mapped_column(nullable=True)
    tax_period_start: Mapped[date] = mapped_column(Date, nullable=False)
    tax_period_end: Mapped[date] = mapped_column(Date, nullable=False)
    due_date: Mapped[date] = mapped_column(Date, nullable=False)
    payment_date: Mapped[date] = mapped_column(Date, nullable=False)
    receipt_number: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    payment_method: Mapped[str] = mapped_column(String(50), nullable=False)
    payment_reference: Mapped[str] = mapped_column(String(100), nullable=False)
    penalties: Mapped[Optional[float]] = mapped_column(nullable=True)
    interest: Mapped[Optional[float]] = mapped_column(nullable=True)
    total_amount: Mapped[float] = mapped_column(nullable=False)
    collected_by: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    verified_by: Mapped[Optional[int]] = mapped_column(ForeignKey("employees.id"), nullable=True)
    verification_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    
    # Optional foreign keys for organizational placement
    ministry_id: Mapped[Optional[int]] = mapped_column(ForeignKey("ministries.id"), nullable=True)
    department_id: Mapped[Optional[int]] = mapped_column(ForeignKey("departments.id"), nullable=True)
    agency_id: Mapped[Optional[int]] = mapped_column(ForeignKey("agencies.id"), nullable=True)
    county_id: Mapped[Optional[int]] = mapped_column(ForeignKey("counties.id"), nullable=True)
    
    # Relationships
    transactions: Mapped[List["Transaction"]] = relationship(back_populates="tax_collection")
    collector: Mapped["Employee"] = relationship(foreign_keys=[collected_by])
    verifier: Mapped[Optional["Employee"]] = relationship(foreign_keys=[verified_by])
    
    def __repr__(self) -> str:
        return f"<TaxCollection(taxpayer='{self.taxpayer_name}', amount={self.amount}, tax_type='{self.tax_type}')>"


class AssetCategory(Base):
    """Represents a category of assets."""
    __tablename__ = "asset_categories"
    
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    depreciation_rate: Mapped[Optional[float]] = mapped_column(nullable=True)
    useful_life_years: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    parent_category_id: Mapped[Optional[int]] = mapped_column(ForeignKey("asset_categories.id"), nullable=True)
    
    # Relationships
    parent_category: Mapped[Optional["AssetCategory"]] = relationship("AssetCategory", remote_side=[id], backref="subcategories")
    assets: Mapped[List["Asset"]] = relationship(back_populates="category")
    
    def __repr__(self) -> str:
        return f"<AssetCategory(name='{self.name}')>"


class AssetStatus(str, Enum):
    NEW = "new"
    IN_USE = "in_use"
    UNDER_MAINTENANCE = "under_maintenance"
    DAMAGED = "damaged"
    OBSOLETE = "obsolete"
    DISPOSED = "disposed"
    LOST = "lost"
    STOLEN = "stolen"


class Asset(Base):
    """Represents an asset owned by the government."""
    __tablename__ = "assets"
    
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    asset_number: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    acquisition_date: Mapped[date] = mapped_column(Date, nullable=False)
    acquisition_cost: Mapped[float] = mapped_column(nullable=False)
    currency: Mapped[str] = mapped_column(String(10), nullable=False, default="KES")
    exchange_rate: Mapped[Optional[float]] = mapped_column(nullable=True)
    current_value: Mapped[float] = mapped_column(nullable=False)
    depreciation_method: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    depreciation_rate: Mapped[Optional[float]] = mapped_column(nullable=True)
    useful_life_years: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    salvage_value: Mapped[Optional[float]] = mapped_column(nullable=True)
    status: Mapped[AssetStatus] = mapped_column(SQLEnum(AssetStatus), nullable=False)
    location: Mapped[str] = mapped_column(String(255), nullable=False)
    gps_coordinates: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    custodian: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    manufacturer: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    model: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    serial_number: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    warranty_expiry: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    maintenance_schedule: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    last_maintenance_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    next_maintenance_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    insurance_policy_number: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    insurance_expiry: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    disposal_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    disposal_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    disposal_amount: Mapped[Optional[float]] = mapped_column(nullable=True)
    disposal_method: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    disposal_authorized_by: Mapped[Optional[int]] = mapped_column(ForeignKey("employees.id"), nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Foreign keys
    category_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("asset_categories.id"), nullable=False)
    
    # Optional foreign keys for organizational placement
    ministry_id: Mapped[Optional[int]] = mapped_column(ForeignKey("ministries.id"), nullable=True)
    department_id: Mapped[Optional[int]] = mapped_column(ForeignKey("departments.id"), nullable=True)
    agency_id: Mapped[Optional[int]] = mapped_column(ForeignKey("agencies.id"), nullable=True)
    county_id: Mapped[Optional[int]] = mapped_column(ForeignKey("counties.id"), nullable=True)
    sub_county_id: Mapped[Optional[int]] = mapped_column(ForeignKey("sub_counties.id"), nullable=True)
    ward_id: Mapped[Optional[int]] = mapped_column(ForeignKey("wards.id"), nullable=True)
    
    # Relationships
    category: Mapped["AssetCategory"] = relationship(back_populates="assets")
    asset_movements: Mapped[List["AssetMovement"]] = relationship(back_populates="asset", cascade="all, delete-orphan")
    asset_maintenances: Mapped[List["AssetMaintenance"]] = relationship(back_populates="asset", cascade="all, delete-orphan")
    custodian_employee: Mapped["Employee"] = relationship(foreign_keys=[custodian])
    disposal_authorizer: Mapped[Optional["Employee"]] = relationship(foreign_keys=[disposal_authorized_by])
    
    def __repr__(self) -> str:
        return f"<Asset(name='{self.name}', asset_number='{self.asset_number}', status='{self.status}')>"


class AssetMovementType(str, Enum):
    ASSIGNMENT = "assignment"
    TRANSFER = "transfer"
    LOAN = "loan"
    RETURN = "return"
    DISPOSAL = "disposal"
    OTHER = "other"


class AssetMovement(Base):
    """Represents a movement or transfer of an asset."""
    __tablename__ = "asset_movements"
    
    movement_type: Mapped[AssetMovementType] = mapped_column(SQLEnum(AssetMovementType), nullable=False)
    movement_date: Mapped[date] = mapped_column(Date, nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    from_location: Mapped[str] = mapped_column(String(255), nullable=False)
    to_location: Mapped[str] = mapped_column(String(255), nullable=False)
    from_custodian: Mapped[Optional[int]] = mapped_column(ForeignKey("employees.id"), nullable=True)
    to_custodian: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    authorized_by: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    authorization_date: Mapped[date] = mapped_column(Date, nullable=False)
    expected_return_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)  # For loans
    actual_return_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)  # For loans
    condition_before: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    condition_after: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Foreign keys
    asset_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("assets.id"), nullable=False)
    
    # Relationships
    asset: Mapped["Asset"] = relationship(back_populates="asset_movements")
    previous_custodian: Mapped[Optional["Employee"]] = relationship(foreign_keys=[from_custodian])
    new_custodian: Mapped["Employee"] = relationship(foreign_keys=[to_custodian])
    authorizer: Mapped["Employee"] = relationship(foreign_keys=[authorized_by])
    
    def __repr__(self) -> str:
        return f"<AssetMovement(asset_id={self.asset_id}, type='{self.movement_type}', date='{self.movement_date}')>"


class MaintenanceType(str, Enum):
    PREVENTIVE = "preventive"
    CORRECTIVE = "corrective"
    PREDICTIVE = "predictive"
    EMERGENCY = "emergency"
    UPGRADE = "upgrade"
    INSPECTION = "inspection"
    OTHER = "other"


class MaintenanceStatus(str, Enum):
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    DEFERRED = "deferred"


class AssetMaintenance(Base):
    """Represents maintenance performed on an asset."""
    __tablename__ = "asset_maintenances"
    
    maintenance_type: Mapped[MaintenanceType] = mapped_column(SQLEnum(MaintenanceType), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    scheduled_date: Mapped[date] = mapped_column(Date, nullable=False)
    start_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    completion_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    status: Mapped[MaintenanceStatus] = mapped_column(SQLEnum(MaintenanceStatus), nullable=False)
    cost: Mapped[Optional[float]] = mapped_column(nullable=True)
    currency: Mapped[Optional[str]] = mapped_column(String(10), nullable=True, default="KES")
    exchange_rate: Mapped[Optional[float]] = mapped_column(nullable=True)
    performed_by: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)  # External service provider or internal
    vendor_id: Mapped[Optional[int]] = mapped_column(ForeignKey("vendors.id"), nullable=True)
    invoice_number: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    invoice_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    warranty_applied: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    parts_replaced: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    condition_before: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    condition_after: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    requested_by: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    approved_by: Mapped[Optional[int]] = mapped_column(ForeignKey("employees.id"), nullable=True)
    verified_by: Mapped[Optional[int]] = mapped_column(ForeignKey("employees.id"), nullable=True)
    
    # Foreign keys
    asset_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("assets.id"), nullable=False)
    
    # Relationships
    asset: Mapped["Asset"] = relationship(back_populates="asset_maintenances")
    vendor: Mapped[Optional["Vendor"]] = relationship()
    requester: Mapped["Employee"] = relationship(foreign_keys=[requested_by])
    approver: Mapped[Optional["Employee"]] = relationship(foreign_keys=[approved_by])
    verifier: Mapped[Optional["Employee"]] = relationship(foreign_keys=[verified_by])
    
    def __repr__(self) -> str:
        return f"<AssetMaintenance(asset_id={self.asset_id}, type='{self.maintenance_type}', status='{self.status}')>"


class ProcurementType(str, Enum):
    GOODS = "goods"
    SERVICES = "services"
    WORKS = "works"
    CONSULTANCY = "consultancy"
    OTHER = "other"


class ProcurementMethod(str, Enum):
    OPEN_TENDER = "open_tender"
    RESTRICTED_TENDER = "restricted_tender"
    DIRECT_PROCUREMENT = "direct_procurement"
    REQUEST_FOR_QUOTATION = "request_for_quotation"
    REQUEST_FOR_PROPOSAL = "request_for_proposal"
    FRAMEWORK_AGREEMENT = "framework_agreement"
    OTHER = "other"


class ProcurementStatus(str, Enum):
    PLANNED = "planned"
    APPROVED = "approved"
    TENDERING = "tendering"
    EVALUATION = "evaluation"
    AWARDED = "awarded"
    CONTRACTED = "contracted"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Procurement(Base):
    """Represents a procurement process."""
    __tablename__ = "procurements"
    
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    reference_number: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    procurement_type: Mapped[ProcurementType] = mapped_column(SQLEnum(ProcurementType), nullable=False)
    procurement_method: Mapped[ProcurementMethod] = mapped_column(SQLEnum(ProcurementMethod), nullable=False)
    justification: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    estimated_cost: Mapped[float] = mapped_column(nullable=False)
    currency: Mapped[str] = mapped_column(String(10), nullable=False, default="KES")
    exchange_rate: Mapped[Optional[float]] = mapped_column(nullable=True)
    budget_line: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    budget_confirmation: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    status: Mapped[ProcurementStatus] = mapped_column(SQLEnum(ProcurementStatus), nullable=False)
    initiated_date: Mapped[date] = mapped_column(Date, nullable=False)
    approval_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    tender_notice_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    tender_closing_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    evaluation_start_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    evaluation_end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    award_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    contract_signing_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    completion_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    number_of_bidders: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    winning_bidder: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    winning_bid_amount: Mapped[Optional[float]] = mapped_column(nullable=True)
    contract_amount: Mapped[Optional[float]] = mapped_column(nullable=True)
    initiated_by: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    approved_by: Mapped[Optional[int]] = mapped_column(ForeignKey("employees.id"), nullable=True)
    evaluation_committee: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON string of committee members
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Optional foreign keys for organizational placement
    ministry_id: Mapped[Optional[int]] = mapped_column(ForeignKey("ministries.id"), nullable=True)
    department_id: Mapped[Optional[int]] = mapped_column(ForeignKey("departments.id"), nullable=True)
    agency_id: Mapped[Optional[int]] = mapped_column(ForeignKey("agencies.id"), nullable=True)
    county_id: Mapped[Optional[int]] = mapped_column(ForeignKey("counties.id"), nullable=True)
    project_id: Mapped[Optional[int]] = mapped_column(ForeignKey("projects.id"), nullable=True)
    program_id: Mapped[Optional[int]] = mapped_column(ForeignKey("programs.id"), nullable=True)
    
    # Relationships
    contracts: Mapped[List["Contract"]] = relationship(back_populates="procurement", cascade="all, delete-orphan")
    initiator: Mapped["Employee"] = relationship(foreign_keys=[initiated_by])
    approver: Mapped[Optional["Employee"]] = relationship(foreign_keys=[approved_by])
    
    def __repr__(self) -> str:
        return f"<Procurement(title='{self.title}', reference='{self.reference_number}', status='{self.status}')>"


class ContractType(str, Enum):
    GOODS = "goods"
    SERVICES = "services"
    WORKS = "works"
    CONSULTANCY = "consultancy"
    LEASE = "lease"
    FRAMEWORK = "framework"
    OTHER = "other"


class ContractStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    COMPLETED = "completed"
    TERMINATED = "terminated"
    EXPIRED = "expired"
    DISPUTED = "disputed"
    AMENDED = "amended"


class Contract(Base):
    """Represents a contract with a vendor or supplier."""
    __tablename__ = "contracts"
    
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    contract_number: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    contract_type: Mapped[ContractType] = mapped_column(SQLEnum(ContractType), nullable=False)
    status: Mapped[ContractStatus] = mapped_column(SQLEnum(ContractStatus), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    extension_option: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    extension_terms: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    value: Mapped[float] = mapped_column(nullable=False)
    currency: Mapped[str] = mapped_column(String(10), nullable=False, default="KES")
    exchange_rate: Mapped[Optional[float]] = mapped_column(nullable=True)
    payment_terms: Mapped[str] = mapped_column(Text, nullable=False)
    performance_metrics: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    penalties: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    termination_clause: Mapped[str] = mapped_column(Text, nullable=False)
    dispute_resolution: Mapped[str] = mapped_column(Text, nullable=False)
    confidentiality_clause: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    intellectual_property_clause: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    insurance_requirements: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    warranty_period_days: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    signed_date: Mapped[date] = mapped_column(Date, nullable=False)
    signed_by_government: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    signed_by_vendor: Mapped[str] = mapped_column(String(255), nullable=False)
    witness: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    amount_paid: Mapped[Optional[float]] = mapped_column(nullable=True)
    amount_remaining: Mapped[Optional[float]] = mapped_column(nullable=True)
    last_payment_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    next_payment_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    next_payment_amount: Mapped[Optional[float]] = mapped_column(nullable=True)
    completion_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    termination_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    termination_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    amendments: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON string of amendments
    
    # Foreign keys
    vendor_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("vendors.id"), nullable=False)
    procurement_id: Mapped[Optional[int]] = mapped_column(ForeignKey("procurements.id"), nullable=True)
    
    # Optional foreign keys for organizational placement
    ministry_id: Mapped[Optional[int]] = mapped_column(ForeignKey("ministries.id"), nullable=True)
    department_id: Mapped[Optional[int]] = mapped_column(ForeignKey("departments.id"), nullable=True)
    agency_id: Mapped[Optional[int]] = mapped_column(ForeignKey("agencies.id"), nullable=True)
    county_id: Mapped[Optional[int]] = mapped_column(ForeignKey("counties.id"), nullable=True)
    project_id: Mapped[Optional[int]] = mapped_column(ForeignKey("projects.id"), nullable=True)
    program_id: Mapped[Optional[int]] = mapped_column(ForeignKey("programs.id"), nullable=True)
    
    # Relationships
    vendor: Mapped["Vendor"] = relationship()
    procurement: Mapped[Optional["Procurement"]] = relationship(back_populates="contracts")
    contract_payments: Mapped[List["ContractPayment"]] = relationship(back_populates="contract", cascade="all, delete-orphan")
    government_signatory: Mapped["Employee"] = relationship(foreign_keys=[signed_by_government])
    
    def __repr__(self) -> str:
        return f"<Contract(title='{self.title}', contract_number='{self.contract_number}', status='{self.status}')>"


class PaymentStatus(str, Enum):
    SCHEDULED = "scheduled"
    PENDING = "pending"
    APPROVED = "approved"
    PAID = "paid"
    REJECTED = "rejected"
    CANCELLED = "cancelled"


class ContractPayment(Base):
    """Represents a payment made against a contract."""
    __tablename__ = "contract_payments"
    
    payment_number: Mapped[int] = mapped_column(Integer, nullable=False)  # e.g., 1st payment, 2nd payment, etc.
    description: Mapped[str] = mapped_column(Text, nullable=False)
    amount: Mapped[float] = mapped_column(nullable=False)
    currency: Mapped[str] = mapped_column(String(10), nullable=False, default="KES")
    exchange_rate: Mapped[Optional[float]] = mapped_column(nullable=True)
    due_date: Mapped[date] = mapped_column(Date, nullable=False)
    payment_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    status: Mapped[PaymentStatus] = mapped_column(SQLEnum(PaymentStatus), nullable=False)
    payment_method: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    payment_reference: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    invoice_number: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    invoice_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    tax_amount: Mapped[Optional[float]] = mapped_column(nullable=True)
    withholding_tax: Mapped[Optional[float]] = mapped_column(nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    requested_by: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    approved_by: Mapped[Optional[int]] = mapped_column(ForeignKey("employees.id"), nullable=True)
    approval_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    paid_by: Mapped[Optional[int]] = mapped_column(ForeignKey("employees.id"), nullable=True)
    
    # Foreign keys
    contract_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("contracts.id"), nullable=False)
    
    # Relationships
    contract: Mapped["Contract"] = relationship(back_populates="contract_payments")
    transactions: Mapped[List["Transaction"]] = relationship(back_populates="contract_payment")
    requester: Mapped["Employee"] = relationship(foreign_keys=[requested_by])
    approver: Mapped[Optional["Employee"]] = relationship(foreign_keys=[approved_by])
    payer: Mapped[Optional["Employee"]] = relationship(foreign_keys=[paid_by])
    
    def __repr__(self) -> str:
        return f"<ContractPayment(contract_id={self.contract_id}, payment_number={self.payment_number}, amount={self.amount}, status='{self.status}')>"


class VendorCategory(str, Enum):
    GOODS = "goods"
    SERVICES = "services"
    WORKS = "works"
    CONSULTANCY = "consultancy"
    GENERAL = "general"
    OTHER = "other"


class VendorStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    BLACKLISTED = "blacklisted"
    SUSPENDED = "suspended"
    PENDING_APPROVAL = "pending_approval"


class Vendor(Base):
    """Represents a vendor or supplier."""
    __tablename__ = "vendors"
    
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    registration_number: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    vendor_category: Mapped[VendorCategory] = mapped_column(SQLEnum(VendorCategory), nullable=False)
    status: Mapped[VendorStatus] = mapped_column(SQLEnum(VendorStatus), nullable=False, default=VendorStatus.ACTIVE)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    address: Mapped[str] = mapped_column(Text, nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    country: Mapped[str] = mapped_column(String(100), nullable=False)
    postal_code: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    phone_number: Mapped[str] = mapped_column(String(50), nullable=False)
    alternative_phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    website: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    contact_person: Mapped[str] = mapped_column(String(255), nullable=False)
    contact_person_position: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    contact_person_phone: Mapped[str] = mapped_column(String(50), nullable=False)
    contact_person_email: Mapped[str] = mapped_column(String(255), nullable=False)
    tax_id: Mapped[str] = mapped_column(String(50), nullable=False)
    tax_compliance_certificate: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    tax_compliance_expiry: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    registration_date: Mapped[date] = mapped_column(Date, nullable=False)
    bank_name: Mapped[str] = mapped_column(String(255), nullable=False)
    bank_branch: Mapped[str] = mapped_column(String(255), nullable=False)
    bank_account: Mapped[str] = mapped_column(String(50), nullable=False)
    bank_code: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    swift_code: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    blacklisting_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    blacklisting_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    suspension_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    suspension_start_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    suspension_end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    performance_rating: Mapped[Optional[float]] = mapped_column(nullable=True)  # 1-5 scale
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    def __repr__(self) -> str:
        return f"<Vendor(name='{self.name}', registration_number='{self.registration_number}', status='{self.status}')>"


class InvoiceStatus(str, Enum):
    DRAFT = "draft"
    ISSUED = "issued"
    APPROVED = "approved"
    PAID = "paid"
    PARTIALLY_PAID = "partially_paid"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"
    DISPUTED = "disputed"


class Invoice(Base):
    """Represents an invoice from a vendor."""
    __tablename__ = "invoices"
    
    invoice_number: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    invoice_date: Mapped[date] = mapped_column(Date, nullable=False)
    due_date: Mapped[date] = mapped_column(Date, nullable=False)
    amount: Mapped[float] = mapped_column(nullable=False)
    tax_amount: Mapped[Optional[float]] = mapped_column(nullable=True)
    total_amount: Mapped[float] = mapped_column(nullable=False)
    currency: Mapped[str] = mapped_column(String(10), nullable=False, default="KES")
    exchange_rate: Mapped[Optional[float]] = mapped_column(nullable=True)
    status: Mapped[InvoiceStatus] = mapped_column(SQLEnum(InvoiceStatus), nullable=False)
    payment_terms: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    received_date: Mapped[date] = mapped_column(Date, nullable=False)
    received_by: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    approved_by: Mapped[Optional[int]] = mapped_column(ForeignKey("employees.id"), nullable=True)
    approval_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    payment_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    payment_reference: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    amount_paid: Mapped[Optional[float]] = mapped_column(nullable=True)
    dispute_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    dispute_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    dispute_resolved_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    
    # Foreign keys
    vendor_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("vendors.id"), nullable=False)
    contract_id: Mapped[Optional[int]] = mapped_column(ForeignKey("contracts.id"), nullable=True)
    
    # Optional foreign keys for organizational placement
    ministry_id: Mapped[Optional[int]] = mapped_column(ForeignKey("ministries.id"), nullable=True)
    department_id: Mapped[Optional[int]] = mapped_column(ForeignKey("departments.id"), nullable=True)
    agency_id: Mapped[Optional[int]] = mapped_column(ForeignKey("agencies.id"), nullable=True)
    county_id: Mapped[Optional[int]] = mapped_column(ForeignKey("counties.id"), nullable=True)
    project_id: Mapped[Optional[int]] = mapped_column(ForeignKey("projects.id"), nullable=True)
    program_id: Mapped[Optional[int]] = mapped_column(ForeignKey("programs.id"), nullable=True)
    
    # Relationships
    vendor: Mapped["Vendor"] = relationship()
    contract: Mapped[Optional["Contract"]] = relationship()
    receiver: Mapped["Employee"] = relationship(foreign_keys=[received_by])
    approver: Mapped[Optional["Employee"]] = relationship(foreign_keys=[approved_by])
    
    def __repr__(self) -> str:
        return f"<Invoice(invoice_number='{self.invoice_number}', amount={self.amount}, status='{self.status}')>"

