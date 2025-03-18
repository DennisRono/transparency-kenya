from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.controllers import complaint_controller
from app.schemas import complaint_schema

router = APIRouter()

@router.get("/", response_model=List[complaint_schema.Complaint])
def get_complaints(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    ministry_id: Optional[int] = None,
    department_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    Retrieve all complaints with optional filtering.
    """
    return complaint_controller.get_complaints(
        db, skip=skip, limit=limit, status=status, priority=priority,
        ministry_id=ministry_id, department_id=department_id
    )

@router.post("/", response_model=complaint_schema.Complaint, status_code=status.HTTP_201_CREATED)
def create_complaint(
    complaint: complaint_schema.ComplaintCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new complaint.
    """
    return complaint_controller.create_complaint(db, complaint=complaint)

@router.get("/{complaint_id}", response_model=complaint_schema.ComplaintDetail)
def get_complaint(
    complaint_id: int,
    db: Session = Depends(get_db)
):
    """
    Get detailed information about a specific complaint.
    """
    db_complaint = complaint_controller.get_complaint(db, complaint_id=complaint_id)
    if db_complaint is None:
        raise HTTPException(status_code=404, detail="Complaint not found")
    return db_complaint

@router.put("/{complaint_id}", response_model=complaint_schema.Complaint)
def update_complaint(
    complaint_id: int,
    complaint: complaint_schema.ComplaintUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a complaint.
    """
    db_complaint = complaint_controller.get_complaint(db, complaint_id=complaint_id)
    if db_complaint is None:
        raise HTTPException(status_code=404, detail="Complaint not found")
    return complaint_controller.update_complaint(db, complaint_id=complaint_id, complaint=complaint)

@router.delete("/{complaint_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_complaint(
    complaint_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a complaint (soft delete).
    """
    db_complaint = complaint_controller.get_complaint(db, complaint_id=complaint_id)
    if db_complaint is None:
        raise HTTPException(status_code=404, detail="Complaint not found")
    complaint_controller.delete_complaint(db, complaint_id=complaint_id)
    return None

@router.post("/{complaint_id}/assign", response_model=complaint_schema.Complaint)
def assign_complaint(
    complaint_id: int,
    assignment: complaint_schema.ComplaintAssignment,
    db: Session = Depends(get_db)
):
    """
    Assign a complaint to an employee.
    """
    db_complaint = complaint_controller.get_complaint(db, complaint_id=complaint_id)
    if db_complaint is None:
        raise HTTPException(status_code=404, detail="Complaint not found")
    return complaint_controller.assign_complaint(db, complaint_id=complaint_id, assignment=assignment)

