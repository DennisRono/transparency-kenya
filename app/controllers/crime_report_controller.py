import os
import uuid
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from datetime import datetime
from fastapi import UploadFile, HTTPException
import aiofiles
from pathlib import Path

from app.models.crime_reporting import CrimeReport, MediaEvidence, WitnessStatement, ReportStatusUpdate
from app.schemas import crime_report_schema

# Create upload directory if it doesn't exist
UPLOAD_DIR = Path("uploads/evidence")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

async def get_crime_report(db: AsyncSession, report_id: int):
    query = select(CrimeReport).where(
        CrimeReport.id == report_id,
        CrimeReport.is_deleted == False
    )
    result = await db.execute(query)
    return result.scalar_one_or_none()

async def get_crime_reports(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    crime_type: Optional[str] = None,
    priority: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
):
    query = select(CrimeReport).where(CrimeReport.is_deleted == False)
    
    if status:
        query = query.where(CrimeReport.status == status)
    
    if crime_type:
        query = query.where(CrimeReport.crime_type == crime_type)
    
    if priority:
        query = query.where(CrimeReport.priority == priority)
    
    if start_date:
        start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
        query = query.where(CrimeReport.report_datetime >= start_datetime)
    
    if end_date:
        end_datetime = datetime.strptime(end_date, "%Y-%m-%d")
        query = query.where(CrimeReport.report_datetime <= end_datetime)
    
    query = query.order_by(CrimeReport.report_datetime.desc()).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

async def create_crime_report(db: AsyncSession, report: crime_report_schema.CrimeReportCreate):
    # Generate a unique report number
    report_number = f"CR-{uuid.uuid4().hex[:8].upper()}"
    
    db_report = CrimeReport(
        report_number=report_number,
        crime_type=report.crime_type,
        description=report.description,
        report_datetime=datetime.now(),
        incident_datetime=report.incident_datetime,
        location_description=report.location_description,
        latitude=report.latitude,
        longitude=report.longitude,
        status="submitted",
        priority=report.priority,
        reporter_name=report.reporter_name,
        reporter_contact=report.reporter_contact,
        reporter_email=report.reporter_email,
        reporter_id_number=report.reporter_id_number,
        anonymous=report.anonymous,
        suspects_description=report.suspects_description,
        victims_information=report.victims_information,
        emergency_services_needed=report.emergency_services_needed,
        emergency_services_details=report.emergency_services_details
    )
    
    db.add(db_report)
    await db.commit()
    await db.refresh(db_report)
    
    # Create initial status update
    status_update = ReportStatusUpdate(
        crime_report_id=db_report.id,
        status="submitted",
        update_datetime=datetime.now(),
        notes="Report submitted",
        public_note="Your report has been received and will be reviewed shortly.",
        notify_reporter=True,
        notification_sent=False,
        updated_by=1  # System user ID
    )
    
    db.add(status_update)
    await db.commit()
    
    return db_report

async def update_crime_report(db: AsyncSession, report_id: int, report: crime_report_schema.CrimeReportUpdate):
    db_report = await get_crime_report(db, report_id)
    
    # Update report attributes
    for key, value in report.dict(exclude_unset=True).items():
        setattr(db_report, key, value)
    
    await db.commit()
    await db.refresh(db_report)
    return db_report

async def delete_crime_report(db: AsyncSession, report_id: int):
    db_report = await get_crime_report(db, report_id)
    db_report.is_deleted = True
    db_report.deleted_at = datetime.now()
    await db.commit()
    return db_report

async def add_media_evidence(db: AsyncSession, report_id: int, file: UploadFile, description: Optional[str] = None):
    # Generate a unique evidence ID
    evidence_id = f"EV-{uuid.uuid4().hex[:8].upper()}"
    
    # Determine media type based on content type
    content_type = file.content_type
    if content_type.startswith("image/"):
        media_type = "image"
    elif content_type.startswith("video/"):
        media_type = "video"
    elif content_type.startswith("audio/"):
        media_type = "audio"
    elif content_type.startswith("application/"):
        media_type = "document"
    else:
        media_type = "other"
    
    # Create file path
    file_extension = os.path.splitext(file.filename)[1]
    file_name = f"{evidence_id}{file_extension}"
    file_path = UPLOAD_DIR / file_name
    
    # Save the file
    try:
        async with aiofiles.open(file_path, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)
            file_size = len(content) / 1024  # Size in KB
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not upload file: {str(e)}")
    
    # Create database record
    db_evidence = MediaEvidence(
        evidence_id=evidence_id,
        media_type=media_type,
        file_url=f"/uploads/evidence/{file_name}",
        file_name=file.filename,
        file_size_kb=file_size,
        mime_type=content_type,
        upload_datetime=datetime.now(),
        description=description,
        crime_report_id=report_id
    )
    
    db.add(db_evidence)
    await db.commit()
    await db.refresh(db_evidence)
    
    return db_evidence

async def add_witness_statement(db: AsyncSession, report_id: int, statement: crime_report_schema.WitnessStatementCreate):
    # Generate a unique statement ID
    statement_id = f"WS-{uuid.uuid4().hex[:8].upper()}"
    
    db_statement = WitnessStatement(
        statement_id=statement_id,
        statement_text=statement.statement_text,
        statement_datetime=datetime.now(),
        witness_name=statement.witness_name,
        witness_contact=statement.witness_contact,
        witness_email=statement.witness_email,
        witness_id_number=statement.witness_id_number,
        anonymous=statement.anonymous,
        verified=False,
        crime_report_id=report_id
    )
    
    db.add(db_statement)
    await db.commit()
    await db.refresh(db_statement)
    
    return db_statement

async def add_status_update(db: AsyncSession, report_id: int, status_update: crime_report_schema.StatusUpdateCreate):
    db_status_update = ReportStatusUpdate(
        crime_report_id=report_id,
        status=status_update.status,
        update_datetime=datetime.now(),
        notes=status_update.notes,
        public_note=status_update.public_note,
        notify_reporter=status_update.notify_reporter,
        notification_sent=False,
        updated_by=status_update.updated_by
    )
    
    db.add(db_status_update)
    
    # Update the report status
    db_report = await get_crime_report(db, report_id)
    db_report.status = status_update.status
    
    await db.commit()
    await db.refresh(db_status_update)
    
    return db_status_update

