from datetime import date, datetime
from enum import Enum
from typing import Optional, List, TYPE_CHECKING
import uuid
from sqlalchemy import String, ForeignKey, Text, Date, DateTime, Enum as SQLEnum, Integer, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

if TYPE_CHECKING:
    from app.models.employee import Employee

class PaymentStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"

class PaymentMethod(str, Enum):
    BANK_TRANSFER = "bank_transfer"
    MOBILE_MONEY = "mobile_money"
    CASH = "cash"
    CHEQUE = "cheque"
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    ELECTRONIC_FUNDS_TRANSFER = "electronic_funds_transfer"
    OTHER = "other"

class TransactionType(str, Enum):
    PAYMENT = "payment"
    REFUND = "refund"
    ADJUSTMENT = "adjustment"
    TRANSFER = "transfer"
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    FEE = "fee"
    INTEREST = "interest"
    TAX = "tax"
    OTHER = "other"

class Budget(Base):
    """Represents a budget for a department or project."""
    __tablename__ = "budgets"
    
    fiscal_year: Mapped[str] = mapped_column(String(10), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    total_amount: Mapped[float] = mapped_column(nullable=False)
    approved_amount: Mapped[float] = mapped_column(nullable=False)
    remaining_amount: Mapped[float] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)  # Draft, Submitted, Approved, Rejected, Active, Closed
    approval_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    approved_by: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Foreign keys
    prepared_by: Mapped[uuid.UUID] = mapped_column(ForeignKey("employees.id"), nullable=False)
    
    # Optional foreign keys for organizational placement
    ministry_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("ministries.id"), nullable=True)
    department_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("departments.id"), nullable=True)
    agency_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("agencies.id"), nullable=True)
    county_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("counties.id"), nullable=True)
    project_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("projects.id"), nullable=True)
    
    # Relationships
    preparer: Mapped["Employee"] = relationship(foreign_keys=[prepared_by])
    budget_items: Mapped[List["BudgetItem"]] = relationship(back_populates="budget", cascade="all, delete-orphan")
    expenditures: Mapped[List["Expenditure"]] = relationship(back_populates="budget")
    
    def __repr__(self) -> str:
        return f"<Budget(fiscal_year='{self.fiscal_year}', title='{self.title}', total_amount={self.total_amount})>"

class BudgetItem(Base):
    """Represents a line item in a budget."""
    __tablename__ = "budget_items"
    
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    subcategory: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    amount: Mapped[float] = mapped_column(nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    unit_cost: Mapped[float] = mapped_column(nullable=False)
    priority: Mapped[int] = mapped_column(Integer, nullable=False)  # 1 = highest priority
    justification: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Foreign keys
    budget_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("budgets.id"), nullable=False)
    
    # Relationships
    budget: Mapped["Budget"] = relationship(back_populates="budget_items")
    
    def __repr__(self) -> str:
        return f"<BudgetItem(category='{self.category}', description='{self.description}', amount={self.amount})>"

class Expenditure(Base):
    """Represents an expenditure against a budget."""
    __tablename__ = "expenditures"
    
    expenditure_number: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    expenditure_date: Mapped[date] = mapped_column(Date, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    amount: Mapped[float] = mapped_column(nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    subcategory: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    payment_method: Mapped[PaymentMethod] = mapped_column(SQLEnum(PaymentMethod), nullable=False)
    payment_reference: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    status: Mapped[PaymentStatus] = mapped_column(SQLEnum(PaymentStatus), nullable=False)
    vendor: Mapped[str] = mapped_column(String(255), nullable=False)
    vendor_contact: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    invoice_number: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    invoice_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    receipt_number: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Foreign keys
    budget_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("budgets.id"), nullable=False)
    requested_by: Mapped[uuid.UUID] = mapped_column(ForeignKey("employees.id"), nullable=False)
    approved_by: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("employees.id"), nullable=True)
    processed_by: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("employees.id"), nullable=True)
    
    # Relationships
    budget: Mapped["Budget"] = relationship(back_populates="expenditures")
    requester: Mapped["Employee"] = relationship(foreign_keys=[requested_by])
    approver: Mapped[Optional["Employee"]] = relationship(foreign_keys=[approved_by])
    processor: Mapped[Optional["Employee"]] = relationship(foreign_keys=[processed_by])
    
    def __repr__(self) -> str:
        return f"<Expenditure(expenditure_number='{self.expenditure_number}', amount={self.amount}, status='{self.status}')>"

class Salary(Base):
    """Represents an employee's salary information."""
    __tablename__ = "salaries"
    
    effective_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    basic_salary: Mapped[float] = mapped_column(nullable=False)
    gross_salary: Mapped[float] = mapped_column(nullable=False)
    net_salary: Mapped[float] = mapped_column(nullable=False)
    currency: Mapped[str] = mapped_column(String(10), nullable=False, default="KES")
    payment_frequency: Mapped[str] = mapped_column(String(50), nullable=False, default="Monthly")
    tax_deductions: Mapped[float] = mapped_column(nullable=False)
    pension_deductions: Mapped[float] = mapped_column(nullable=False)
    health_insurance_deductions: Mapped[float] = mapped_column(nullable=False)
    other_deductions: Mapped[float] = mapped_column(nullable=False, default=0)
    allowances: Mapped[float] = mapped_column(nullable=False, default=0)
    bonuses: Mapped[float] = mapped_column(nullable=False, default=0)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Foreign keys
    employee_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("employees.id"), nullable=False)
    approved_by: Mapped[uuid.UUID] = mapped_column(ForeignKey("employees.id"), nullable=False)
    
    # Relationships
    employee: Mapped["Employee"] = relationship(back_populates="salaries", foreign_keys=[employee_id])
    approver: Mapped["Employee"] = relationship(foreign_keys=[approved_by])
    
    def __repr__(self) -> str:
        return f"<Salary(employee_id={self.employee_id}, effective_date='{self.effective_date}', basic_salary={self.basic_salary})>"

class Payment(Base):
    """Represents a payment made to an employee or vendor."""
    __tablename__ = "payments"
    
    payment_number: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    payment_date: Mapped[date] = mapped_column(Date, nullable=False)
    amount: Mapped[float] = mapped_column(nullable=False)
    currency: Mapped[str] = mapped_column(String(10), nullable=False, default="KES")
    payment_method: Mapped[PaymentMethod] = mapped_column(SQLEnum(PaymentMethod), nullable=False)
    payment_reference: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[PaymentStatus] = mapped_column(SQLEnum(PaymentStatus), nullable=False)
    transaction_type: Mapped[TransactionType] = mapped_column(SQLEnum(TransactionType), nullable=False)
    payee_name: Mapped[str] = mapped_column(String(255), nullable=False)
    payee_account: Mapped[str] = mapped_column(String(100), nullable=False)
    payee_bank: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    payee_branch: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Foreign keys
    employee_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("employees.id"), nullable=True)
    approved_by: Mapped[uuid.UUID] = mapped_column(ForeignKey("employees.id"), nullable=False)
    processed_by: Mapped[uuid.UUID] = mapped_column(ForeignKey("employees.id"), nullable=False)
    
    # Relationships
    employee: Mapped[Optional["Employee"]] = relationship(foreign_keys=[employee_id])
    approver: Mapped["Employee"] = relationship(foreign_keys=[approved_by])
    processor: Mapped["Employee"] = relationship(foreign_keys=[processed_by])
    
    def __repr__(self) -> str:
        return f"<Payment(payment_number='{self.payment_number}', amount={self.amount}, status='{self.status}')>"

class FinancialReport(Base):
    """Represents a financial report."""
    __tablename__ = "financial_reports"
    
    report_number: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    report_type: Mapped[str] = mapped_column(String(100), nullable=False)  # Budget, Expenditure, Audit, etc.
    period_start: Mapped[date] = mapped_column(Date, nullable=False)
    period_end: Mapped[date] = mapped_column(Date, nullable=False)
    fiscal_year: Mapped[str] = mapped_column(String(10), nullable=False)
    generation_date: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)  # Draft, Submitted, Approved, Published
    content: Mapped[str] = mapped_column(Text, nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    recommendations: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    document_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Foreign keys
    prepared_by: Mapped[uuid.UUID] = mapped_column(ForeignKey("employees.id"), nullable=False)
    approved_by: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("employees.id"), nullable=True)
    
    # Optional foreign keys for organizational placement
    ministry_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("ministries.id"), nullable=True)
    department_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("departments.id"), nullable=True)
    agency_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("agencies.id"), nullable=True)
    county_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("counties.id"), nullable=True)
    
    # Relationships
    preparer: Mapped["Employee"] = relationship(foreign_keys=[prepared_by])
    approver: Mapped[Optional["Employee"]] = relationship(foreign_keys=[approved_by])
    
    def __repr__(self) -> str:
        return f"<FinancialReport(report_number='{self.report_number}', title='{self.title}', fiscal_year='{self.fiscal_year}')>"