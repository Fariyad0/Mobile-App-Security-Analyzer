def generate_owasp_summary(findings):
    summary = {}

    for f in findings:
        category = f.get("owasp", "Uncategorized")
        summary[category] = summary.get(category, 0) + 1

    return summary
