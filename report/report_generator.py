from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import pagesizes
import os
from datetime import datetime


def generate_report(filename, findings, report_folder, risk_score, risk_level, owasp_summary):

    if not os.path.exists(report_folder):
        os.makedirs(report_folder)

    path = os.path.join(report_folder, f"{filename}_security_report.pdf")

    doc = SimpleDocTemplate(path, pagesize=pagesizes.A4)
    styles = getSampleStyleSheet()
    elements = []

    # ---------------- EXECUTIVE SUMMARY ---------------- #
    elements.append(Paragraph("AndroSentry Security Assessment Report", styles["Title"]))
    elements.append(Spacer(1, 20))

    elements.append(Paragraph("Executive Summary", styles["Heading2"]))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph(f"Scan Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles["Normal"]))
    elements.append(Paragraph(f"Total Findings: {len(findings)}", styles["Normal"]))
    elements.append(Paragraph(f"Risk Score: {risk_score}", styles["Normal"]))
    elements.append(Paragraph(f"Overall Risk Level: {risk_level}", styles["Normal"]))
    elements.append(Spacer(1, 20))

    elements.append(PageBreak())

    # ---------------- OWASP SUMMARY ---------------- #
    elements.append(Paragraph("OWASP Category Summary", styles["Heading2"]))
    elements.append(Spacer(1, 10))

    if not owasp_summary:
        elements.append(Paragraph("No OWASP-mapped vulnerabilities detected.", styles["Normal"]))
    else:
        for category, count in owasp_summary.items():
            elements.append(Paragraph(f"{category}: {count} issue(s)", styles["Normal"]))
            elements.append(Spacer(1, 5))

    elements.append(PageBreak())

    # ---------------- DETAILED FINDINGS ---------------- #
    elements.append(Paragraph("Detailed Vulnerability Findings", styles["Heading2"]))
    elements.append(Spacer(1, 10))

    if not findings:
        elements.append(Paragraph("No security issues detected.", styles["Normal"]))
    else:
        for i, f in enumerate(findings, 1):
            elements.append(Paragraph(f"{i}. {f['title']}", styles["Heading3"]))
            elements.append(Spacer(1, 5))
            elements.append(Paragraph(f"Description: {f['description']}", styles["Normal"]))
            elements.append(Paragraph(f"Severity: {f['severity']}", styles["Normal"]))
            elements.append(Paragraph(f"OWASP Category: {f['owasp']}", styles["Normal"]))
            elements.append(Paragraph(f"Remediation: {f['remediation']}", styles["Normal"]))
            elements.append(Spacer(1, 15))

    doc.build(elements)
    return path
