from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.controllers import budget_controller
from app.schemas import budget_schema

router = APIRouter()

@router.get("/", response_model=List[budget_schema.Budget])
def get_budgets(
    skip: int = 0,
    limit: int = 100,
    fiscal_year: Optional[str] = None,
    ministry_id: Optional[int] = None,
    department_id: Optional[int] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Retrieve all budgets with optional filtering.
    """
    return budget_controller.get_budgets(
        db, skip=skip, limit=limit, fiscal_year=fiscal_year,
        ministry_id=ministry_id, department_id=department_id, status=status
    )

@router.post("/", response_model=budget_schema.Budget, status_code=status.HTTP_201_CREATED)
def create_budget(
    budget: budget_schema.BudgetCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new budget.
    """
    return budget_controller.create_budget(db, budget=budget)

@router.get("/{budget_id}", response_model=budget_schema.BudgetDetail)
def get_budget(
    budget_id: int,
    db: Session = Depends(get_db)
):
    """
    Get detailed information about a specific budget.
    """
    db_budget = budget_controller.get_budget(db, budget_id=budget_id)
    if db_budget is None:
        raise HTTPException(status_code=404, detail="Budget not found")
    return db_budget

@router.put("/{budget_id}", response_model=budget_schema.Budget)
def update_budget(
    budget_id: int,
    budget: budget_schema.BudgetUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a budget.
    """
    db_budget = budget_controller.get_budget(db, budget_id=budget_id)
    if db_budget is None:
        raise HTTPException(status_code=404, detail="Budget not found")
    return budget_controller.update_budget(db, budget_id=budget_id, budget=budget)

@router.delete("/{budget_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_budget(
    budget_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a budget (soft delete).
    """
    db_budget = budget_controller.get_budget(db, budget_id=budget_id)
    if db_budget is None:
        raise HTTPException(status_code=404, detail="Budget not found")
    budget_controller.delete_budget(db, budget_id=budget_id)
    return None

@router.get("/{budget_id}/expenditures", response_model=List[budget_schema.Expenditure])
def get_budget_expenditures(
    budget_id: int,
    db: Session = Depends(get_db)
):
    """
    Get all expenditures for a specific budget.
    """
    db_budget = budget_controller.get_budget(db, budget_id=budget_id)
    if db_budget is None:
        raise HTTPException(status_code=404, detail="Budget not found")
    return budget_controller.get_budget_expenditures(db, budget_id=budget_id)

