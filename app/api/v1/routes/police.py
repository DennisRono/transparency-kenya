from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.controllers import police_controller
from app.schemas import police_schema

router = APIRouter()

@router.get("/officers", response_model=List[police_schema.PoliceOfficer])
def get_police_officers(
    skip: int = 0,
    limit: int = 100,
    name: Optional[str] = None,
    rank: Optional[str] = None,
    station_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    Retrieve all police officers with optional filtering.
    """
    return police_controller.get_police_officers(
        db, skip=skip, limit=limit, name=name, rank=rank, station_id=station_id
    )

@router.post("/officers", response_model=police_schema.PoliceOfficer, status_code=status.HTTP_201_CREATED)
def create_police_officer(
    officer: police_schema.PoliceOfficerCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new police officer.
    """
    return police_controller.create_police_officer(db, officer=officer)

@router.get("/officers/{officer_id}", response_model=police_schema.PoliceOfficerDetail)
def get_police_officer(
    officer_id: int,
    db: Session = Depends(get_db)
):
    """
    Get detailed information about a specific police officer.
    """
    db_officer = police_controller.get_police_officer(db, officer_id=officer_id)
    if db_officer is None:
        raise HTTPException(status_code=404, detail="Police officer not found")
    return db_officer

@router.put("/officers/{officer_id}", response_model=police_schema.PoliceOfficer)
def update_police_officer(
    officer_id: int,
    officer: police_schema.PoliceOfficerUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a police officer.
    """
    db_officer = police_controller.get_police_officer(db, officer_id=officer_id)
    if db_officer is None:
        raise HTTPException(status_code=404, detail="Police officer not found")
    return police_controller.update_police_officer(db, officer_id=officer_id, officer=officer)

@router.delete("/officers/{officer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_police_officer(
    officer_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a police officer (soft delete).
    """
    db_officer = police_controller.get_police_officer(db, officer_id=officer_id)
    if db_officer is None:
        raise HTTPException(status_code=404, detail="Police officer not found")
    police_controller.delete_police_officer(db, officer_id=officer_id)
    return None

@router.get("/complaints", response_model=List[police_schema.PoliceComplaint])
def get_police_complaints(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    officer_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    Retrieve all police complaints with optional filtering.
    """
    return police_controller.get_police_complaints(
        db, skip=skip, limit=limit, status=status, officer_id=officer_id
    )

@router.post("/complaints", response_model=police_schema.PoliceComplaint, status_code=status.HTTP_201_CREATED)
def create_police_complaint(
    complaint: police_schema.PoliceComplaintCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new police complaint.
    """
    return police_controller.create_police_complaint(db, complaint=complaint)

@router.get("/complaints/{complaint_id}", response_model=police_schema.PoliceComplaintDetail)
def get_police_complaint(
    complaint_id: int,
    db: Session = Depends(get_db)
):
    """
    Get detailed information about a specific police complaint.
    """
    db_complaint = police_controller.get_police_complaint(db, complaint_id=complaint_id)
    if db_complaint is None:
        raise HTTPException(status_code=404, detail="Police complaint not found")
    return db_complaint

