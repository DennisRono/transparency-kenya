from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import datetime
import uuid

from app.models.public import Complaint
from app.schemas import complaint_schema

def get_complaint(db: Session, complaint_id: int):
    return db.query(Complaint).filter(
        Complaint.id == complaint_id,
        Complaint.is_deleted == False
    ).first()

def get_complaints(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    ministry_id: Optional[int] = None,
    department_id: Optional[int] = None
):
    query = db.query(Complaint).filter(Complaint.is_deleted == False)
    
    if status:
        query = query.filter(Complaint.status == status)
    
    if priority:
        query = query.filter(Complaint.priority == priority)
    
    if ministry_id:
        query = query.filter(Complaint.ministry_id == ministry_id)
    
    if department_id:
        query = query.filter(Complaint.department_id == department_id)
    
    return query.order_by(Complaint.submission_date.desc()).offset(skip).limit(limit).all()

def create_complaint(db: Session, complaint: complaint_schema.ComplaintCreate):
    # Generate a unique reference number
    reference_number = f"C-{uuid.uuid4().hex[:8].upper()}"
    
    db_complaint = Complaint(
        reference_number=reference_number,
        subject=complaint.subject,
        description=complaint.description,
        submission_date=datetime.now(),
        status="submitted",
        priority=complaint.priority,
        complainant_name=complaint.complainant_name,
        complainant_contact=complaint.complainant_contact,
        complainant_email=complaint.complainant_email,
        complainant_id_number=complaint.complainant_id_number,
        anonymous=complaint.anonymous,
        location=complaint.location,
        incident_date=complaint.incident_date
    )
    
    db.add(db_complaint)
    db.commit()
    db.refresh(db_complaint)
    return db_complaint

def update_complaint(db: Session, complaint_id: int, complaint: complaint_schema.ComplaintUpdate):
    db_complaint = get_complaint(db, complaint_id)
    
    # Update complaint attributes
    for key, value in complaint.dict(exclude_unset=True).items():
        setattr(db_complaint, key, value)
    
    # If status is set to resolved, set resolution_date
    if complaint.status == "resolved":
        db_complaint.resolution_date = datetime.now()
    
    db.commit()
    db.refresh(db_complaint)
    return db_complaint

def delete_complaint(db: Session, complaint_id: int):
    db_complaint = get_complaint(db, complaint_id)
    db_complaint.is_deleted = True
    db_complaint.deleted_at = datetime.now()
    db.commit()
    return db_complaint

def assign_complaint(db: Session, complaint_id: int, assignment: complaint_schema.ComplaintAssignment):
    db_complaint = get_complaint(db, complaint_id)
    
    db_complaint.assigned_to = assignment.assigned_to
    db_complaint.assignment_date = datetime.now()
    db_complaint.status = "under_review"
    
    db.commit()
    db.refresh(db_complaint)
    return db_complaint

