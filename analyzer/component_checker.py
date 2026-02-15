def check_exported_components(app):
    findings = []

    activities = app.get_activities()

    for activity in activities:
        if app.get_activity_exported(activity):
            findings.append({
                "title": "Exported Activity Detected",
                "description": f"Activity {activity} is exported.",
                "severity": "Medium",
                "owasp": "M1: Improper Platform Usage",
                "remediation": "Set exported=false unless explicitly required."
            })

    return findings
