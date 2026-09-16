#!/usr/bin/env python3
"""Builds docs/IT-Ops-Console-Case-Study.pdf — a short, visual leave-behind
summarizing the IT Ops Console portfolio project. Run with:
    python3 scripts/build_case_study_pdf.py
Requires reportlab + Pillow (pip3 install --user reportlab pillow).
"""
import os

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image,
    PageBreak, HRFlowable, KeepTogether,
)
from reportlab.graphics.shapes import Drawing, Rect, String, Polygon, Line
from reportlab.lib.enums import TA_CENTER

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHOTS = os.path.join(ROOT, "docs", "screenshots")
OUT = os.path.join(ROOT, "docs", "IT-Ops-Console-Case-Study.pdf")

ACCENT = colors.HexColor("#0071e3")
TEXT = colors.HexColor("#1d1d1f")
MUTED = colors.HexColor("#6e6e73")
LINE = colors.HexColor("#d8d8dc")
GREEN = colors.HexColor("#1a7f37")

styles = getSampleStyleSheet()
title_style = ParagraphStyle("TitleX", parent=styles["Title"], textColor=TEXT, fontSize=24, spaceAfter=2)
subtitle_style = ParagraphStyle("SubtitleX", parent=styles["Normal"], textColor=MUTED, fontSize=12, spaceAfter=14)
h2 = ParagraphStyle("H2X", parent=styles["Heading2"], textColor=TEXT, fontSize=14, spaceBefore=16, spaceAfter=8)
body = ParagraphStyle("BodyX", parent=styles["Normal"], textColor=TEXT, fontSize=10, leading=15)
muted = ParagraphStyle("MutedX", parent=styles["Normal"], textColor=MUTED, fontSize=9, leading=13)
caption = ParagraphStyle("CaptionX", parent=styles["Normal"], textColor=MUTED, fontSize=8.5, alignment=TA_CENTER, spaceBefore=4, spaceAfter=12)
link_style = ParagraphStyle("LinkX", parent=styles["Normal"], textColor=ACCENT, fontSize=10, leading=15)


def arrow_flow(labels, y=20, box_w=118, box_h=34, gap=26, font_size=8.5):
    """A small horizontal box-and-arrow diagram flowable."""
    n = len(labels)
    width = n * box_w + (n - 1) * gap
    d = Drawing(width, box_h + 12)
    x = 0
    for i, label in enumerate(labels):
        d.add(Rect(x, y, box_w, box_h, rx=6, ry=6, fillColor=colors.HexColor("#eef4fe"),
                    strokeColor=ACCENT, strokeWidth=1))
        # simple manual line wrap for two-line labels marked with "\n"
        lines = label.split("\n")
        line_h = font_size + 2
        start_y = y + box_h / 2 + (len(lines) - 1) * line_h / 2
        for j, ln in enumerate(lines):
            d.add(String(x + box_w / 2, start_y - j * line_h, ln, fontName="Helvetica-Bold",
                          fontSize=font_size, fillColor=TEXT, textAnchor="middle"))
        if i < n - 1:
            ax1 = x + box_w
            ax2 = x + box_w + gap
            ay = y + box_h / 2
            d.add(Line(ax1, ay, ax2 - 6, ay, strokeColor=MUTED, strokeWidth=1.2))
            d.add(Polygon(points=[ax2, ay, ax2 - 7, ay + 4, ax2 - 7, ay - 4], fillColor=MUTED, strokeColor=MUTED))
        x += box_w + gap
    return d


def section_header(text):
    return [Paragraph(text, h2), HRFlowable(width="100%", thickness=0.75, color=LINE, spaceAfter=8)]


def build():
    doc = SimpleDocTemplate(
        OUT, pagesize=letter,
        leftMargin=0.65 * inch, rightMargin=0.65 * inch,
        topMargin=0.6 * inch, bottomMargin=0.6 * inch,
        title="IT Ops Console - Case Study", author="Bryan Cole",
    )
    story = []

    # ---------- Header ----------
    story.append(Paragraph("IT Ops Console", title_style))
    story.append(Paragraph(
        "A serverless IT-operations tool built as a portfolio project for Clockwork's "
        "IT Operations Specialist posting (Minneapolis, macOS-based environment).",
        subtitle_style,
    ))
    story.append(Table(
        [[Paragraph("<b>Live demo:</b> https://d198vhce9vcowy.cloudfront.net", link_style)],
         [Paragraph("<b>Source code:</b> https://github.com/bcole84/clockwork-it-ops-console", link_style)]],
        colWidths=[7.2 * inch],
        style=TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f5f5f7")),
            ("BOX", (0, 0), (-1, -1), 0.75, LINE),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ]),
    ))
    story.append(Spacer(1, 6))

    story += section_header("Why this exists")
    story.append(Paragraph(
        "Rather than just list skills on a resume, I built a small working tool covering three of the "
        "role's core duties, plus the documentation habit the posting explicitly calls for. Everything "
        "here runs on my own AWS account and was scoped to stay inside AWS's <b>always-free</b> tier.",
        body,
    ))
    story.append(Spacer(1, 8))

    # ---------- Feature -> duty mapping ----------
    story += section_header("What it does")
    data = [
        [Paragraph("<b>Feature</b>", body), Paragraph("<b>Job posting duty it demonstrates</b>", body)],
        [Paragraph("Asset Tracker", body),
         Paragraph('"Manage IT assets... procure, configure, track, maintain, retire... using MDM"', body)],
        [Paragraph("Onboarding &amp; Offboarding", body),
         Paragraph('"Manage employee onboarding and offboarding"', body)],
        [Paragraph("Helpdesk Tickets", body),
         Paragraph('"Triage requests, troubleshoot problems, resolve support tickets"', body)],
        [Paragraph("Knowledge Base (5 playbooks)", body),
         Paragraph('"Document and share knowledge... playbooks, training materials"', body)],
    ]
    t = Table(data, colWidths=[1.9 * inch, 5.3 * inch])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f5f5f7")),
        ("LINEBELOW", (0, 0), (-1, 0), 1, LINE),
        ("LINEBELOW", (0, 1), (-1, -2), 0.5, LINE),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    story.append(t)

    story.append(PageBreak())

    # ---------- Hero screenshot ----------
    story += section_header("Asset Tracker")
    story.append(Paragraph(
        "Tracks laptops and other hardware: type, serial number, assigned employee, status "
        "(In Stock / In Use / In Repair / Retired), purchase date, and notes.", body))
    story.append(Spacer(1, 10))
    img = Image(os.path.join(SHOTS, "assets-tab.png"), width=6.2 * inch, height=6.2 * inch * 600 / 800)
    img.hAlign = "CENTER"
    story.append(img)

    story.append(PageBreak())

    # ---------- Other 3 screenshots, 2 per row ----------
    story += section_header("Onboarding & Offboarding, Tickets, Knowledge Base")
    story.append(Paragraph(
        "Onboarding/offboarding checklists track per-employee progress against a standard template "
        "(Mosyle enrollment, SSO, Slack, Atlassian, 1Password, laptop handoff). Tickets cover intake and "
        "triage with priority/category/status. The Knowledge Base renders five macOS/Mosyle-specific "
        "playbooks I wrote directly from the app.", body))
    story.append(Spacer(1, 8))

    row1 = Table(
        [[
            [Image(os.path.join(SHOTS, "onboarding-tab.png"), width=2.9 * inch, height=2.9 * inch * 600 / 800),
             Paragraph("Onboarding & Offboarding", caption)],
            [Image(os.path.join(SHOTS, "tickets-tab.png"), width=2.9 * inch, height=2.9 * inch * 600 / 800),
             Paragraph("Helpdesk Tickets", caption)],
        ]],
        colWidths=[3.25 * inch, 3.25 * inch],
        style=TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP")]),
    )
    story.append(row1)
    story.append(Spacer(1, 10))

    kb_img = Image(os.path.join(SHOTS, "knowledge-base-tab.png"), width=4.2 * inch, height=4.2 * inch * 600 / 800)
    kb_row = Table([[kb_img, Paragraph(
        "<b>Knowledge Base</b><br/><br/>"
        "Five playbooks, written the way I'd actually hand them to a new IT hire on day one:<br/>"
        "&bull; New Hire Onboarding<br/>"
        "&bull; Offboarding Checklist<br/>"
        "&bull; MDM Laptop Deployment (Mosyle)<br/>"
        "&bull; Ticket Triage SOP<br/>"
        "&bull; Network Troubleshooting (macOS)",
        body,
    )]], colWidths=[4.4 * inch, 2.1 * inch], style=TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP")]))
    story.append(kb_row)

    story.append(PageBreak())

    # ---------- Architecture ----------
    story += section_header("Architecture")
    story.append(arrow_flow(["Browser", "CloudFront\n(PriceClass_100)", "S3\n(static SPA)"]))
    story.append(Spacer(1, 10))
    story.append(arrow_flow(["Browser", "API Gateway\n(HTTP API)", "Lambda x3\n(Python 3.12)", "DynamoDB x3\n(1 RCU/WCU)"],
                             box_w=112, gap=22, font_size=8))
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "Fully serverless, no fixed-hourly-cost resources (no NAT Gateway, VPC, RDS, or ALB). "
        "Infrastructure is defined as a single CloudFormation template and deployed via the AWS CLI "
        "(<font face='Courier'>cloudformation package</font> / <font face='Courier'>deploy</font>) "
        "rather than CDK/SAM, since the build machine had no Node.js toolchain installed.",
        body,
    ))
    story.append(Spacer(1, 12))

    # ---------- Decisions / cost ----------
    story += section_header("Technical decisions worth noting")
    bullets = [
        "<b>DynamoDB at provisioned 1 RCU / 1 WCU per table</b> (3/3 total) &mdash; inside AWS's "
        "<i>always-free</i> allowance (25/25), not just the 12-month one.",
        "<b>API Gateway HTTP API instead of REST API</b> &mdash; ~70% cheaper per request beyond free "
        "tier, simpler built-in CORS.",
        "<b>CloudFront PriceClass_100</b> &mdash; cheapest edge-location tier, sufficient for a demo.",
        "<b>Least-privilege IAM</b> &mdash; each Lambda's execution role is scoped to only its own "
        "DynamoDB table.",
        "Two real bugs found and fixed during deployment: HTTP API's automatic CORS doesn't intercept "
        "<font face='Courier'>OPTIONS</font> when a route uses <font face='Courier'>ANY</font> (fixed "
        "with an early return in each Lambda); DynamoDB's <font face='Courier'>Decimal</font> type isn't "
        "JSON-serializable by default (fixed with a custom JSON encoder).",
    ]
    for b in bullets:
        story.append(Paragraph(f"&bull; {b}", body))
        story.append(Spacer(1, 4))

    story.append(Spacer(1, 8))
    story += section_header("What I'd add next")
    story.append(Paragraph(
        "Kept out of scope on purpose, to keep this honest about what it is: Cognito-based auth instead "
        "of a shared-secret header; a dedicated least-privilege IAM deploy user instead of root "
        "credentials; CI/CD instead of a manual deploy script.",
        body,
    ))

    story.append(Spacer(1, 16))
    story.append(HRFlowable(width="100%", thickness=0.75, color=LINE))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "Bryan Cole &nbsp;&bull;&nbsp; bryancole84@gmail.com &nbsp;&bull;&nbsp; "
        "github.com/bcole84/clockwork-it-ops-console",
        muted,
    ))

    doc.build(story)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    build()
