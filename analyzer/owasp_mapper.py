def group_by_owasp(findings):
    grouped = {}

    for finding in findings:
        category = finding.get("owasp", "Uncategorized")

        if category not in grouped:
            grouped[category] = []

        grouped[category].append(finding)

    return grouped
