from prompts.prompt_registry import get_prompt
from services.reranker_service import get_reranker
from config.settings import MAX_HISTORY_TURNS

def expand_query(query: str, llm) -> str:
    """Expand the query with semantic synonyms for richer retrieval."""
    try:
        prompt_tpl = get_prompt("expand")
        response = llm.invoke(prompt_tpl.format(query=query))
        keywords = response.content.strip()
        return f"{query} {keywords}"
    except Exception:
        return query

def hybrid_search(query: str, expanded_query: str, chroma_db, bm25, all_chunks, top_k=5):
    """Top-15 hybrid retrieval → cross-encoder rerank → Top-5."""
    # Semantic search
    chroma_results = chroma_db.similarity_search(expanded_query, k=15)

    # BM25 keyword search on original query
    tokenized_q = query.lower().split()
    bm25_scores = bm25.get_scores(tokenized_q)
    top_bm25_idx = sorted(range(len(bm25_scores)), key=lambda i: bm25_scores[i], reverse=True)[:15]
    bm25_results = [all_chunks[i] for i in top_bm25_idx]

    # Merge + deduplicate
    merged = {}
    for doc in chroma_results + bm25_results:
        cid = doc.metadata.get("chunk_id")
        if cid not in merged:
            merged[cid] = doc
    unique_docs = list(merged.values())

    if not unique_docs:
        return []

    # Cross-Encoder reranking
    reranker = get_reranker()
    pairs = [[query, doc.page_content] for doc in unique_docs]
    scores = reranker.predict(pairs)
    ranked = sorted(zip(unique_docs, scores), key=lambda x: x[1], reverse=True)
    return [doc for doc, _ in ranked[:top_k]]

def format_context(docs) -> str:
    parts = []
    for i, doc in enumerate(docs):
        page = doc.metadata.get("page_number", "?")
        parts.append(f"[Source {i+1} | Page {page}]\n{doc.page_content}")
    return "\n\n---\n\n".join(parts)

def format_history(history: list) -> str:
    if not history:
        return "No previous conversation."
    lines = []
    for turn in history[-MAX_HISTORY_TURNS:]:
        lines.append(f"User: {turn['q']}")
        lines.append(f"Assistant: {turn['a'][:300]}...")
    return "\n".join(lines)
