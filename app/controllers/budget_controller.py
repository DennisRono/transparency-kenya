from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from datetime import datetime
from app.models.finance import Budget, Expenditure
from app.schemas import budget_schema

async def get_budget(db: AsyncSession, budget_id: int):
    query = select(Budget).where(Budget.id == budget_id, Budget.is_deleted == False)
    result = await db.execute(query)
    return result.scalar_one_or_none()

async def get_budgets(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
    fiscal_year: Optional[str] = None,
    ministry_id: Optional[int] = None,
    department_id: Optional[int] = None,
    status: Optional[str] = None
):
    query = select(Budget).where(Budget.is_deleted == False)
    
    if fiscal_year:
        query = query.where(Budget.fiscal_year == fiscal_year)
    
    if ministry_id:
        query = query.where(Budget.ministry_id == ministry_id)
    
    if department_id:
        query = query.where(Budget.department_id == department_id)
    
    if status:
        query = query.where(Budget.status == status)
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

async def create_budget(db: AsyncSession, budget: budget_schema.BudgetCreate):
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
    await db.commit()
    await db.refresh(db_budget)
    return db_budget

async def update_budget(db: AsyncSession, budget_id: int, budget: budget_schema.BudgetUpdate):
    db_budget = await get_budget(db, budget_id)
    
    # Update budget attributes
    for key, value in budget.dict(exclude_unset=True).items():
        setattr(db_budget, key, value)
    
    await db.commit()
    await db.refresh(db_budget)
    return db_budget

async def delete_budget(db: AsyncSession, budget_id: int):
    db_budget = await get_budget(db, budget_id)
    db_budget.is_deleted = True
    db_budget.deleted_at = datetime.now()
    await db.commit()
    return db_budget

async def get_budget_expenditures(db: AsyncSession, budget_id: int):
    query = select(Expenditure).where(
        Expenditure.budget_id == budget_id,
        Expenditure.is_deleted == False
    )
    result = await db.execute(query)
    return result.scalars().all()

