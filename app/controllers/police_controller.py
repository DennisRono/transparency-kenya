from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import datetime
import uuid

from app.models.police import PoliceOfficer
from app.models.public import Complaint
from app.schemas import police_schema

def get_police_officer(db: Session, officer_id: int):
    return db.query(PoliceOfficer).filter(
        PoliceOfficer.id == officer_id,
        PoliceOfficer.is_deleted == False
    ).first()

def get_police_officers(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    name: Optional[str] = None,
    rank: Optional[str] = None,
    station_id: Optional[int] = None
):
    query = db.query(PoliceOfficer).filter(PoliceOfficer.is_deleted == False)
    
    if name:
        query = query.filter(
            or_(
                PoliceOfficer.first_name.ilike(f"%{name}%"),
                PoliceOfficer.last_name.ilike(f"%{name}%")
            )
        )
    
    if rank:
        query = query.filter(PoliceOfficer.rank == rank)
    
    if station_id:
        query = query.filter(PoliceOfficer.station_id == station_id)
    
    return query.offset(skip).limit(limit).all()

def create_police_officer(db: Session, officer: police_schema.PoliceOfficerCreate):
    db_officer = PoliceOfficer(
        service_number=officer.service_number,
        rank=officer.rank,
        first_name=officer.first_name,
        middle_name=officer.middle_name,
        last_name=officer.last_name,
        gender=officer.gender,
        date_of_birth=officer.date_of_birth,
        national_id=officer.national_id,
        email=officer.email,
        phone_number=officer.phone_number,
        physical_address=officer.physical_address,
        date_of_enlistment=officer.date_of_enlistment,
        station_id=officer.station_id,
        department=officer.department,
        supervisor_id=officer.supervisor_id,
        status=officer.status
    )
    
    db.add(db_officer)
    db.commit()
    db.refresh(db_officer)
    return db_officer

def update_police_officer(db: Session, officer_id: int, officer: police_schema.PoliceOfficerUpdate):
    db_officer = get_police_officer(db, officer_id)
    
    # Update officer attributes
    for key, value in officer.dict(exclude_unset=True).items():
        setattr(db_officer, key, value)
    
    db.commit()
    db.refresh(db_officer)
    return db_officer

def delete_police_officer(db: Session, officer_id: int):
    db_officer = get_police_officer(db, officer_id)
    db_officer.is_deleted = True
    db_officer.deleted_at = datetime.now()
    db.commit()
    return db_officer

def get_police_complaint(db: Session, complaint_id: int):
    return db.query(Complaint).filter(
        Complaint.id == complaint_id,
        Complaint.is_deleted == False
    ).first()

def get_police_complaints(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    officer_id: Optional[int] = None
):
    query = db.query(Complaint).filter(Complaint.is_deleted == False)
    
    if status:
        query = query.filter(Complaint.status == status)
    
    if officer_id:
        query = query.filter(Complaint.officer_id == officer_id)
    
    return query.order_by(Complaint.submission_date.desc()).offset(skip).limit(limit).all()

def create_police_complaint(db: Session, complaint: police_schema.PoliceComplaintCreate):
    # Generate a unique reference number
    reference_number = f"PC-{uuid.uuid4().hex[:8].upper()}"
    
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
        incident_date=complaint.incident_date,
        location=complaint.location,
        officer_id=complaint.officer_id,
        witnesses=complaint.witnesses
    )
    
    db.add(db_complaint)
    db.commit()
    db.refresh(db_complaint)
    return db_complaint

def update_police_complaint(db: Session, complaint_id: int, complaint: police_schema.PoliceComplaintUpdate):
    db_complaint = get_police_complaint(db, complaint_id)
    
    # Update complaint attributes
    for key, value in complaint.dict(exclude_unset=True).items():
        setattr(db_complaint, key, value)
    
    # If assigned_to is updated, set assignment_date
    if complaint.assigned_to is not None:
        db_complaint.assignment_date = datetime.now()
    
    db.commit()
    db.refresh(db_complaint)
    return db_complaint

