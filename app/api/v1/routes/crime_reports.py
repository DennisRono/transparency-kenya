from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status, File, UploadFile
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.controllers import crime_report_controller
from app.schemas import crime_report_schema

router = APIRouter()

@router.get("/", response_model=List[crime_report_schema.CrimeReport])
def get_crime_reports(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    crime_type: Optional[str] = None,
    priority: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Retrieve all crime reports with optional filtering.
    """
    return crime_report_controller.get_crime_reports(
        db, skip=skip, limit=limit, status=status, crime_type=crime_type,
        priority=priority, start_date=start_date, end_date=end_date
    )

@router.post("/", response_model=crime_report_schema.CrimeReport, status_code=status.HTTP_201_CREATED)
def create_crime_report(
    report: crime_report_schema.CrimeReportCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new crime report.
    """
    return crime_report_controller.create_crime_report(db, report=report)

@router.get("/{report_id}", response_model=crime_report_schema.CrimeReportDetail)
def get_crime_report(
    report_id: int,
    db: Session = Depends(get_db)
):
    """
    Get detailed information about a specific crime report.
    """
    db_report = crime_report_controller.get_crime_report(db, report_id=report_id)
    if db_report is None:
        raise HTTPException(status_code=404, detail="Crime report not found")
    return db_report

@router.put("/{report_id}", response_model=crime_report_schema.CrimeReport)
def update_crime_report(
    report_id: int,
    report: crime_report_schema.CrimeReportUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a crime report.
    """
    db_report = crime_report_controller.get_crime_report(db, report_id=report_id)
    if db_report is None:
        raise HTTPException(status_code=404, detail="Crime report not found")
    return crime_report_controller.update_crime_report(db, report_id=report_id, report=report)

@router.delete("/{report_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_crime_report(
    report_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a crime report (soft delete).
    """
    db_report = crime_report_controller.get_crime_report(db, report_id=report_id)
    if db_report is None:
        raise HTTPException(status_code=404, detail="Crime report not found")
    crime_report_controller.delete_crime_report(db, report_id=report_id)
    return None

@router.post("/{report_id}/evidence", response_model=crime_report_schema.MediaEvidence)
async def upload_evidence(
    report_id: int,
    file: UploadFile = File(...),
    description: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Upload media evidence for a crime report.
    """
    db_report = crime_report_controller.get_crime_report(db, report_id=report_id)
    if db_report is None:
        raise HTTPException(status_code=404, detail="Crime report not found")
    
    return await crime_report_controller.add_media_evidence(db, report_id=report_id, file=file, description=description)

@router.post("/{report_id}/witness-statement", response_model=crime_report_schema.WitnessStatement)
def add_witness_statement(
    report_id: int,
    statement: crime_report_schema.WitnessStatementCreate,
    db: Session = Depends(get_db)
):
    """
    Add a witness statement to a crime report.
    """
    db_report = crime_report_controller.get_crime_report(db, report_id=report_id)
    if db_report is None:
        raise HTTPException(status_code=404, detail="Crime report not found")
    
    return crime_report_controller.add_witness_statement(db, report_id=report_id, statement=statement)

@router.post("/{report_id}/status-update", response_model=crime_report_schema.ReportStatusUpdate)
def update_report_status(
    report_id: int,
    status_update: crime_report_schema.StatusUpdateCreate,
    db: Session = Depends(get_db)
):
    """
    Add a status update to a crime report.
    """
    db_report = crime_report_controller.get_crime_report(db, report_id=report_id)
    if db_report is None:
        raise HTTPException(status_code=404, detail="Crime report not found")
    
    return crime_report_controller.add_status_update(db, report_id=report_id, status_update=status_update)

