from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.controllers import ministry_controller
from app.db.session import get_db
from app.schemas import ministry_schema
from app.auth.jwt import get_current_active_user, has_permission
from app.auth.permissions import Permissions
from app.models.employee import UserAccount

router = APIRouter()

@router.get("/", response_model=List[ministry_schema.Ministry])
def get_ministries(
  skip: int = 0,
  limit: int = 100,
  name: Optional[str] = None,
  db: Session = Depends(get_db),
  current_user: UserAccount = Depends(has_permission(Permissions.MINISTRY_READ))
):
  """
  Retrieve all ministries with optional filtering by name.
  """
  return ministry_controller.get_ministries(db, skip=skip, limit=limit, name=name)

@router.post("/", response_model=ministry_schema.Ministry, status_code=status.HTTP_201_CREATED)
def create_ministry(
  ministry: ministry_schema.MinistryCreate,
  db: Session = Depends(get_db),
  current_user: UserAccount = Depends(has_permission(Permissions.MINISTRY_CREATE))
):
  """
  Create a new ministry.
  """
  return ministry_controller.create_ministry(db, ministry=ministry)

@router.get("/{ministry_id}", response_model=ministry_schema.MinistryDetail)
def get_ministry(
  ministry_id: int,
  db: Session = Depends(get_db),
  current_user: UserAccount = Depends(has_permission(Permissions.MINISTRY_READ))
):
  """
  Get detailed information about a specific ministry.
  """
  db_ministry = ministry_controller.get_ministry(db, ministry_id=ministry_id)
  if db_ministry is None:
      raise HTTPException(status_code=404, detail="Ministry not found")
  return db_ministry

@router.put("/{ministry_id}", response_model=ministry_schema.Ministry)
def update_ministry(
  ministry_id: int,
  ministry: ministry_schema.MinistryUpdate,
  db: Session = Depends(get_db),
  current_user: UserAccount = Depends(has_permission(Permissions.MINISTRY_UPDATE))
):
  """
  Update a ministry.
  """
  db_ministry = ministry_controller.get_ministry(db, ministry_id=ministry_id)
  if db_ministry is None:
      raise HTTPException(status_code=404, detail="Ministry not found")
  return ministry_controller.update_ministry(db, ministry_id=ministry_id, ministry=ministry)

@router.delete("/{ministry_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ministry(
  ministry_id: int,
  db: Session = Depends(get_db),
  current_user: UserAccount = Depends(has_permission(Permissions.MINISTRY_DELETE))
):
  """
  Delete a ministry.
  """
  db_ministry = ministry_controller.get_ministry(db, ministry_id=ministry_id)
  if db_ministry is None:
      raise HTTPException(status_code=404, detail="Ministry not found")
  ministry_controller.delete_ministry(db, ministry_id=ministry_id)
  return None

@router.get("/{ministry_id}/departments", response_model=List[ministry_schema.Department])
def get_ministry_departments(
  ministry_id: int,
  db: Session = Depends(get_db),
  current_user: UserAccount = Depends(has_permission(Permissions.MINISTRY_READ))
):
  """
  Get all departments belonging to a specific ministry.
  """
  db_ministry = ministry_controller.get_ministry(db, ministry_id=ministry_id)
  if db_ministry is None:
      raise HTTPException(status_code=404, detail="Ministry not found")
  return ministry_controller.get_ministry_departments(db, ministry_id=ministry_id)

