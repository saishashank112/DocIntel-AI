from utils.prompt_loader import load_prompt

PROMPTS = {
    "doc_overview":   lambda: load_prompt("doc_overview.txt"),
    "resume_extract": lambda: load_prompt("resume_extract.txt"),
    "intent":         lambda: load_prompt("intent.txt"),
    "expand":         lambda: load_prompt("expand.txt"),
    "summary_intent": lambda: load_prompt("summary_intent.txt"),
    "resume_intent":  lambda: load_prompt("resume_intent.txt"),
    "rag_answer":     lambda: load_prompt("rag_answer.txt"),
    "grounding":      lambda: load_prompt("grounding.txt"),
    "followups":      lambda: load_prompt("followups.txt"),
}

def get_prompt(name: str) -> str:
    """Retrieve the prompt text by name from registry."""
    if name in PROMPTS:
        return PROMPTS[name]()
    raise ValueError(f"Prompt '{name}' not found in registry.")
