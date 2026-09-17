import streamlit as st
import json
import os
import re
import time
from io import BytesIO
from xml.sax.saxutils import escape

from dotenv import load_dotenv
from google import genai

from resume_parser import extract_resume_text
from config.config import EXTRACTED_TEXT, ANALYSIS_RESULT

# PDF
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="ResumeAI | Smart Resume Analyzer",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# PROFESSIONAL LIGHT UI
# =========================================================

st.markdown("""
<style>

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}


/* =====================================================
   GLOBAL
   ===================================================== */

.stApp {
    background: #f7f8fc;
    color: #172033;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 3rem;
    max-width: 1180px;
}


/* =====================================================
   TEXT
   ===================================================== */

h1, h2, h3, h4 {
    color: #172033 !important;
}

p {
    color: #526071;
}

label {
    color: #344054 !important;
    font-weight: 600 !important;
}

.stMarkdown {
    color: #344054;
}


/* =====================================================
   BRAND
   ===================================================== */

.brand {
    font-size: 31px;
    font-weight: 800;
    letter-spacing: -1.2px;
    color: #172033;
    padding: 2px 0 4px 0;
}

.brand span {
    color: #4f46e5;
}


/* =====================================================
   DIVIDER
   ===================================================== */

hr {
    border: none !important;
    border-top: 1px solid #e6e8ef !important;
}


/* =====================================================
   HERO
   ===================================================== */

.hero {
    padding: 54px 10px 34px 10px;
    text-align: center;
}

.hero-title {
    font-size: 48px;
    font-weight: 800;
    line-height: 1.12;
    letter-spacing: -1.8px;
    color: #172033;
    margin-bottom: 16px;
}

.hero-title span {
    color: #4f46e5;
}

.hero-subtitle {
    font-size: 17px;
    line-height: 1.65;
    color: #667085;
    max-width: 720px;
    margin: auto;
}


/* =====================================================
   UPLOAD CARD
   ===================================================== */

.upload-card {
    margin-top: 18px;
    padding: 30px 32px 22px 32px;
    border-radius: 18px;
    border: 1px solid #e1e5ee;
    background: #ffffff;
    box-shadow: 0 8px 30px rgba(16, 24, 40, 0.06);
}

.upload-title {
    font-size: 22px;
    font-weight: 750;
    color: #172033;
    margin-bottom: 6px;
}

.upload-subtitle {
    color: #667085;
    font-size: 15px;
    margin-bottom: 12px;
}


/* =====================================================
   FILE UPLOADER
   ===================================================== */

[data-testid="stFileUploader"] {
    background: #ffffff;
    border: 0;
    padding: 0;
}

[data-testid="stFileUploaderDropzone"] {
    background: #fafbff !important;
    border: 2px dashed #c7cef0 !important;
    border-radius: 14px !important;
    min-height: 145px !important;
    padding: 22px !important;
}

[data-testid="stFileUploaderDropzone"]:hover {
    border-color: #818cf8 !important;
    background: #f8f8ff !important;
}

[data-testid="stFileUploaderDropzoneInstructions"] {
    color: #667085 !important;
}

[data-testid="stFileUploaderDropzoneInstructions"] span {
    color: #667085 !important;
}

[data-testid="stFileUploaderDropzone"] button {
    background: #ffffff !important;
    color: #4f46e5 !important;
    border: 1px solid #c7cef0 !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    padding: 8px 18px !important;
}

[data-testid="stFileUploaderDropzone"] button:hover {
    background: #f5f5ff !important;
    border-color: #818cf8 !important;
    color: #4338ca !important;
}
/* =====================================================
   ANALYZE BUTTON - EMERALD GREEN
   ===================================================== */

div.stButton > button[kind="primary"] {
    width: 175px !important;
    height: 42px !important;
    min-height: 42px !important;

    padding: 0 16px !important;
    margin: 0 !important;

    border-radius: 9px !important;

    background: #059669 !important;
    background-image: none !important;

    border: 1px solid #059669 !important;

    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;

    font-size: 14px !important;
    font-weight: 700 !important;
    line-height: 42px !important;

    box-shadow: none !important;
    text-shadow: none !important;

    outline: none !important;
    transform: none !important;
    opacity: 1 !important;

    transition: background 0.15s ease !important;
}

div.stButton > button[kind="primary"] p {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;

    font-size: 14px !important;
    font-weight: 700 !important;
}

div.stButton > button[kind="primary"]:hover {
    background: #047857 !important;
    background-image: none !important;

    border-color: #047857 !important;

    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;

    box-shadow: none !important;
    text-shadow: none !important;
    transform: none !important;
}

div.stButton > button[kind="primary"]:focus,
div.stButton > button[kind="primary"]:focus-visible,
div.stButton > button[kind="primary"]:active {
    background: #059669 !important;
    background-image: none !important;

    border-color: #059669 !important;

    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;

    box-shadow: none !important;
    outline: none !important;
}


/* BUTTON TEXT IN ALL STATES */

div.stButton > button[kind="primary"]:hover p,
div.stButton > button[kind="primary"]:focus p,
div.stButton > button[kind="primary"]:focus-visible p,
div.stButton > button[kind="primary"]:active p {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}









/* =====================================================
   TEXT AREA
   ===================================================== */

.stTextArea textarea {
    background: #ffffff !important;
    color: #172033 !important;
    border: 1px solid #d9dee9 !important;
    border-radius: 12px !important;
}

.stTextArea textarea:focus {
    border-color: #818cf8 !important;
    box-shadow: 0 0 0 1px #818cf8 !important;
}

.stTextArea textarea::placeholder {
    color: #98a2b3 !important;
}


/* =====================================================
   SUCCESS MESSAGE
   ===================================================== */

[data-testid="stAlert"] {
    border-radius: 11px !important;
}


/* =====================================================
   METRICS
   ===================================================== */

[data-testid="stMetric"] {
    background: #ffffff;
    border: 1px solid #e4e7ec;
    padding: 18px 18px;
    border-radius: 14px;
    box-shadow: 0 4px 16px rgba(16, 24, 40, 0.045);
}

[data-testid="stMetricLabel"] {
    color: #667085 !important;
}

[data-testid="stMetricValue"] {
    color: #172033 !important;
}


/* =====================================================
   RESULT CARDS
   ===================================================== */

.result-card {
    background: #ffffff;
    border: 1px solid #e4e7ec;
    border-radius: 16px;
    padding: 22px;
    margin-bottom: 18px;
    box-shadow: 0 5px 20px rgba(16, 24, 40, 0.045);
}

.card-title {
    font-size: 18px;
    font-weight: 750;
    color: #172033;
    margin-bottom: 12px;
}


/* =====================================================
   ATS SCORE
   ===================================================== */

.score-box {
    text-align: center;
    padding: 28px 22px;
    border-radius: 18px;
    background: #ffffff;
    border: 1px solid #e4e7ec;
    box-shadow: 0 7px 25px rgba(16, 24, 40, 0.05);
}

.score-number {
    font-size: 60px;
    line-height: 1;
    font-weight: 800;
    color: #4f46e5;
    margin: 12px 0;
}

.score-label {
    color: #667085;
    font-size: 14px;
    font-weight: 600;
}


/* =====================================================
   TAGS
   ===================================================== */

.tag {
    display: inline-block;
    padding: 7px 12px;
    margin: 4px 4px 4px 0;
    border-radius: 18px;
    background: #eef0ff;
    border: 1px solid #dfe3ff;
    color: #4338ca;
    font-size: 13px;
    font-weight: 600;
}


/* =====================================================
   PROGRESS
   ===================================================== */

.stProgress > div > div > div > div {
    background-color: #4f46e5 !important;
}


/* =====================================================
   DOWNLOAD BUTTONS
   ===================================================== */

.stDownloadButton > button {
    min-height: 46px;
    border-radius: 11px !important;
    font-weight: 700 !important;
    color: #344054 !important;
    background: #ffffff !important;
    border: 1px solid #d9dee9 !important;
}

.stDownloadButton > button:hover {
    color: #4f46e5 !important;
    border-color: #818cf8 !important;
    background: #fafaff !important;
}


/* =====================================================
   INFO / WARNING
   ===================================================== */

.stAlert {
    border-radius: 12px !important;
}


/* =====================================================
   FOOTER
   ===================================================== */

.footer {
    text-align: center;
    color: #98a2b3;
    margin-top: 55px;
    font-size: 13px;
    padding-top: 20px;
    border-top: 1px solid #e6e8ef;
}
/* =====================================================
   ANALYZE BUTTON - EMERALD GREEN
   ===================================================== */

div.stButton > button[kind="primary"] {
    background: #059669 !important;
    background-image: none !important;

    border: 1px solid #059669 !important;
    border-color: #059669 !important;

    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;

    box-shadow: none !important;
    text-shadow: none !important;
}

div.stButton > button[kind="primary"] p {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}

div.stButton > button[kind="primary"]:hover {
    background: #047857 !important;
    background-image: none !important;

    border-color: #047857 !important;

    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;

    box-shadow: none !important;
    text-shadow: none !important;

    transform: none !important;
}

div.stButton > button[kind="primary"]:focus,
div.stButton > button[kind="primary"]:focus-visible,
div.stButton > button[kind="primary"]:active {
    background: #059669 !important;
    background-image: none !important;

    border-color: #059669 !important;

    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;

    box-shadow: none !important;
    outline: none !important;
}
</style>
""", unsafe_allow_html=True)


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def clean_json_response(text):
    text = text.strip()

    if text.startswith("```"):
        text = re.sub(
            r"^```(?:json)?\s*",
            "",
            text,
            flags=re.IGNORECASE
        )
        text = re.sub(
            r"\s*```$",
            "",
            text
        )

    match = re.search(
        r"\{.*\}",
        text,
        re.DOTALL
    )

    if match:
        return match.group(0)

    return text


def safe_list(data):
    if isinstance(data, list):
        return data
    return []


def safe_int(value, default=0):
    try:
        return int(value)
    except:
        return default


def create_pdf_report(analysis, resume_name):

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=22,
        leading=27,
        alignment=TA_CENTER,
        spaceAfter=8
    )

    subtitle_style = ParagraphStyle(
        "ReportSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        textColor=colors.grey,
        alignment=TA_CENTER,
        spaceAfter=18
    )

    section_style = ParagraphStyle(
        "SectionTitle",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=18,
        spaceBefore=13,
        spaceAfter=7
    )

    body_style = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        spaceAfter=5
    )

    small_style = ParagraphStyle(
        "Small",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=8,
        leading=11
    )

    score_style = ParagraphStyle(
        "Score",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=25,
        leading=30,
        alignment=TA_CENTER
    )

    story = []

    story.append(Paragraph("ResumeAI", title_style))

    story.append(
        Paragraph(
            "AI-Powered Resume Analysis Report",
            subtitle_style
        )
    )

    filename = escape(str(resume_name))

    info = [
        [
            Paragraph("<b>Resume File</b>", body_style),
            Paragraph(filename, body_style)
        ],
        [
            Paragraph("<b>Analysis Engine</b>", body_style),
            Paragraph(
                "Gemini AI + ResumeAI Analysis Pipeline",
                body_style
            )
        ]
    ]

    info_table = Table(
        info,
        colWidths=[45 * mm, 125 * mm]
    )

    info_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#eeeeee")),
            ("BOX", (0, 0), (-1, -1), 0.5, colors.grey),
            ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.lightgrey),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 7),
            ("RIGHTPADDING", (0, 0), (-1, -1), 7),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6)
        ])
    )

    story.append(info_table)

    score = safe_int(analysis.get("ats_score", 0))

    if score >= 80:
        status = "Excellent Resume"
    elif score >= 70:
        status = "Strong Resume"
    elif score >= 60:
        status = "Good, but needs improvement"
    elif score >= 40:
        status = "Needs improvement"
    else:
        status = "Major improvements recommended"

    story.append(
        Paragraph(
            "ATS Compatibility Score",
            section_style
        )
    )

    score_table = Table(
        [[
            Paragraph(f"{score}/100", score_style),
            Paragraph(
                f"<b>{escape(status)}</b><br/>Overall Resume Assessment",
                ParagraphStyle(
                    "Status",
                    parent=body_style,
                    alignment=TA_CENTER,
                    fontSize=10,
                    leading=15
                )
            )
        ]],
        colWidths=[70 * mm, 100 * mm]
    )

    score_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f5f3ff")),
            ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#6d5dfc")),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
            ("RIGHTPADDING", (0, 0), (-1, -1), 10),
            ("TOPPADDING", (0, 0), (-1, -1), 14),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 14)
        ])
    )

    story.append(score_table)

    breakdown = analysis.get("ats_breakdown", {})

    if isinstance(breakdown, dict) and breakdown:

        story.append(
            Paragraph(
                "ATS Score Breakdown",
                section_style
            )
        )

        rows = [
            [
                Paragraph("<b>Category</b>", small_style),
                Paragraph("<b>Score</b>", small_style)
            ]
        ]

        for key, value in breakdown.items():

            rows.append([
                Paragraph(
                    escape(
                        str(key).replace(
                            "_",
                            " "
                        ).title()
                    ),
                    small_style
                ),
                Paragraph(
                    f"{safe_int(value)}%",
                    small_style
                )
            ])

        table = Table(
            rows,
            colWidths=[130 * mm, 40 * mm]
        )

        table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#eeeeee")),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.grey),
                ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.lightgrey),
                ("ALIGN", (1, 1), (1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5)
            ])
        )

        story.append(table)

    role_matching = safe_list(
        analysis.get("role_matching", [])
    )

    story.append(
        Paragraph(
            "Recommended Career Roles",
            section_style
        )
    )

    if role_matching:

        rows = [
            [
                Paragraph("<b>Role</b>", small_style),
                Paragraph("<b>Match</b>", small_style)
            ]
        ]

        for item in role_matching:

            if isinstance(item, dict):

                role = item.get(
                    "role",
                    "Unknown Role"
                )

                percentage = safe_int(
                    item.get(
                        "match_percentage",
                        0
                    )
                )

                rows.append([
                    Paragraph(
                        escape(str(role)),
                        small_style
                    ),
                    Paragraph(
                        f"{percentage}%",
                        small_style
                    )
                ])

        table = Table(
            rows,
            colWidths=[130 * mm, 40 * mm]
        )

        table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#eeeeee")),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.grey),
                ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.lightgrey),
                ("ALIGN", (1, 1), (1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5)
            ])
        )

        story.append(table)

    health_check = safe_list(
        analysis.get("resume_health_check", [])
    )

    story.append(
        Paragraph(
            "Resume Health Check",
            section_style
        )
    )

    for item in health_check:

        if isinstance(item, dict):

            section = item.get("item", "Check")
            status_value = item.get("status", "Review")
            reason = item.get("reason", "")

            story.append(
                Paragraph(
                    f"<b>{escape(str(section))}</b> — "
                    f"{escape(str(status_value))}<br/>"
                    f"{escape(str(reason))}",
                    body_style
                )
            )

    section_analysis = safe_list(
        analysis.get("section_analysis", [])
    )

    story.append(
        Paragraph(
            "Resume Section Analysis",
            section_style
        )
    )

    for item in section_analysis:

        if isinstance(item, dict):

            section = item.get("section", "Section")
            status_value = item.get("status", "Review")
            recommendation = item.get(
                "recommendation",
                ""
            )

            story.append(
                Paragraph(
                    f"<b>{escape(str(section))}</b> — "
                    f"{escape(str(status_value))}<br/>"
                    f"{escape(str(recommendation))}",
                    body_style
                )
            )

    technical_skills = safe_list(
        analysis.get("technical_skills", [])
    )

    story.append(
        Paragraph(
            "Technical Skills",
            section_style
        )
    )

    if technical_skills:

        story.append(
            Paragraph(
                " • ".join(
                    escape(str(skill))
                    for skill in technical_skills
                ),
                body_style
            )
        )

    soft_skills = safe_list(
        analysis.get("soft_skills", [])
    )

    story.append(
        Paragraph(
            "Soft Skills",
            section_style
        )
    )

    for item in soft_skills:

        story.append(
            Paragraph(
                f"• {escape(str(item))}",
                body_style
            )
        )

    keywords_found = safe_list(
        analysis.get("keywords_found", [])
    )

    suggested_keywords = safe_list(
        analysis.get("suggested_keywords", [])
    )

    story.append(
        Paragraph(
            "ATS Keyword Analysis",
            section_style
        )
    )

    story.append(
        Paragraph(
            "<b>Keywords Found</b>",
            body_style
        )
    )

    if keywords_found:

        story.append(
            Paragraph(
                " • ".join(
                    escape(str(item))
                    for item in keywords_found
                ),
                body_style
            )
        )

    story.append(
        Paragraph(
            "<b>Suggested Keywords</b>",
            body_style
        )
    )

    if suggested_keywords:

        story.append(
            Paragraph(
                " • ".join(
                    escape(str(item))
                    for item in suggested_keywords
                ),
                body_style
            )
        )

    content_quality = safe_list(
        analysis.get("content_quality", [])
    )

    story.append(
        Paragraph(
            "Content Quality Analysis",
            section_style
        )
    )

    for item in content_quality:

        if isinstance(item, dict):

            category = item.get(
                "category",
                "Quality Check"
            )

            score_value = item.get(
                "score",
                0
            )

            comment = item.get(
                "comment",
                ""
            )

            story.append(
                Paragraph(
                    f"<b>{escape(str(category))}</b> — "
                    f"{safe_int(score_value)}%<br/>"
                    f"{escape(str(comment))}",
                    body_style
                )
            )

    strengths = safe_list(
        analysis.get("strengths", [])
    )

    story.append(
        Paragraph(
            "Strengths",
            section_style
        )
    )

    for item in strengths:

        story.append(
            Paragraph(
                f"✓ {escape(str(item))}",
                body_style
            )
        )

    weaknesses = safe_list(
        analysis.get("weaknesses", [])
    )

    story.append(
        Paragraph(
            "Weaknesses",
            section_style
        )
    )

    for item in weaknesses:

        story.append(
            Paragraph(
                f"• {escape(str(item))}",
                body_style
            )
        )

    missing_skills = safe_list(
        analysis.get("missing_skills", [])
    )

    story.append(
        Paragraph(
            "Missing / Recommended Skills",
            section_style
        )
    )

    for item in missing_skills:

        story.append(
            Paragraph(
                f"＋ {escape(str(item))}",
                body_style
            )
        )

    project_analysis = safe_list(
        analysis.get("project_analysis", [])
    )

    story.append(
        Paragraph(
            "Project Strength Analysis",
            section_style
        )
    )

    for item in project_analysis:

        if isinstance(item, dict):

            project = item.get(
                "project",
                "Project"
            )

            technical_depth = item.get(
                "technical_depth",
                0
            )

            description_quality = item.get(
                "description_quality",
                0
            )

            impact = item.get(
                "impact",
                0
            )

            recommendation = item.get(
                "recommendation",
                ""
            )

            story.append(
                Paragraph(
                    f"<b>{escape(str(project))}</b><br/>"
                    f"Technical Depth: {safe_int(technical_depth)}%<br/>"
                    f"Description Quality: {safe_int(description_quality)}%<br/>"
                    f"Impact: {safe_int(impact)}%<br/>"
                    f"Recommendation: {escape(str(recommendation))}",
                    body_style
                )
            )

    summary_suggestion = analysis.get(
        "summary_suggestion",
        ""
    )

    if summary_suggestion:

        story.append(
            Paragraph(
                "AI Professional Summary Suggestion",
                section_style
            )
        )

        story.append(
            Paragraph(
                escape(str(summary_suggestion)),
                body_style
            )
        )

    bullet_improvements = safe_list(
        analysis.get("bullet_improvements", [])
    )

    story.append(
        Paragraph(
            "AI Bullet Improvement Suggestions",
            section_style
        )
    )

    for item in bullet_improvements:

        if isinstance(item, dict):

            original = item.get("original", "")
            improved = item.get("improved", "")

            story.append(
                Paragraph(
                    f"<b>Original:</b> {escape(str(original))}<br/>"
                    f"<b>Improved:</b> {escape(str(improved))}",
                    body_style
                )
            )

    improvements = safe_list(
        analysis.get("resume_improvements", [])
    )

    story.append(
        Paragraph(
            "AI Resume Improvement Plan",
            section_style
        )
    )

    for index, item in enumerate(
        improvements,
        start=1
    ):

        story.append(
            Paragraph(
                f"<b>{index}.</b> {escape(str(item))}",
                body_style
            )
        )

    interview = analysis.get(
        "interview_preparation",
        {}
    )

    if isinstance(interview, dict):

        story.append(
            Paragraph(
                "AI Interview Preparation",
                section_style
            )
        )

        technical_questions = safe_list(
            interview.get(
                "technical_questions",
                []
            )
        )

        project_questions = safe_list(
            interview.get(
                "project_questions",
                []
            )
        )

        hr_questions = safe_list(
            interview.get(
                "hr_questions",
                []
            )
        )

        story.append(
            Paragraph(
                "<b>Technical Questions</b>",
                body_style
            )
        )

        for index, question in enumerate(
            technical_questions,
            start=1
        ):

            story.append(
                Paragraph(
                    f"{index}. {escape(str(question))}",
                    body_style
                )
            )

        story.append(
            Paragraph(
                "<b>Project Questions</b>",
                body_style
            )
        )

        for index, question in enumerate(
            project_questions,
            start=1
        ):

            story.append(
                Paragraph(
                    f"{index}. {escape(str(question))}",
                    body_style
                )
            )

        story.append(
            Paragraph(
                "<b>HR Questions</b>",
                body_style
            )
        )

        for index, question in enumerate(
            hr_questions,
            start=1
        ):

            story.append(
                Paragraph(
                    f"{index}. {escape(str(question))}",
                    body_style
                )
            )

    story.append(
        Spacer(
            1,
            18
        )
    )

    story.append(
        Paragraph(
            "Generated by ResumeAI • AI-Powered Resume Intelligence",
            subtitle_style
        )
    )

    doc.build(story)

    buffer.seek(0)

    return buffer.getvalue()


# =========================================================
# NAVBAR
# =========================================================

st.markdown(
    '<div class="brand">◈ Resume<span>AI</span></div>',
    unsafe_allow_html=True
)

st.divider()


# =========================================================
# HERO
# =========================================================

st.markdown("""
<div class="hero">

<div class="hero-title">
Make Your Resume <span>ATS-Ready.</span><br>
Get Hired Faster.
</div>

<div class="hero-subtitle">
Analyze your resume with AI, discover your ATS score,
identify skill gaps, and get actionable improvements
before you apply.
</div>

</div>
""", unsafe_allow_html=True)


# =========================================================
# UPLOAD SECTION
# =========================================================

st.markdown("""
<div class="upload-card">

<div class="upload-title">
📄 Upload Your Resume
</div>

<div class="upload-subtitle">
Upload your PDF resume and get an AI-powered ATS analysis in seconds.
</div>

</div>
""", unsafe_allow_html=True)


uploaded_file = st.file_uploader(
    "Choose your resume PDF",
    type=["pdf"],
    label_visibility="collapsed"
)


# =========================================================
# OPTIONAL JOB DESCRIPTION
# =========================================================

job_description = st.text_area(
    "🎯 Job Description (Optional)",
    placeholder=(
        "Paste the job description here to compare "
        "your resume with a specific job..."
    ),
    height=150
)


# =========================================================
# ANALYZE
# =========================================================

if uploaded_file:

    st.success(
        f"✓ {uploaded_file.name} uploaded successfully"
    )

    if st.button(
        "🚀 Analyze Resume",
        type="primary"
    ):

        try:

           

            with open(
                "resume.pdf",
                "wb"
            ) as file:

                file.write(
                    uploaded_file.getbuffer()
                )

        except Exception as e:

            st.error(
                f"Could not save resume: {e}"
            )

            st.stop()

        st.divider()

        st.markdown(
            "### ◈ AI Resume Analysis"
        )

        analysis_progress = st.progress(0)

        with st.spinner(
            "📄 Reading and extracting your resume..."
        ):

            try:

                analysis_progress.progress(20)

                resume_text = extract_resume_text(
                    "resume.pdf"
                )

                if not resume_text:

                    st.error(
                        "Could not extract text from the resume."
                    )

                    st.stop()

                with open(
                    EXTRACTED_TEXT,
                    "w",
                    encoding="utf-8"
                ) as file:

                    file.write(
                        resume_text
                    )

                analysis_progress.progress(35)

            except Exception as e:

                st.error(
                    f"Resume extraction error: {e}"
                )

                st.stop()

        with st.spinner(
            "🤖 Gemini AI is performing advanced resume analysis..."
        ):

            try:

                load_dotenv()

                api_key = os.getenv(
                    "GEMINI_API_KEY"
                )

                if not api_key:

                    st.error(
                        "GEMINI_API_KEY not found in .env file."
                    )

                    st.stop()

                client = genai.Client(
                    api_key=api_key
                )

                if job_description.strip():

                    job_context = f"""
A JOB DESCRIPTION has been provided.

Compare the resume against this job description.

JOB DESCRIPTION:

{job_description}

Perform:
- job match percentage
- matching skills
- missing job-specific skills
- keyword gaps
- relevant recommendations

Do not invent candidate experience.
"""

                else:

                    job_context = """
No job description was provided.

Perform general ATS and career analysis based only
on the resume.
"""

                prompt = f"""
You are an expert ATS resume analyzer,
career advisor, recruiter and technical interviewer.

Analyze the resume carefully.

Your analysis must be based ONLY on information
actually present in the resume.

Do not invent:
- experience
- education
- certifications
- skills
- achievements
- metrics
- job history

If information is unavailable, say so.

{job_context}

Return ONLY valid JSON.

Use EXACTLY this structure:

{{
    "ats_score": 0,

    "ats_breakdown": {{
        "content_quality": 0,
        "skills": 0,
        "keywords": 0,
        "structure": 0,
        "impact": 0
    }},

    "recommended_roles": [],

    "role_matching": [
        {{
            "role": "Role Name",
            "match_percentage": 0
        }}
    ],

    "technical_skills": [],

    "soft_skills": [],

    "strengths": [],

    "weaknesses": [],

    "missing_skills": [],

    "keywords_found": [],

    "suggested_keywords": [],

    "resume_health_check": [
        {{
            "item": "Contact Information",
            "status": "Good",
            "reason": "Short explanation"
        }}
    ],

    "section_analysis": [
        {{
            "section": "Education",
            "status": "Present",
            "recommendation": "Short recommendation"
        }}
    ],

    "content_quality": [
        {{
            "category": "Grammar",
            "score": 0,
            "comment": "Short explanation"
        }}
    ],

    "project_analysis": [
        {{
            "project": "Project Name",
            "technical_depth": 0,
            "description_quality": 0,
            "impact": 0,
            "recommendation": "Short recommendation"
        }}
    ],

    "bullet_improvements": [
        {{
            "original": "Existing resume bullet",
            "improved": "Improved version"
        }}
    ],

    "summary_suggestion": "",

    "resume_improvements": [],

    "job_description_match": {{
        "match_percentage": 0,
        "matching_skills": [],
        "missing_job_skills": [],
        "keyword_gaps": [],
        "recommendations": []
    }},

    "interview_preparation": {{
        "technical_questions": [],
        "project_questions": [],
        "hr_questions": []
    }}
}}

RULES:

1. ats_score must be between 0 and 100.

2. ats_breakdown values must be between 0 and 100.

3. Recommended roles must be realistic for the candidate.

4. Return up to 5 recommended roles.

5. role_matching must contain up to 5 roles.

6. Role percentages must be based on actual resume evidence.
Do NOT generate random percentages.

7. technical_skills must contain skills actually found
in the resume.

8. missing_skills should be useful skills for realistic
target roles.

9. keywords_found must come from the resume.

10. suggested_keywords should be relevant to realistic
target roles and should not falsely claim that the
candidate already possesses them.

11. Resume health check should check:
- contact information
- education
- skills
- projects
- experience
- certifications
- section naming
- readability
- ATS friendliness
- measurable achievements

12. Section analysis should identify important sections
that are present, weak or missing.

13. Content quality should check:
- grammar
- spelling
- repetition
- bullet quality
- action verbs
- quantified impact
- clarity

14. Project analysis should analyze projects actually
mentioned in the resume.

15. Do not invent project metrics.

16. Bullet improvements must preserve the original meaning.
Do not add fake numbers or achievements.

17. summary_suggestion should be professional and based
only on the candidate's actual background.

18. If job description is provided, compare resume
against it.

19. If job description is not provided, job_description_match
may contain empty arrays and match_percentage can be 0.

20. Interview questions must be based on the actual resume.

21. Include technical questions related to the candidate's
actual technologies.

22. Include project questions related to actual projects.

23. Include HR questions relevant to the candidate profile.

24. Return ONLY JSON.

25. Do not use Markdown.

26. Do not use code fences.

RESUME:

{resume_text}
"""

                analysis_progress.progress(50)

                gemini_start = time.time()

                response = client.interactions.create(
                    model="gemini-3.6-flash",
                    input=prompt
                )

                gemini_time = time.time() - gemini_start

                st.caption(
                    f"⚡ Gemini AI analysis time: {gemini_time:.1f} seconds"
                )

                analysis_progress.progress(75)

                result_text = response.output_text.strip()

                result_text = clean_json_response(
                    result_text
                )

                analysis = json.loads(
                    result_text
                )

                analysis["ats_score"] = max(
                    0,
                    min(
                        safe_int(
                            analysis.get(
                                "ats_score",
                                0
                            )
                        ),
                        100
                    )
                )

                list_fields = [
                    "recommended_roles",
                    "technical_skills",
                    "soft_skills",
                    "strengths",
                    "weaknesses",
                    "missing_skills",
                    "keywords_found",
                    "suggested_keywords",
                    "resume_health_check",
                    "section_analysis",
                    "content_quality",
                    "project_analysis",
                    "bullet_improvements",
                    "resume_improvements"
                ]

                for field in list_fields:

                    analysis[field] = safe_list(
                        analysis.get(
                            field,
                            []
                        )
                    )

                if not isinstance(
                    analysis.get(
                        "role_matching",
                        []
                    ),
                    list
                ):

                    analysis["role_matching"] = []

                if not isinstance(
                    analysis.get(
                        "ats_breakdown",
                        {}
                    ),
                    dict
                ):

                    analysis["ats_breakdown"] = {}

                if not isinstance(
                    analysis.get(
                        "job_description_match",
                        {}
                    ),
                    dict
                ):

                    analysis["job_description_match"] = {}

                if not isinstance(
                    analysis.get(
                        "interview_preparation",
                        {}
                    ),
                    dict
                ):

                    analysis["interview_preparation"] = {}

                analysis_progress.progress(90)

                with open(
                    ANALYSIS_RESULT,
                    "w",
                    encoding="utf-8"
                ) as file:

                    json.dump(
                        analysis,
                        file,
                        indent=4,
                        ensure_ascii=False
                    )

                analysis_progress.progress(100)

            except json.JSONDecodeError:

                st.error(
                    "Gemini returned invalid JSON. Please try again."
                )

                st.stop()

            except Exception as e:

                st.error(
                    f"AI analysis error: {e}"
                )

                st.stop()


        # =================================================
        # RESULTS
        # =================================================

        st.divider()

        score = safe_int(
            analysis.get(
                "ats_score",
                0
            )
        )

        st.markdown(
            "## 📊 Resume Analysis"
        )

        if score >= 80:
            score_status = "Excellent Resume"
        elif score >= 70:
            score_status = "Strong Resume"
        elif score >= 60:
            score_status = "Good, but needs improvement"
        elif score >= 40:
            score_status = "Needs improvement"
        else:
            score_status = "Major improvements recommended"

        st.caption(
            f"📌 {score_status}"
        )

        technical_count = len(
            analysis.get(
                "technical_skills",
                []
            )
        )

        role_count = len(
            analysis.get(
                "recommended_roles",
                []
            )
        )

        strength_count = len(
            analysis.get(
                "strengths",
                []
            )
        )

        missing_count = len(
            analysis.get(
                "missing_skills",
                []
            )
        )

        summary1, summary2, summary3, summary4, summary5 = st.columns(5)

        with summary1:
            st.metric(
                "ATS Score",
                f"{score}/100"
            )

        with summary2:
            st.metric(
                "Technical Skills",
                technical_count
            )

        with summary3:
            st.metric(
                "Recommended Roles",
                role_count
            )

        with summary4:
            st.metric(
                "Strengths",
                strength_count
            )

        with summary5:
            st.metric(
                "Missing Skills",
                missing_count
            )

        col1, col2 = st.columns([1, 2])

        with col1:

            st.markdown(
                f"""
                <div class="score-box">

                <div class="score-label">
                ATS COMPATIBILITY SCORE
                </div>

                <div class="score-number">
                {score}
                </div>

                <div class="score-label">
                out of 100
                </div>

                </div>
                """,
                unsafe_allow_html=True
            )

            st.progress(
                score / 100
            )

        with col2:

            st.markdown(
                '<div class="result-card">'
                '<div class="card-title">💼 Recommended Roles</div>',
                unsafe_allow_html=True
            )

            roles = analysis.get(
                "recommended_roles",
                []
            )

            if roles:

                for role in roles:

                    st.markdown(
                        f'<span class="tag">{escape(str(role))}</span>',
                        unsafe_allow_html=True
                    )

            else:

                st.write(
                    "No roles returned."
                )

            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )

        st.markdown(
            "### 📈 ATS Score Breakdown"
        )

        breakdown = analysis.get(
            "ats_breakdown",
            {}
        )

        if breakdown:

            breakdown_cols = st.columns(
                len(breakdown)
            )

            for index, (
                category,
                value
            ) in enumerate(
                breakdown.items()
            ):

                with breakdown_cols[index]:

                    score_value = max(
                        0,
                        min(
                            safe_int(value),
                            100
                        )
                    )

                    st.metric(
                        category.replace(
                            "_",
                            " "
                        ).title(),
                        f"{score_value}%"
                    )

                    st.progress(
                        score_value / 100
                    )

        role_matching = analysis.get(
            "role_matching",
            []
        )

        st.markdown(
            "### 🎯 Career Role Matching"
        )

        if role_matching:

            for item in role_matching:

                if isinstance(
                    item,
                    dict
                ):

                    role = item.get(
                        "role",
                        "Role"
                    )

                    match = max(
                        0,
                        min(
                            safe_int(
                                item.get(
                                    "match_percentage",
                                    0
                                )
                            ),
                            100
                        )
                    )

                    st.write(
                        f"**{role} — {match}%**"
                    )

                    st.progress(
                        match / 100
                    )

        else:

            st.info(
                "No role matching data returned."
            )

        st.markdown(
            '<div class="result-card">'
            '<div class="card-title">🛠️ Technical Skills</div>',
            unsafe_allow_html=True
        )

        technical_skills = analysis.get(
            "technical_skills",
            []
        )

        if technical_skills:

            for skill in technical_skills:

                st.markdown(
                    f'<span class="tag">{escape(str(skill))}</span>',
                    unsafe_allow_html=True
                )

        else:

            st.write(
                "No technical skills found."
            )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )

        st.markdown(
            "### 🔎 ATS Keyword Analysis"
        )

        keyword_col1, keyword_col2 = st.columns(2)

        with keyword_col1:

            st.markdown(
                "#### ✅ Keywords Found"
            )

            keywords_found = analysis.get(
                "keywords_found",
                []
            )

            if keywords_found:

                for keyword in keywords_found:

                    st.markdown(
                        f'<span class="tag">{escape(str(keyword))}</span>',
                        unsafe_allow_html=True
                    )

            else:

                st.write(
                    "No keywords detected."
                )

        with keyword_col2:

            st.markdown(
                "#### 💡 Suggested Keywords"
            )

            suggested_keywords = analysis.get(
                "suggested_keywords",
                []
            )

            if suggested_keywords:

                for keyword in suggested_keywords:

                    st.markdown(
                        f'<span class="tag">{escape(str(keyword))}</span>',
                        unsafe_allow_html=True
                    )

            else:

                st.write(
                    "No suggestions."
                )

        if job_description.strip():

            st.divider()

            st.markdown(
                "## 🎯 Job Description Matching"
            )

            job_match = analysis.get(
                "job_description_match",
                {}
            )

            if job_match:

                match_percentage = max(
                    0,
                    min(
                        safe_int(
                            job_match.get(
                                "match_percentage",
                                0
                            )
                        ),
                        100
                    )
                )

                st.metric(
                    "Resume ↔ Job Match",
                    f"{match_percentage}%"
                )

                st.progress(
                    match_percentage / 100
                )

                jd_col1, jd_col2 = st.columns(2)

                with jd_col1:

                    st.markdown(
                        "### ✅ Matching Skills"
                    )

                    for item in safe_list(
                        job_match.get(
                            "matching_skills",
                            []
                        )
                    ):

                        st.write(
                            f"✓ {item}"
                        )

                with jd_col2:

                    st.markdown(
                        "### ⚠️ Missing Job Skills"
                    )

                    for item in safe_list(
                        job_match.get(
                            "missing_job_skills",
                            []
                        )
                    ):

                        st.write(
                            f"• {item}"
                        )

                keyword_gaps = safe_list(
                    job_match.get(
                        "keyword_gaps",
                        []
                    )
                )

                if keyword_gaps:

                    st.markdown(
                        "### 🔍 Job Keyword Gaps"
                    )

                    for item in keyword_gaps:

                        st.write(
                            f"• {item}"
                        )

                recommendations = safe_list(
                    job_match.get(
                        "recommendations",
                        []
                    )
                )

                if recommendations:

                    st.markdown(
                        "### 💡 Job Match Recommendations"
                    )

                    for index, item in enumerate(
                        recommendations,
                        start=1
                    ):

                        st.write(
                            f"**{index}.** {item}"
                        )

        st.divider()

        st.markdown(
            "## 🩺 Resume Health Check"
        )

        health_check = analysis.get(
            "resume_health_check",
            []
        )

        if health_check:

            for item in health_check:

                if isinstance(
                    item,
                    dict
                ):

                    check_name = item.get(
                        "item",
                        "Check"
                    )

                    status_value = item.get(
                        "status",
                        "Review"
                    )

                    reason = item.get(
                        "reason",
                        ""
                    )

                    status_lower = str(
                        status_value
                    ).lower()

                    if status_lower in [
                        "good",
                        "present",
                        "yes",
                        "pass",
                        "passed"
                    ]:

                        icon = "✅"

                    elif status_lower in [
                        "missing",
                        "weak",
                        "poor",
                        "no"
                    ]:

                        icon = "❌"

                    else:

                        icon = "⚠️"

                    st.write(
                        f"{icon} **{check_name}** — "
                        f"{status_value}"
                    )

                    if reason:

                        st.caption(
                            reason
                        )

        st.markdown(
            "## 📑 Resume Section Analysis"
        )

        section_analysis = analysis.get(
            "section_analysis",
            []
        )

        for item in section_analysis:

            if isinstance(
                item,
                dict
            ):

                section = item.get(
                    "section",
                    "Section"
                )

                status_value = item.get(
                    "status",
                    "Review"
                )

                recommendation = item.get(
                    "recommendation",
                    ""
                )

                st.write(
                    f"**{section}** — {status_value}"
                )

                if recommendation:

                    st.caption(
                        recommendation
                    )

        st.markdown(
            "## ✍️ Content Quality Analysis"
        )

        content_quality = analysis.get(
            "content_quality",
            []
        )

        if content_quality:

            quality_cols = st.columns(
                min(
                    len(content_quality),
                    4
                )
            )

            for index, item in enumerate(
                content_quality
            ):

                if isinstance(
                    item,
                    dict
                ):

                    category = item.get(
                        "category",
                        "Quality"
                    )

                    quality_score = max(
                        0,
                        min(
                            safe_int(
                                item.get(
                                    "score",
                                    0
                                )
                            ),
                            100
                        )
                    )

                    comment = item.get(
                        "comment",
                        ""
                    )

                    with quality_cols[
                        index % len(quality_cols)
                    ]:

                        st.metric(
                            category,
                            f"{quality_score}%"
                        )

                        st.progress(
                            quality_score / 100
                        )

                        if comment:

                            st.caption(
                                comment
                            )

        st.divider()

        st.markdown(
            "## 🚀 Project Strength Analysis"
        )

        project_analysis = analysis.get(
            "project_analysis",
            []
        )

        if project_analysis:

            for item in project_analysis:

                if isinstance(
                    item,
                    dict
                ):

                    project = item.get(
                        "project",
                        "Project"
                    )

                    technical_depth = max(
                        0,
                        min(
                            safe_int(
                                item.get(
                                    "technical_depth",
                                    0
                                )
                            ),
                            100
                        )
                    )

                    description_quality = max(
                        0,
                        min(
                            safe_int(
                                item.get(
                                    "description_quality",
                                    0
                                )
                            ),
                            100
                        )
                    )

                    impact = max(
                        0,
                        min(
                            safe_int(
                                item.get(
                                    "impact",
                                    0
                                )
                            ),
                            100
                        )
                    )

                    recommendation = item.get(
                        "recommendation",
                        ""
                    )

                    st.markdown(
                        f"### 📌 {project}"
                    )

                    p1, p2, p3 = st.columns(3)

                    with p1:

                        st.metric(
                            "Technical Depth",
                            f"{technical_depth}%"
                        )

                    with p2:

                        st.metric(
                            "Description",
                            f"{description_quality}%"
                        )

                    with p3:

                        st.metric(
                            "Impact",
                            f"{impact}%"
                        )

                    if recommendation:

                        st.info(
                            recommendation
                        )

        summary_suggestion = analysis.get(
            "summary_suggestion",
            ""
        )

        if summary_suggestion:

            st.divider()

            st.markdown(
                "## 📝 AI Professional Summary Suggestion"
            )

            st.info(
                summary_suggestion
            )

        bullet_improvements = analysis.get(
            "bullet_improvements",
            []
        )

        if bullet_improvements:

            st.markdown(
                "## ✨ AI Bullet Improvement"
            )

            for index, item in enumerate(
                bullet_improvements,
                start=1
            ):

                if isinstance(
                    item,
                    dict
                ):

                    original = item.get(
                        "original",
                        ""
                    )

                    improved = item.get(
                        "improved",
                        ""
                    )

                    st.markdown(
                        f"### Suggestion {index}"
                    )

                    st.write(
                        f"**Original:** {original}"
                    )

                    st.success(
                        f"**Improved:** {improved}"
                    )

        left, right = st.columns(2)

        with left:

            st.markdown(
                '<div class="result-card">'
                '<div class="card-title">🤝 Soft Skills</div>',
                unsafe_allow_html=True
            )

            for item in analysis.get(
                "soft_skills",
                []
            ):

                st.write(
                    "•",
                    item
                )

            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )

        with right:

            st.markdown(
                '<div class="result-card">'
                '<div class="card-title">✨ Strengths</div>',
                unsafe_allow_html=True
            )

            for item in analysis.get(
                "strengths",
                []
            ):

                st.write(
                    "✓",
                    item
                )

            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )

        left, right = st.columns(2)

        with left:

            st.markdown(
                '<div class="result-card">'
                '<div class="card-title">⚠️ Weaknesses</div>',
                unsafe_allow_html=True
            )

            for item in analysis.get(
                "weaknesses",
                []
            ):

                st.write(
                    "•",
                    item
                )

            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )

        with right:

            st.markdown(
                '<div class="result-card">'
                '<div class="card-title">📚 Missing Skills</div>',
                unsafe_allow_html=True
            )

            for item in analysis.get(
                "missing_skills",
                []
            ):

                st.write(
                    "＋",
                    item
                )

            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )

        st.markdown(
            '<div class="result-card">'
            '<div class="card-title">💡 AI Resume Improvement Plan</div>',
            unsafe_allow_html=True
        )

        improvements = analysis.get(
            "resume_improvements",
            []
        )

        for index, item in enumerate(
            improvements,
            start=1
        ):

            st.write(
                f"**{index}.** {item}"
            )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )

        st.divider()

        st.markdown(
            "## 🎤 AI Interview Preparation"
        )

        interview = analysis.get(
            "interview_preparation",
            {}
        )

        if isinstance(
            interview,
            dict
        ):

            interview_col1, interview_col2 = st.columns(2)

            with interview_col1:

                st.markdown(
                    "### 💻 Technical Questions"
                )

                technical_questions = safe_list(
                    interview.get(
                        "technical_questions",
                        []
                    )
                )

                for index, question in enumerate(
                    technical_questions,
                    start=1
                ):

                    st.write(
                        f"**{index}.** {question}"
                    )

            with interview_col2:

                st.markdown(
                    "### 🚀 Project Questions"
                )

                project_questions = safe_list(
                    interview.get(
                        "project_questions",
                        []
                    )
                )

                for index, question in enumerate(
                    project_questions,
                    start=1
                ):

                    st.write(
                        f"**{index}.** {question}"
                    )

            st.markdown(
                "### 👔 HR Questions"
            )

            hr_questions = safe_list(
                interview.get(
                    "hr_questions",
                    []
                )
            )

            for index, question in enumerate(
                hr_questions,
                start=1
            ):

                st.write(
                    f"**{index}.** {question}"
                )

        st.divider()

        st.markdown(
            "## 📥 Download Reports"
        )

        report_json = json.dumps(
            analysis,
            indent=4,
            ensure_ascii=False
        )

        try:

            pdf_report = create_pdf_report(
                analysis,
                uploaded_file.name
            )

            download_col1, download_col2 = st.columns(2)

            with download_col1:

                st.download_button(
                    "📥 Download JSON Report",
                    data=report_json,
                    file_name="resume_analysis.json",
                    mime="application/json",
                    use_container_width=True
                )

            with download_col2:

                st.download_button(
                    "📄 Download A4 PDF Report",
                    data=pdf_report,
                    file_name="resume_analysis_report.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )

        except Exception as e:

            st.error(
                f"Could not generate PDF report: {e}"
            )

            st.download_button(
                "📥 Download JSON Report",
                data=report_json,
                file_name="resume_analysis.json",
                mime="application/json",
                use_container_width=True
            )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
    ◈ ResumeAI &nbsp;•&nbsp; AI-Powered Resume Intelligence
    </div>
    """,
    unsafe_allow_html=True
)