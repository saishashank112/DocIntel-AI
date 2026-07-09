import streamlit as st
import json
from config.settings import INTENT_META
from services.llm_service import get_llm
from routing.intent_classifier import classify_intent
from routing.response_router import answer_with_intent
from rag.grounding import grounding_badge, parse_grounding
from prompts.prompt_registry import get_prompt
from providers.base_provider import (
    PlatformError,
    ProviderConnectionError,
    ProviderConfigurationError,
    ProviderModelError,
    RetrievalError,
    ValidationError
)

def render_error_card(error_type, title, description, suggested_fix, technical_details=None):
    """Render a dedicated beautiful SaaS error card with appropriate icon and style."""
    icons = {
        "Connection Error": "🔌",
        "Configuration Error": "🔑",
        "Model Error": "🤖",
        "Retrieval Error": "📚",
        "Validation Error": "⚠️"
    }
    class_map = {
        "Connection Error": "connection",
        "Configuration Error": "configuration",
        "Model Error": "model",
        "Retrieval Error": "retrieval",
        "Validation Error": "validation"
    }
    icon = icons.get(error_type, "⚠️")
    cls = class_map.get(error_type, "validation")
    
    card_html = f"""
    <div class="error-card error-card-{cls}">
        <div>
            <span class="error-icon-span">{icon}</span>
            <span class="error-title-text">{title}</span>
        </div>
        <p class="error-card-desc">{description}</p>
        <div class="error-card-fix">
            <strong>Suggested Fix:</strong>
            <p>{suggested_fix}</p>
        </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)
    if technical_details:
        with st.expander("🔍 Show Technical Details", expanded=False):
            st.code(technical_details, language="text")

def render_chat():
    """Render the main conversation panel, suggestions, and chat input."""
    # ── Render chat history ──
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            if "error_type" in msg:
                render_error_card(
                    error_type=msg["error_type"],
                    title=msg["error_title"],
                    description=msg["error_description"],
                    suggested_fix=msg["error_suggested_fix"],
                    technical_details=msg.get("error_technical")
                )
                continue

            # Intent badge
            if "intent" in msg:
                meta = INTENT_META.get(msg["intent"], {})
                label = meta.get("label", msg["intent"])
                color = meta.get("color", "#475569")
                st.markdown(
                    f'<span class="intent-badge">{label}</span>',
                    unsafe_allow_html=True
                )
            st.markdown(msg["content"])

            # Grounding badge
            if "grounding" in msg:
                g = msg["grounding"]
                icon, color = grounding_badge(g.get("verdict", ""), g.get("confidence", ""))
                verdict = g.get("verdict", "Unknown")
                conf    = g.get("confidence", "")
                expl    = g.get("explanation", "")
                st.markdown(
                    f'<div class="ground-badge">'
                    f'{icon} {verdict} · {conf} Confidence</div>',
                    unsafe_allow_html=True
                )
                if expl:
                    st.caption(expl)

            # Source cards (collapsed by default)
            if msg.get("sources"):
                with st.expander(f"📚 Sources & Evidence ({len(msg['sources'])} chunks)", expanded=False):
                    for i, doc in enumerate(msg["sources"]):
                        page = doc.metadata.get("page_number", "?")
                        snippet = doc.page_content[:400].replace("\n", " ")
                        st.markdown(
                            f'<div class="source-card"><b>Source {i+1} · Page {page}</b><br>'
                            f'<span style="color:#000000;">{snippet}{"..." if len(doc.page_content) > 400 else ""}</span></div>',
                            unsafe_allow_html=True
                        )

    # ── Follow-up chips ──
    if st.session_state.followups:
        st.markdown("<p style='color:#000000;font-size:13px;margin-bottom:8px;margin-top:16px;'>💡 Suggested follow-ups:</p>", unsafe_allow_html=True)
        cols = st.columns(len(st.session_state.followups))
        for i, fu in enumerate(st.session_state.followups):
            if cols[i].button(fu, key=f"fu_{i}", use_container_width=True):
                st.session_state.suggested_prompt = fu
                st.rerun()

    # ── Chat input ──
    user_input = st.chat_input("Ask anything about the document...")
    st.markdown(
        "<div style='text-align: center; font-size: 11px; color: #000000; margin-top: -15px; margin-bottom: 15px;'>"
        "📎 Attach Documents · 🎤 Voice Mode placeholder · Drag-and-drop PDF anywhere to upload</div>",
        unsafe_allow_html=True
    )
    if "suggested_prompt" in st.session_state:
        user_input = st.session_state.pop("suggested_prompt")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            try:
                llm = get_llm()

                with st.status("🧠 AI Orchestrator Pipeline", expanded=True) as status:
                    # Step 1: Query intent classification
                    status.write("⏳ Classifying query intent...")
                    intent = classify_intent(user_input, llm)
                    status.write(f"✓ Intent Classified: `{intent.upper()}`")
                    
                    # Step 2: Retrieval & Context assembly
                    status.write("⏳ Retrieving document chunks...")
                    from rag.retrieval import expand_query, hybrid_search, format_context
                    
                    expanded = expand_query(user_input, llm)
                    status.write("✓ Document Retrieved")
                    
                    sources = hybrid_search(user_input, expanded, st.session_state.chroma_db, st.session_state.bm25, st.session_state.all_chunks, top_k=5)
                    
                    is_creative = ("generation" in intent or "post" in intent or "letter" in intent or "introduction" in intent or "writing" in intent or "content" in intent)
                    if (intent in ("skill_extraction", "career_analysis", "project_extraction", "timeline_extraction") or is_creative) and st.session_state.resume_data:
                        extra_context = f"[Structured Resume Data]\n{json.dumps(st.session_state.resume_data, indent=2)}\n\n"
                    else:
                        extra_context = ""
                    context = extra_context + format_context(sources)
                    status.write("✓ Context Built")
                    
                    # Step 3: Response generation
                    status.write("⏳ Generating Response...")
                    from prompts.prompt_registry import get_prompt
                    from rag.retrieval import format_history
                    
                    history_str = format_history(st.session_state.conversation_history)
                    
                    if intent == "document_summary":
                        profile_str = json.dumps(st.session_state.doc_profile, indent=2)
                        prompt_tpl = get_prompt("summary_intent")
                        response = llm.invoke(prompt_tpl.format(profile=profile_str, question=user_input))
                        answer = response.content
                    else:
                        prompt_tpl = get_prompt("rag_answer")
                        prompt = prompt_tpl.format(
                            history=history_str,
                            context=context,
                            question=user_input,
                            intent=intent
                        )
                        response = llm.invoke(prompt)
                        answer = response.content
                    status.write("✓ Response Generated")
                    
                    # Step 4: Grounding check
                    grounding = {}
                    if context:
                        status.write("⏳ Verifying Grounding...")
                        grounding_tpl = get_prompt("grounding")
                        ground_resp = llm.invoke(grounding_tpl.format(context=context[:3000], answer=answer))
                        grounding = parse_grounding(ground_resp.content)
                        status.write("✓ Grounding Verified")
                    
                    # Step 5: Follow-ups
                    status.write("⏳ Generating follow-ups...")
                    ctx_for_fu = context if context else json.dumps(st.session_state.doc_profile)
                    fu_tpl = get_prompt("followups")
                    fu_resp = llm.invoke(fu_tpl.format(context=ctx_for_fu[:2000], question=user_input))
                    followups = [l.strip() for l in fu_resp.content.split("\n") if l.strip()][:3]
                    st.session_state.followups = followups
                    
                    status.update(label="✨ Response generation pipeline complete", state="complete", expanded=False)

                # Render response
                meta  = INTENT_META.get(intent, {"label": intent, "color": "#475569"})
                label = meta["label"]
                color = meta["color"]
                st.markdown(
                    f'<span class="intent-badge">{label}</span>',
                    unsafe_allow_html=True
                )
                st.markdown(answer)

                if sources:
                    with st.expander(f"📚 Sources & Evidence ({len(sources)} chunks)", expanded=False):
                        for i, doc in enumerate(sources):
                            page = doc.metadata.get("page_number", "?")
                            snippet = doc.page_content[:400].replace("\n", " ")
                            st.markdown(
                                f'<div class="source-card"><b>Source {i+1} · Page {page}</b><br>'
                                f'<span style="color:#000000;">{snippet}{"..." if len(doc.page_content) > 400 else ""}</span></div>',
                                unsafe_allow_html=True
                            )

                if grounding:
                    icon, gcolor = grounding_badge(grounding.get("verdict", ""), grounding.get("confidence", ""))
                    st.markdown(
                        f'<div class="ground-badge">'
                        f'{icon} {grounding.get("verdict","Unknown")} · {grounding.get("confidence","")} Confidence</div>',
                        unsafe_allow_html=True
                    )
                    if grounding.get("explanation"):
                        st.caption(grounding["explanation"])

                st.session_state.conversation_history.append({"q": user_input, "a": answer})
                st.session_state.messages.append({
                    "role":      "assistant",
                    "content":   answer,
                    "intent":    intent,
                    "grounding": grounding,
                    "sources":   sources,
                })
                st.rerun()

            except PlatformError as e:
                err_type = "Validation Error"
                err_title = "Action Failed"
                err_desc = str(e)
                err_fix = "Please try again."
                
                if isinstance(e, ProviderConnectionError):
                    err_type = "Connection Error"
                    err_title = "Could not connect to model provider."
                    if "ollama" in st.session_state.settings_provider.lower():
                        err_title = "Could not connect to Ollama."
                        err_desc = "DocIntel was unable to connect to your local Ollama instance."
                        err_fix = "1. Run `ollama serve` in a terminal to start the service.\n2. Verify the model is pulled using `ollama list`.\n3. Make sure the port 11434 is accessible."
                    else:
                        err_desc = f"Network connection to {st.session_state.settings_provider} failed."
                        err_fix = "1. Check your internet connection.\n2. Verify that the provider API endpoints are online."
                elif isinstance(e, ProviderConfigurationError):
                    err_type = "Configuration Error"
                    err_title = f"{st.session_state.settings_provider} Configuration Error"
                    err_desc = str(e)
                    err_fix = "1. Navigate to Settings Panel.\n2. Verify that your API Key is correctly entered.\n3. Test the connection before returning to chat."
                elif isinstance(e, ProviderModelError):
                    err_type = "Model Error"
                    err_title = "Selected Model Unavailable"
                    err_desc = str(e)
                    if "ollama" in st.session_state.settings_provider.lower():
                        err_fix = f"Run: `ollama pull {st.session_state.settings_model}` in a terminal."
                    else:
                        err_fix = "Verify the model name or change to a different model in the Settings Panel."
                elif isinstance(e, RetrievalError):
                    err_type = "Retrieval Error"
                    err_title = "Document Query Retrieval Failed"
                    err_desc = str(e)
                    err_fix = "1. Try clearing the document and re-uploading.\n2. Verify if the PDF content is readable/extractable."
                
                render_error_card(
                    error_type=err_type,
                    title=err_title,
                    description=err_desc,
                    suggested_fix=err_fix,
                    technical_details=e.technical_details or str(e)
                )
                
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": "Error occurred during execution.",
                    "error_type": err_type,
                    "error_title": err_title,
                    "error_description": err_desc,
                    "error_suggested_fix": err_fix,
                    "error_technical": e.technical_details or str(e)
                })

