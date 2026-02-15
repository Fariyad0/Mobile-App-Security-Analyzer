# 📱 Mobile App Security Analyzer

A Static Application Security Testing (SAST) tool for Android APK files built using Python and Androguard.

This tool analyzes Android applications and detects common security vulnerabilities based on OWASP Mobile Top 10 guidelines. It generates a structured security report along with a calculated risk score and risk level.

---

## 🚀 Project Overview

Mobile App Security Analyzer performs static analysis on Android APK files and identifies potential security misconfigurations such as:

- Insecure target SDK versions
- Debuggable mode enabled
- Exported components without protection
- Dangerous permissions
- Network security weaknesses

The tool generates:
- Structured vulnerability report
- Risk Score calculation
- Risk Level classification
- Executive Summary
- Downloadable PDF report

---

## 🛠 Features

✔ APK Upload & Analysis  
✔ Detects targetSdkVersion issues  
✔ Detects debuggable flag  
✔ Detects exported activities/services  
✔ Risk Score Calculation  
✔ Risk Level Classification (Low / Medium / High)  
✔ OWASP Mobile Top 10 Mapping  
✔ Executive Summary in PDF  
✔ Structured PDF Report Generation  

---

## 🏗 Architecture
User Upload APK
↓
Scanner Module (Androguard)
↓
Vulnerability Detection
↓
Risk Engine (Score Calculation)
↓
Report Generator (PDF)
↓
Final Security Report

##
---

## 📦 Technologies Used

- Python 3.9+
- Flask (Web Interface)
- Androguard (APK Analysis)
- ReportLab (PDF Generation)
- HTML/CSS (Frontend UI)

---

## ⚙️ Installation Guide

### 1️⃣ Clone Repository

```bash
git clone https://github.com/Fariyad0/Mobile-App-Security-Analyzer.git
cd Mobile-App-Security-Analyzer

### 2️⃣ Install Dependencies
pip install -r requirements.txt

#3️⃣ Run Application
python app.py

#4️⃣ Open in Browser
The link showing in the terminal

###🔍 How It Works

User uploads APK file

Tool extracts AndroidManifest.xml

Scanner checks for:
        -targetSdkVersion
        -minSdkVersion
        -Debuggable flag
        -Exported components

Risk engine calculates total risk score
PDF report is generated
User downloads structured report

📊 Risk Score Calculation
Each vulnerability is assigned severity weight:
| Severity | Score |
| -------- | ----- |
| Low      | 1     |
| Medium   | 3     |
| High     | 5     |

🛡 OWASP Mobile Top 10 Mapping
| Vulnerability       | OWASP Category             |
| ------------------- | -------------------------- |
| Debuggable Enabled  | M7: Client Code Quality    |
| targetSdk < 28      | M2: Insecure Data Storage  |
| Exported Components | M3: Insecure Communication |

📄 Sample Output

The generated report includes:
-Executive Summary
-Total Vulnerabilities
-Risk Score
-Risk Level
-Detailed Findings Table
-Recommendations
-OWASP Mapping

📁 Project Structure:
Mobile-App-Security-Analyzer/
│
├── app.py
├── config.py
├── database.db
├── requirements.txt
├── README.md
│
├── analyzer/
│   ├── component_checker.py
│   ├── manifest_analyzer.py
│   ├── network_checker.py
│   ├── permission_analyzer.py
│   ├── secrets_scanner.py
│   ├── owasp_mapper.py
│   ├── owasp_summary.py
│   ├── risk_engine.py
│
├── reports/
│   └── report_generator.py
│
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── analysis.html
│   ├── reports.html
│
├── static/
│   ├── style.css
│   └── script.js
│
├── uploads/
│
└── sample_reports/
