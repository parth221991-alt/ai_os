from pathlib import Path
from typing import Any
from uuid import UUID

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    HRFlowable, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
)


def _style(name: str, **kwargs) -> ParagraphStyle:
    base = getSampleStyleSheet()["Normal"]
    return ParagraphStyle(name, parent=base, **kwargs)


NAME_STYLE = _style("Name", fontSize=18, fontName="Helvetica-Bold", spaceAfter=2)
CONTACT_STYLE = _style("Contact", fontSize=9, textColor=colors.grey, spaceAfter=6)
SECTION_STYLE = _style("Section", fontSize=11, fontName="Helvetica-Bold", spaceBefore=10, spaceAfter=3)
BODY_STYLE = _style("Body", fontSize=9, leading=13)
BULLET_STYLE = _style("Bullet", fontSize=9, leading=13, leftIndent=10, bulletIndent=4)
JOB_TITLE_STYLE = _style("JobTitle", fontSize=10, fontName="Helvetica-Bold")
COMPANY_STYLE = _style("Company", fontSize=9, textColor=colors.HexColor("#444444"))


def _divider():
    return HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#cccccc"), spaceAfter=4)


def generate_resume_pdf(
    resume_content: dict[str, Any],
    output_dir: str,
    resume_variant_id: UUID,
    candidate_name: str = "Candidate",
) -> str:
    output_path = Path(output_dir) / f"{resume_variant_id}.pdf"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        topMargin=15 * mm,
        bottomMargin=15 * mm,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
    )

    story = []

    # Header
    name = resume_content.get("name", candidate_name)
    story.append(Paragraph(name, NAME_STYLE))

    contact_parts = []
    for field in ("email", "phone", "linkedin", "github", "location"):
        val = resume_content.get(field, "")
        if val:
            contact_parts.append(val)
    if contact_parts:
        story.append(Paragraph(" | ".join(contact_parts), CONTACT_STYLE))

    story.append(_divider())

    # Summary
    summary = resume_content.get("summary", "")
    if summary:
        story.append(Paragraph("PROFESSIONAL SUMMARY", SECTION_STYLE))
        story.append(Paragraph(summary, BODY_STYLE))
        story.append(Spacer(1, 4))

    # Skills
    skills = resume_content.get("skills", [])
    if skills:
        story.append(Paragraph("TECHNICAL SKILLS", SECTION_STYLE))
        story.append(_divider())
        skills_text = " • ".join(skills)
        story.append(Paragraph(skills_text, BODY_STYLE))
        story.append(Spacer(1, 4))

    # Experience
    experience = resume_content.get("experience", [])
    if experience:
        story.append(Paragraph("EXPERIENCE", SECTION_STYLE))
        story.append(_divider())
        for job in experience:
            title = job.get("title", "")
            company = job.get("company", "")
            period = job.get("period", "")
            location = job.get("location", "")

            header_data = [[
                Paragraph(title, JOB_TITLE_STYLE),
                Paragraph(period, COMPANY_STYLE),
            ]]
            header_table = Table(header_data, colWidths=["70%", "30%"])
            header_table.setStyle(TableStyle([
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("ALIGN", (1, 0), (1, 0), "RIGHT"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ]))
            story.append(header_table)
            story.append(Paragraph(f"{company}  {location}", COMPANY_STYLE))

            for bullet in job.get("bullets", []):
                story.append(Paragraph(f"• {bullet}", BULLET_STYLE))
            story.append(Spacer(1, 5))

    # Education
    education = resume_content.get("education", [])
    if education:
        story.append(Paragraph("EDUCATION", SECTION_STYLE))
        story.append(_divider())
        for edu in education:
            degree = edu.get("degree", "")
            institution = edu.get("institution", "")
            year = edu.get("year", "")
            story.append(Paragraph(f"{degree} — {institution} ({year})", BODY_STYLE))
        story.append(Spacer(1, 4))

    # Certifications
    certs = resume_content.get("certifications", [])
    if certs:
        story.append(Paragraph("CERTIFICATIONS", SECTION_STYLE))
        story.append(_divider())
        for cert in certs:
            name_c = cert.get("name", "")
            issuer = cert.get("issuer", "")
            year_c = cert.get("year", "")
            story.append(Paragraph(f"• {name_c} — {issuer} ({year_c})", BULLET_STYLE))

    doc.build(story)
    return str(output_path)
