def calculate_risk(findings):
    score = 0

    weights = {
        "High": 10,
        "Medium": 6,
        "Low": 3
    }

    for f in findings:
        severity = f.get("severity", "Low")
        score += weights.get(severity, 3)

    # Risk Level Classification
    if score >= 40:
        level = "Critical"
    elif score >= 25:
        level = "High"
    elif score >= 10:
        level = "Medium"
    else:
        level = "Low"

    return score, level
