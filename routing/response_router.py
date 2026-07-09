import json
from prompts.prompt_registry import get_prompt
from rag.retrieval import expand_query, hybrid_search, format_context, format_history

def answer_with_intent(intent, question, llm, doc_profile, resume_data, chroma_db, bm25, all_chunks, history):
    """Route to the correct answer strategy based on intent."""
    sources = []
    context = ""

    # ── DOCUMENT-LEVEL INTENTS (no retrieval needed) ──
    if intent == "document_summary":
        profile_str = json.dumps(doc_profile, indent=2)
        prompt_tpl = get_prompt("summary_intent")
        response = llm.invoke(prompt_tpl.format(profile=profile_str, question=question))
        return response.content, sources, context

    # ── RESUME-ENRICHED INTENTS & CREATIVE TASKS ──
    is_creative = ("generation" in intent or "post" in intent or "letter" in intent or "introduction" in intent or "writing" in intent or "content" in intent)
    if (intent in ("skill_extraction", "career_analysis", "project_extraction", "timeline_extraction") or is_creative) and resume_data:
        # Blend resume data into context for richer answers / templates
        extra_context = f"[Structured Resume Data]\n{json.dumps(resume_data, indent=2)}\n\n"
    else:
        extra_context = ""

    # ── RETRIEVAL ──
    expanded = expand_query(question, llm)
    sources = hybrid_search(question, expanded, chroma_db, bm25, all_chunks, top_k=5)
    context = extra_context + format_context(sources)
    history_str = format_history(history)

    prompt_tpl = get_prompt("rag_answer")
    prompt = prompt_tpl.format(
        history=history_str,
        context=context,
        question=question,
        intent=intent
    )
    response = llm.invoke(prompt)
    return response.content, sources, context
