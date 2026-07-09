from config.settings import INTENT_META
from prompts.prompt_registry import get_prompt

def classify_intent(question: str, llm) -> str:
    """Classify the user's question into a routing intent."""
    valid_intents = set(INTENT_META.keys())
    try:
        prompt_tpl = get_prompt("intent")
        response = llm.invoke(prompt_tpl.format(question=question))
        intent = response.content.strip().lower().replace('"', '').replace("'", "")
        return intent if intent in valid_intents else "fact_lookup"
    except Exception:
        return "fact_lookup"
