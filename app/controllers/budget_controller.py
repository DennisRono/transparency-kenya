from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import datetime

from app.models.finance import Budget, Expenditure
from app.schemas import budget_schema

def get_budget(db: Session, budget_id: int):
    return db.query(Budget).filter(
        Budget.id == budget_id,
        Budget.is_deleted == False
    ).first()

def get_budgets(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    fiscal_year: Optional[str] = None,
    ministry_id: Optional[int] = None,
    department_id: Optional[int] = None,
    status: Optional[str] = None
):
    query = db.query(Budget).filter(Budget.is_deleted == False)
    
    if fiscal_year:
        query = query.filter(Budget.fiscal_year == fiscal_year)
    
    if ministry_id:
        query = query.filter(Budget.ministry_id == ministry_id)
    
    if department_id:
        query = query.filter(Budget.department_id == department_id)
    
    if status:
        query = query.filter(Budget.status == status)
    
    return query.offset(skip).limit(limit).all()

def create_budget(db: Session, budget: budget_schema.BudgetCreate):
    db_budget = Budget(
        fiscal_year=budget.fiscal_year,
        budget_type=budget.budget_type,
        amount=budget.amount,
        description=budget.description,
        start_date=budget.start_date,
        end_date=budget.end_date,
        status=budget.status,
        approved_amount=budget.approved_amount,
        approval_date=budget.approval_date,
        approved_by=budget.approved_by,
        rejection_reason=budget.rejection_reason,
        revision_number=budget.revision_number,
        previous_budget_id=budget.previous_budget_id,
        currency=budget.currency,
        ministry_id=budget.ministry_id,
        department_id=budget.department_id,
        agency_id=budget.agency_id,
        county_id=budget.county_id,
        sub_county_id=budget.sub_county_id,
        ward_id=budget.ward_id,
        project_id=budget.project_id,
        program_id=budget.program_id
    )
    
    db.add(db_budget)
    db.commit()
    db.refresh(db_budget)
    return db_budget

def update_budget(db: Session, budget_id: int, budget: budget_schema.BudgetUpdate):
    db_budget = get_budget(db, budget_id)
    
    # Update budget attributes
    for key, value in budget.dict(exclude_unset=True).items():
        setattr(db_budget, key, value)
    
    db.commit()
    db.refresh(db_budget)
    return db_budget

def delete_budget(db: Session, budget_id: int):
    db_budget = get_budget(db, budget_id)
    db_budget.is_deleted = True
    db_budget.deleted_at = datetime.now()
    db.commit()
    return db_budget

def get_budget_expenditures(db: Session, budget_id: int):
    return db.query(Expenditure).filter(
        Expenditure.budget_id == budget_id,
        Expenditure.is_deleted == False
    ).all()

