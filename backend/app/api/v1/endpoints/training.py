import uuid
import io
from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.session import get_db
from app.models.training import ORTrainingSession, ORTrainingAttendee
from app.models.project import Project
from app.models.partner import Partner
from app.schemas.training import (
    ORTrainingSession as ORTrainingSessionSchema,
    ORTrainingSessionCreate,
    ORTrainingAttendeeCreate,
    ORTrainingAttendee as ORTrainingAttendeeSchema,
    ORTrainingSessionDetail
)
from app.api.v1.endpoints.login import get_current_user
from app.models.auth import User

# For PDF generation
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.units import inch

router = APIRouter()

@router.post("/", response_model=ORTrainingSessionSchema)
async def create_training_session(
    session_in: ORTrainingSessionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Calculate expiry (24 hours from now)
    expires_at = datetime.utcnow() + timedelta(hours=24)
    
    db_obj = ORTrainingSession(
        **session_in.dict(),
        expires_at=expires_at,
        created_by=current_user.user_id
    )
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj

@router.get("/session/{session_id}")
async def get_public_session_status(
    session_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    """Public endpoint to check if session is active/expired."""
    stmt = select(ORTrainingSession).where(ORTrainingSession.session_id == session_id).options(
        selectinload(ORTrainingSession.project).selectinload(Project.partner)
    )
    result = await db.execute(stmt)
    db_session = result.scalar_one_or_none()
    
    if not db_session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    now = datetime.utcnow()
    is_expired = now > db_session.expires_at.replace(tzinfo=None)
    
    return {
        "session_id": db_session.session_id,
        "topic": db_session.topic,
        "partner_name": db_session.project.partner.name,
        "is_active": db_session.is_active and not is_expired,
        "expires_at": db_session.expires_at
    }

@router.post("/submit", status_code=status.HTTP_201_CREATED)
async def submit_attendance(
    attendee_in: ORTrainingAttendeeCreate,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    # 1. Check session
    stmt = select(ORTrainingSession).where(ORTrainingSession.session_id == attendee_in.session_id)
    result = await db.execute(stmt)
    db_session = result.scalar_one_or_none()
    
    if not db_session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    now = datetime.utcnow()
    if now > db_session.expires_at.replace(tzinfo=None) or not db_session.is_active:
        raise HTTPException(status_code=400, detail="Attendance link has expired (24h limit)")

    # 2. Hard validation: Check if device_id + session_id already exists
    if attendee_in.device_id:
        dup_stmt = select(ORTrainingAttendee).where(
            ORTrainingAttendee.session_id == attendee_in.session_id,
            ORTrainingAttendee.device_id == attendee_in.device_id
        )
        dup_res = await db.execute(dup_stmt)
        if dup_res.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="You have already submitted your attendance for this session.")

    # 3. Soft validation: Same name in same session
    name_stmt = select(ORTrainingAttendee).where(
        ORTrainingAttendee.session_id == attendee_in.session_id,
        func.lower(ORTrainingAttendee.fullname) == attendee_in.fullname.lower().strip()
    )
    name_res = await db.execute(name_stmt)
    if name_res.scalar_one_or_none():
         raise HTTPException(status_code=400, detail="An entry with this name already exists for this session.")

    # 4. Create attendee
    db_obj = ORTrainingAttendee(
        **attendee_in.dict(),
        ip_address=request.client.host
    )
    db.add(db_obj)
    await db.commit()
    return {"message": "Attendance submitted successfully"}

@router.get("/list/{project_id}", response_model=List[ORTrainingSessionSchema])
async def get_project_training_sessions(
    project_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    stmt = select(ORTrainingSession).where(ORTrainingSession.project_id == project_id).order_by(ORTrainingSession.created_at.desc())
    result = await db.execute(stmt)
    return result.scalars().all()

@router.get("/export/{session_id}")
async def export_training_pdf(
    session_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 1. Fetch Session Data
    stmt = select(ORTrainingSession).where(ORTrainingSession.session_id == session_id).options(
        selectinload(ORTrainingSession.project).selectinload(Project.partner),
        selectinload(ORTrainingSession.attendees)
    )
    result = await db.execute(stmt)
    db_session = result.scalar_one_or_none()
    
    if not db_session:
        raise HTTPException(status_code=404, detail="Session not found")

    # 2. Generate PDF
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=20, bottomMargin=30)
    elements = []
    styles = getSampleStyleSheet()
    
    # Custom Styles
    title_style = ParagraphStyle(
        'TitleStyle', parent=styles['Heading1'],
        fontSize=14, alignment=1, spaceAfter=15, textColor=colors.black
    )
    header_address_style = ParagraphStyle(
        'HeaderAddress', parent=styles['Normal'],
        fontSize=8, alignment=2, textColor=colors.grey, leading=10
    )

    # --- Corporate Header ---
    logo_path = "/app/app/assets/logo_pdf.png"
    try:
        logo = Image(logo_path, width=2.0*inch, height=0.6*inch)
    except Exception as e:
        print(f"Error loading logo: {e}")
        logo = Paragraph("<b>Power Pro</b>", styles['Normal'])

    company_info = [
        [logo, Paragraph(
            "<b>P.T. Infotek Jaya Makmur</b><br/>"
            "Jl. Gading Kirana Utara, Blok F10/No. 20-21<br/>"
            "Kelapa Gading Barat, Kelapa Gading<br/>"
            "Jakarta Utara - 14240<br/>"
            "WA : 0877 0050 7017 | Ph : 021 450 7017",
            header_address_style
        )]
    ]
    header_corp_table = Table(company_info, colWidths=[2.5*inch, 4.8*inch])
    header_corp_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))
    elements.append(header_corp_table)
    elements.append(Spacer(1, 10))
    # -----------------------

    # Adjust time to WIB (UTC+7)
    created_at_wib = db_session.created_at + timedelta(hours=7)
    now_wib = datetime.utcnow() + timedelta(hours=7)

    # Header Section (Matching Docx)
    elements.append(Paragraph("<b>POWERFO MODULE TRAINING - LIST OF TRAINING PARTICIPANTS</b>", title_style))
    elements.append(Spacer(1, 5))

    # Function for Page Numbering and Footer
    def draw_footer(canvas, doc):
        canvas.saveState()
        # Footer Timestamp
        footer_text = f"Printed on: {now_wib.strftime('%d/%m/%Y %H:%M:%S')} WIB"
        canvas.setFont('Helvetica', 8)
        canvas.drawString(inch, 0.5 * inch, footer_text)
        # Page Number
        page_num = f"Page {doc.page} of {doc.page}" # Simple version, reportlab needs a trick for total pages
        # Actually, let's just do Page X
        canvas.drawRightString(7.5 * inch, 0.5 * inch, f"Page {doc.page}")
        canvas.restoreState()

    # Header Data Table
    # Note: Page numbering in header is tricky with SimpleDocTemplate, 
    # so I'll put it in the footer or use a fixed placeholder for now.
    header_data = [
        [Paragraph(f"<b>Project</b>: {db_session.project.name}", styles['Normal']), Paragraph(f"<b>Page</b>: 1 of 1", styles['Normal'])],
        [Paragraph(f"<b>Venue</b>: {db_session.project.partner.name}", styles['Normal']), Paragraph(f"<b>Dept.</b>: {db_session.project.partner.area_id or '-'}", styles['Normal'])],
        [Paragraph(f"<b>Date</b>: {created_at_wib.strftime('%d %b %Y')}", styles['Normal']), Paragraph(f"<b>Module</b>: PowerFO", styles['Normal'])],
        [Paragraph(f"<b>Time</b>: {created_at_wib.strftime('%H:%M')} to { (created_at_wib + timedelta(hours=2)).strftime('%H:%M') } WIB", styles['Normal']), Paragraph(f"<b>Trainer</b>: {db_session.trainer_name or '-'}", styles['Normal'])]
    ]
    
    header_table = Table(header_data, colWidths=[380, 150])
    header_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
    ]))
    elements.append(header_table)
    elements.append(Spacer(1, 15))

    # Instruction
    instr_style = ParagraphStyle('InstrStyle', parent=styles['Normal'], fontSize=8, alignment=1, fontName='Helvetica-Oblique')
    elements.append(Paragraph("Please fill in with CAPITAL letter / mohon diisi dengan huruf CETAK", instr_style))
    elements.append(Spacer(1, 10))
    
    # Attendees Table (Matching Docx)
    data = [["No", "Full Name", "Position", "Signature"]]
    
    sorted_attendees = sorted(db_session.attendees, key=lambda x: x.created_at)
    for i, att in enumerate(sorted_attendees, 1):
        data.append([
            str(i),
            att.fullname.upper(),
            att.position or "-",
            f"{att.created_at.strftime('%H:%M')}"
        ])
    
    # Add empty rows to reach 18 rows
    while len(data) <= 18:
        data.append([str(len(data)), "", "", ""])

    t = Table(data, colWidths=[30, 220, 180, 100])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (1, 1), (1, -1), 10),
        ('ALIGN', (1, 1), (1, -1), 'LEFT'),
    ]))
    elements.append(t)
    
    # Build with footer
    doc.build(elements, onFirstPage=draw_footer, onLaterPages=draw_footer)
    
    buffer.seek(0)
    filename = f"Attendance_{db_session.project.partner.name.replace(' ', '_')}_{db_session.created_at.strftime('%Y%m%d')}.pdf"
    
    return Response(
        content=buffer.getvalue(),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
