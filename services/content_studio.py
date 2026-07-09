import json

PROMPT_STUDIO = """You are a professional content creator and copywriting assistant.
Using the document profile and details, generate the requested creative output format: {content_type}.

RULES:
- Maintain high semantic fidelity using the facts inside the document.
- Adjust tone, formatting, and layout to match a premium example of the requested format.
- Output ONLY the generated text. Do not write introductory prose or notes.

DOCUMENT DETAILS:
{details}

OUTPUT CONTENT TYPE: {content_type}
Your content:"""

def generate_studio_content(content_type: str, details: dict, llm) -> str:
    """Generate professional formatted copy based on document metadata."""
    details_str = json.dumps(details, indent=2)
    response = llm.invoke(PROMPT_STUDIO.format(content_type=content_type, details=details_str))
    return response.content
