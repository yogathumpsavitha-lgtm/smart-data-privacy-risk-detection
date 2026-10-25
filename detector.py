import re


SENSITIVE_PATTERNS = {
    "Email Address": {
        "pattern": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        "risk": "Medium",
    },
    "Phone Number": {
        "pattern": r"(?<!\d)(?:\+91[-\s]?)?[6-9]\d{9}(?!\d)",
        "risk": "High",
    },
    "Indian PAN": {
        "pattern": r"\b[A-Z]{5}\d{4}[A-Z]\b",
        "risk": "High",
    },
    "Employee ID": {
        "pattern": r"\bEMP[-_]?\d{4,8}\b",
        "risk": "Medium",
    },
}


def detect_sensitive_data(text):
    """
    Detect possible sensitive information in text.

    Returns findings with their type, location, risk level,
    confidence, and matched value.
    """
    findings = []

    if not isinstance(text, str) or not text:
        return findings

    for category, details in SENSITIVE_PATTERNS.items():
        for match in re.finditer(details["pattern"], text):
            findings.append({
                "type": category,
                "value": match.group(),
                "start": match.start(),
                "end": match.end(),
                "risk": details["risk"],
                "confidence": 0.95,
            })

    findings.sort(key=lambda item: item["start"])

    return findings