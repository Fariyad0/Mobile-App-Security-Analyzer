def check_cleartext(app):
    findings = []

    if app.get_attribute_value("application", "usesCleartextTraffic") == "true":
        findings.append({
            "title": "Cleartext Traffic Allowed",
            "description": "App allows HTTP traffic.",
            "severity": "High",
            "owasp": "M3: Insecure Communication",
            "remediation": "Disable cleartext traffic and enforce HTTPS."
        })

    return findings
