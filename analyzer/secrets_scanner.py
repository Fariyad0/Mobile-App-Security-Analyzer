import re

SECRET_PATTERNS = [
    r'AIza[0-9A-Za-z-_]{35}',  # Google API
    r'sk_live_[0-9a-zA-Z]{24}',  # Stripe
    r'AKIA[0-9A-Z]{16}'  # AWS
]

def scan_secrets(strings):
    findings = []

    for s in strings:
        for pattern in SECRET_PATTERNS:
            if re.search(pattern, s):
                findings.append({
                    "title": "Hardcoded API Key Found",
                    "description": "Potential hardcoded secret detected.",
                    "severity": "High",
                    "owasp": "M2: Insecure Data Storage",
                    "remediation": "Store secrets securely using keystore or backend."
                })

    return findings
