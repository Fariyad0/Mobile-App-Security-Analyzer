from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from androguard.core.bytecodes.apk import APK
import os
import sqlite3
from datetime import datetime

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
REPORT_FOLDER = "reports"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# ---------------- DATABASE INIT (SAFE MIGRATION) ---------------- #

def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Create base table if not exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            scan_date TEXT,
            total_findings INTEGER,
            report_path TEXT
        )
    """)

    # Check existing columns
    cursor.execute("PRAGMA table_info(scans)")
    columns = [column[1] for column in cursor.fetchall()]

    # Add missing columns safely
    if "risk_score" not in columns:
        cursor.execute("ALTER TABLE scans ADD COLUMN risk_score INTEGER DEFAULT 0")

    if "risk_level" not in columns:
        cursor.execute("ALTER TABLE scans ADD COLUMN risk_level TEXT DEFAULT 'Low'")

    conn.commit()
    conn.close()


# ---------------- RISK CALCULATION ---------------- #

def calculate_risk(findings):
    score = 0

    for f in findings:
        if f["severity"] == "High":
            score += 10
        elif f["severity"] == "Medium":
            score += 6
        else:
            score += 3

    if score >= 40:
        level = "Critical"
    elif score >= 25:
        level = "High"
    elif score >= 10:
        level = "Medium"
    else:
        level = "Low"

    return score, level


# ---------------- HOME / SCAN ---------------- #

@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        file = request.files.get("apkfile")

        if not file:
            return render_template("dashboard.html", error="No file selected.")

        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        try:
            apk = APK(filepath)

            findings = []

            permissions = apk.get_permissions()

            if len(permissions) > 20:
                findings.append({
                    "title": "Excessive Permissions",
                    "description": "App requests too many permissions.",
                    "severity": "Medium",
                    "owasp": "M1: Improper Platform Usage",
                    "remediation": "Remove unnecessary permissions."
                })

            debuggable = apk.get_attribute_value("application", "debuggable")
            if debuggable == "true":
                findings.append({
                    "title": "Debug Mode Enabled",
                    "description": "App is debuggable.",
                    "severity": "High",
                    "owasp": "M7: Code Quality",
                    "remediation": "Disable debug mode in production."
                })

            # Calculate Risk
            risk_score, risk_level = calculate_risk(findings)

            # Create report folder
            if not os.path.exists(REPORT_FOLDER):
                os.makedirs(REPORT_FOLDER)

            report_filename = file.filename + "_report.txt"
            report_path = os.path.join(REPORT_FOLDER, report_filename)

            # Generate simple text report
            with open(report_path, "w") as f:
                f.write("AndroSentry Security Report\n\n")
                f.write(f"Scan Date: {datetime.now()}\n")
                f.write(f"Total Findings: {len(findings)}\n")
                f.write(f"Risk Score: {risk_score}\n")
                f.write(f"Risk Level: {risk_level}\n\n")

                for item in findings:
                    f.write(f"Title: {item['title']}\n")
                    f.write(f"Severity: {item['severity']}\n")
                    f.write(f"OWASP: {item['owasp']}\n")
                    f.write(f"Remediation: {item['remediation']}\n\n")

            # Save to database
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO scans
                (filename, scan_date, total_findings, report_path, risk_score, risk_level)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                file.filename,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                len(findings),
                report_filename,
                risk_score,
                risk_level
            ))

            conn.commit()
            conn.close()

            return redirect(url_for("analysis"))

        except Exception as e:
            return render_template("dashboard.html", error=str(e))

    return render_template("dashboard.html")


# ---------------- SCAN HISTORY ---------------- #

@app.route("/analysis")
def analysis():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM scans ORDER BY id DESC")
    scans = cursor.fetchall()

    conn.close()

    return render_template("analysis.html", scans=scans)


# ---------------- REPORT DOWNLOAD ---------------- #

@app.route("/reports/<filename>")
def download_report(filename):
    return send_from_directory(REPORT_FOLDER, filename)


# ---------------- MAIN ---------------- #

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
