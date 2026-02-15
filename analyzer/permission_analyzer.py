DANGEROUS = {
    "android.permission.READ_SMS",
    "android.permission.SEND_SMS",
    "android.permission.READ_CONTACTS",
    "android.permission.ACCESS_FINE_LOCATION",
    "android.permission.RECORD_AUDIO",
    "android.permission.CAMERA"
}

def analyze_permissions(permissions):
    findings = []

    dangerous_found = [p for p in permissions if p in DANGEROUS]

    if dangerous_found:
        findings.append({
            "title": "Dangerous Permissions Detected",
            "description": "The application requests high-risk permissions.",
            "severity": "High",
            "owasp": "M1: Improper Platform Usage",
            "remediation": "Request only essential permissions and follow least privilege principle."
        })

    if len(permissions) > 20:
        findings.append({
            "title": "Excessive Permission Count",
            "description": f"Application requests {len(permissions)} permissions.",
            "severity": "Medium",
            "owasp": "M1: Improper Platform Usage",
            "remediation": "Review and remove unnecessary permissions."
        })

    return findings
