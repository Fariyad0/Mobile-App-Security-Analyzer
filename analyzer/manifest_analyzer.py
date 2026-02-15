def check_manifest_security(apk):
    findings = []

    # Debuggable check
    debuggable = apk.get_attribute_value("application", "debuggable")
    if debuggable == "true":
        findings.append({
            "title": "Application is Debuggable",
            "description": "Debug mode is enabled. This exposes the app to runtime inspection.",
            "severity": "High",
            "owasp": "M7: Insufficient Code Quality",
            "remediation": "Disable android:debuggable in release builds."
        })

    # Backup enabled check
    backup = apk.get_attribute_value("application", "allowBackup")
    if backup == "true":
        findings.append({
            "title": "ADB Backup Enabled",
            "description": "Application allows device backup which may expose sensitive data.",
            "severity": "Medium",
            "owasp": "M2: Insecure Data Storage",
            "remediation": "Disable android:allowBackup for production builds."
        })

    min_sdk = apk.get_min_sdk_version()
    if min_sdk and int(min_sdk) < 23:
        findings.append({
            "title": "Low Minimum SDK Version",
            "description": f"Minimum SDK version is {min_sdk}, which may allow insecure legacy behavior.",
            "severity": "Medium",
            "owasp": "M1: Improper Platform Usage",
            "remediation": "Increase minSdkVersion to enforce modern security protections."
        })

    return findings
