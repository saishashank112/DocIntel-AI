from services.document_service import safe_json_parse

def parse_grounding(raw: str) -> dict:
    """Parse factual grounding verification verdict."""
    return safe_json_parse(raw, {
        "verdict": "Partially Grounded",
        "confidence": "Low",
        "explanation": "Could not parse grounding response."
    })

def grounding_badge(verdict: str, confidence: str) -> tuple[str, str]:
    """Return icon and brand hex color for the grounding badge."""
    v = verdict.lower()
    if "fully" in v:
        return "🟢", "#10b981"
    elif "partially" in v:
        return "🟡", "#f59e0b"
    elif "reasoned" in v:
        return "🔵", "#6366f1"
    else:
        return "🔴", "#ef4444"
