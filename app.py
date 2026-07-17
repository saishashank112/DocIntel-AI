import streamlit as st
import json

# Import layouts and styling
from ui.styling import apply_custom_css
from ui.sidebar import render_sidebar
from ui.chat import render_chat

# Import feature engines and services
from services.llm_service import get_llm
from services.interview_engine import generate_interview_questions, evaluate_interview_answer
from services.persona_engine import generate_twin_response
from services.content_studio import generate_studio_content
from services.knowledge_graph import render_knowledge_graph
from services.career_engine import generate_career_insights
from providers.base_provider import (
    PlatformError,
    ProviderConnectionError,
    ProviderConfigurationError,
    ProviderModelError,
    RetrievalError,
    ValidationError
)
from ui.chat import render_error_card

def handle_platform_error(e: PlatformError):
    """Translate and display PlatformError instances as beautiful SaaS error cards."""
    err_type = "Validation Error"
    err_title = "Action Failed"
    err_desc = str(e)
    err_fix = "Please try again."
    
    if isinstance(e, ProviderConnectionError):
        err_type = "Connection Error"
        err_title = "Could not connect to Ollama."
        is_ollama_provider = "ollama" in st.session_state.settings_provider.lower()
        is_ollama_embeddings = "ollama" in st.session_state.settings_embeddings.lower()
        
        if is_ollama_provider or is_ollama_embeddings:
            err_desc = "DocIntel was unable to connect to the local Ollama service endpoint."
            err_fix = (
                "1. **Running Locally?** Start the service with `ollama serve` in a terminal and verify the models are pulled using `ollama list`.\n"
                "2. **Running in the Cloud (Streamlit Cloud)?** Local Ollama is not accessible. Please:\n"
                "   - Go to the **Settings Panel** (under Navigation).\n"
                "   - Switch the **LLM Provider** to a cloud API provider (e.g. Gemini, OpenAI, Anthropic, OpenRouter).\n"
                "   - Switch the **Embedding Model** to 'Local Sentence-Transformers' under the **Embeddings** tab."
            )
        else:
            err_title = "Could not connect to model provider."
            err_desc = f"Network connection to {st.session_state.settings_provider} failed."
            err_fix = "1. Check your internet connection.\n2. Verify that the provider API endpoints are online."
    elif isinstance(e, ProviderConfigurationError):
        err_type = "Configuration Error"
        err_title = f"{st.session_state.settings_provider} Configuration Error"
        err_desc = str(e)
        err_fix = "1. Navigate to Settings Panel.\\n2. Verify that your API Key is correctly entered.\\n3. Test the connection before returning to chat."
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
        err_fix = "1. Try clearing the document and re-uploading.\\n2. Verify if the PDF content is readable/extractable."

    render_error_card(
        error_type=err_type,
        title=err_title,
        description=err_desc,
        suggested_fix=err_fix,
        technical_details=e.technical_details or str(e)
    )


# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="DocIntel AI Platform",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Session state initialization
for key, default in {
    "messages": [],
    "pdf_processed": False,
    "pdf_filename": "",
    "followups": [],
    "doc_profile": None,
    "resume_data": None,
    "chroma_db": None,
    "bm25": None,
    "all_chunks": None,
    "total_pages": 0,
    "conversation_history": [],
    "navigation": "💬 Chat Assistant",
    "settings_provider": "ollama",
    "settings_model": "llama3.2",
    "settings_embeddings": "Ollama nomic-embed-text",
    "settings_temperature": 0.0,
    "settings_max_history": 3,
    "settings_chunk_size": 1000,
    "settings_chunk_overlap": 200,
    "connection_tested_provider": "",
    "connection_status": None,
    "api_keys": {"openai": "", "anthropic": "", "grok": "", "gemini": "", "openrouter": ""},
    # Feature specific states
    "twin_mode": False,
    "interview_questions": None,
    "active_question_index": 0,
    "interview_history": [],
    "interview_eval": None
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# Render sidebar first so theme toggle is committed to session state
render_sidebar()

# Apply CSS AFTER sidebar so theme variable is correct
apply_custom_css()

from ui.styling import render_global_header
render_global_header()

nav = st.session_state.navigation

if nav == "⚙️ Settings Panel":
    st.markdown("<h1>⚙️ Platform Settings Center</h1>", unsafe_allow_html=True)
    st.markdown("Configure LLM Providers, API credentials, and advanced model temperature thresholds.")
    st.markdown("---")

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🔌 AI Provider",
        "🤖 Model Selection",
        "🔑 API Credentials",
        "🧠 Embeddings",
        "⚙️ Advanced Settings"
    ])

    with tab1:
        st.markdown("### AI Provider Backend")
        with st.container(border=True):
            st.session_state.settings_provider = st.selectbox(
                "Select LLM Provider",
                ["Ollama", "OpenAI", "Anthropic", "Gemini", "Grok", "OpenRouter"],
                index=["ollama", "openai", "anthropic", "gemini", "grok", "openrouter"].index(st.session_state.settings_provider.lower())
            )

    with tab2:
        st.markdown("### Model Selection")
        with st.container(border=True):
            provider_models = {
                "ollama": ["llama3.2", "qwen2.5", "mistral", "deepseek-r1"],
                "openai": ["gpt-4o", "gpt-4o-mini", "o1-mini"],
                "anthropic": ["claude-3-5-sonnet-20241022", "claude-3-opus-20240229"],
                "gemini": ["gemini-1.5-flash", "gemini-1.5-pro"],
                "grok": ["grok-2-1212"],
                "openrouter": ["google/gemini-2.0-flash-exp:free", "meta-llama/llama-3.3-70b-instruct:free"]
            }
            current_models = provider_models.get(st.session_state.settings_provider.lower(), ["custom-model"])
            st.session_state.settings_model = st.selectbox(
                "Select Model",
                current_models,
                index=0 if st.session_state.settings_model not in current_models else current_models.index(st.session_state.settings_model)
            )

    with tab3:
        st.markdown("### API Keys & Credentials")
        keys = st.session_state.api_keys
        with st.container(border=True):
            col1, col2 = st.columns(2)
            with col1:
                keys["openai"] = st.text_input("OpenAI API Key", value=keys.get("openai", ""), type="password")
                keys["anthropic"] = st.text_input("Anthropic API Key", value=keys.get("anthropic", ""), type="password")
                keys["grok"] = st.text_input("Grok/xAI API Key", value=keys.get("grok", ""), type="password")
            with col2:
                keys["gemini"] = st.text_input("Gemini API Key", value=keys.get("gemini", ""), type="password")
                keys["openrouter"] = st.text_input("OpenRouter API Key", value=keys.get("openrouter", ""), type="password")
        st.session_state.api_keys = keys

    with tab4:
        st.markdown("### Embeddings Engine")
        with st.container(border=True):
            st.session_state.settings_embeddings = st.selectbox(
                "Select Embedding Model",
                ["Ollama nomic-embed-text", "Local Sentence-Transformers (all-MiniLM-L6-v2)"],
                index=0 if "nomic" in st.session_state.settings_embeddings else 1
            )

    with tab5:
        st.markdown("### Advanced Platform Tuning")
        with st.container(border=True):
            st.session_state.settings_temperature = st.slider(
                "Temperature",
                min_value=0.0,
                max_value=1.0,
                value=st.session_state.settings_temperature,
                step=0.1,
                help="Higher values mean more creative but less factual output."
            )
            st.session_state.settings_max_history = st.number_input(
                "Max Conversation History turns",
                min_value=1,
                max_value=10,
                value=st.session_state.settings_max_history,
                step=1,
                help="Number of turns to remember in conversation history."
            )
            col_c1, col_c2 = st.columns(2)
            with col_c1:
                st.session_state.settings_chunk_size = st.number_input(
                    "RAG Chunk Size",
                    min_value=100,
                    max_value=5000,
                    value=st.session_state.settings_chunk_size,
                    step=100,
                    help="Target chunk size for document splitting."
                )
            with col_c2:
                st.session_state.settings_chunk_overlap = st.number_input(
                    "RAG Chunk Overlap",
                    min_value=0,
                    max_value=1000,
                    value=st.session_state.settings_chunk_overlap,
                    step=50,
                    help="Overlap size for splitting chunks."
                )

    # Validation Checks before Connection Test
    selected_p_lower = st.session_state.settings_provider.lower()
    key_missing = False
    if selected_p_lower != "ollama":
        req_key = keys.get(selected_p_lower, "").strip()
        if not req_key:
            key_missing = True
            st.warning(f"⚠️ {st.session_state.settings_provider} API Key Required to save or test connection.")

    st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("🔌 Test Connection", use_container_width=True, disabled=key_missing):
            st.session_state.api_keys = keys
            llm = get_llm()
            with st.spinner("Testing connection..."):
                if llm.health_check():
                    st.session_state.connection_status = "success"
                    st.session_state.connection_tested_provider = st.session_state.settings_provider
                    st.success(f"✓ Connection Successful! Provider '{st.session_state.settings_provider}' is responding.")
                else:
                    st.session_state.connection_status = "failed"
                    st.session_state.connection_tested_provider = st.session_state.settings_provider
                    st.error(f"✗ Connection Failed! Verify credentials, local status, or model availability.")
                    
    with col_btn2:
        save_disabled = (
            st.session_state.connection_status != "success" 
            or st.session_state.connection_tested_provider != st.session_state.settings_provider
        )
        if st.button("💾 Save Configuration", use_container_width=True, disabled=save_disabled):
            st.success("✓ Settings Saved successfully!")
            st.session_state.api_keys = keys
            st.rerun()

else:
    # ── Check for document processing error ──
    if "process_error" in st.session_state and st.session_state.process_error:
        st.markdown(f"<h1>🧠 {nav}</h1>", unsafe_allow_html=True)
        err = st.session_state.process_error
        
        from providers.base_provider import (
            PlatformError,
            ProviderConnectionError,
            ProviderConfigurationError,
            ProviderModelError,
            RetrievalError,
            ValidationError
        )
        
        err_cls = RetrievalError
        if err["type"] == "ProviderConnectionError":
            err_cls = ProviderConnectionError
        elif err["type"] == "ProviderConfigurationError":
            err_cls = ProviderConfigurationError
        elif err["type"] == "ProviderModelError":
            err_cls = ProviderModelError
        elif err["type"] == "ValidationError":
            err_cls = ValidationError
            
        e_obj = err_cls(err["message"], technical_details=err["technical_details"])
        handle_platform_error(e_obj)
        
        if st.button("🗑️ Dismiss Error & Clear", key="dismiss_process_error"):
            del st.session_state.process_error
            st.rerun()
        st.stop()

    # ── Verify PDF upload first ──
    if not st.session_state.pdf_processed:
        st.markdown(f"<h1>🧠 {nav}</h1>", unsafe_allow_html=True)
        st.info("Upload a PDF document in the sidebar to activate this mode.")
        st.stop()

    # ── Verify API Key exists for non-Ollama providers ──
    active_p = st.session_state.settings_provider.lower()
    if active_p != "ollama" and not st.session_state.api_keys.get(active_p, "").strip():
        st.markdown(f"<h1>🧠 {nav}</h1>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="background-color: #ffffff; border: 1px solid #000000; border-left: 4px solid #000000; border-radius: 12px; padding: 16px; margin-bottom: 20px;">
            <h4 style="color: #000000; margin: 0 0 8px 0; display: flex; align-items: center; gap: 8px;">
                ⚠️ {st.session_state.settings_provider} API Key Required
            </h4>
            <p style="color: #000000; font-size: 14px; margin: 0 0 12px 0; line-height: 1.5;">
                The platform is currently set to use {st.session_state.settings_provider}, but the corresponding API credential key is missing.
            </p>
            <div style="background-color: #ffffff; border: 1px solid #000000; border-radius: 6px; padding: 10px; font-size: 13px; color: #000000;">
                <strong>Suggested Fix:</strong> Switch to <strong>Settings Panel</strong> and input your API key under the Credentials section.
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.stop()

    if nav == "💬 Chat Assistant":
        # Options to toggle Digital Twin Mode
        col_t1, col_t2 = st.columns([3, 1])
        with col_t1:
            st.markdown("<h1>💬 Conversation Assistant</h1>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: var(--text-secondary); margin-top:-10px; font-size: 13px;'>Active: {st.session_state.settings_provider} · {st.session_state.settings_model}</p>", unsafe_allow_html=True)
        with col_t2:
            st.session_state.twin_mode = st.toggle("🤖 Digital Twin Persona", value=st.session_state.twin_mode)
        
        # Standard chat rendering
        if st.session_state.twin_mode:
            # Custom Twin persona handler
            st.info("Digital Twin Persona mode enabled! Conversing directly with the document subject in the first person.")
            
            # Simple Twin chat loop
            for msg in st.session_state.messages:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])
            
            twin_input = st.chat_input("Speak to the Digital Twin...")
            if twin_input:
                st.session_state.messages.append({"role": "user", "content": twin_input})
                with st.chat_message("user"):
                    st.markdown(twin_input)
                
                with st.chat_message("assistant"):
                    try:
                        with st.spinner("Simulating twin response..."):
                            llm = get_llm()
                            twin_resp = generate_twin_response(twin_input, st.session_state.doc_profile, st.session_state.resume_data, llm)
                            st.markdown(twin_resp)
                            st.session_state.messages.append({"role": "assistant", "content": twin_resp})
                            st.rerun()
                    except PlatformError as e:
                        handle_platform_error(e)
        else:
            render_chat()

    elif nav == "🎓 AI Interviewer":
        st.markdown("<h1>🎓 AI Interviewer Mode</h1>", unsafe_allow_html=True)
        st.markdown("Converse with an AI interviewer based on your resume credentials.")
        st.markdown("---")
        
        llm = get_llm()
        
        # Step 1: Generate Questions
        if not st.session_state.interview_questions:
            with st.spinner("Reviewing credentials to draft tailored questions..."):
                try:
                    st.session_state.interview_questions = generate_interview_questions(
                        st.session_state.resume_data or st.session_state.doc_profile, llm
                    )
                    st.rerun()
                except PlatformError as e:
                    handle_platform_error(e)
                    st.stop()

        questions = st.session_state.interview_questions
        q_idx = st.session_state.active_question_index
        q_keys = list(questions.keys())
        
        # Active Interviewer Avatar Card
        st.markdown("""
        <div class="interview-avatar-card">
            <div class="interview-avatar">🤖</div>
            <div class="interview-avatar-text">
                <h4>DocIntel AI Recruiter</h4>
                <p>Conducting technical assessment based on your credentials</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if q_idx < len(q_keys):
            active_key = q_keys[q_idx]
            active_q = questions[active_key]
            
            # Progress bar
            progress_val = float(q_idx) / len(q_keys)
            st.markdown(f"**Assessment Progress:** Question {q_idx + 1} of {len(q_keys)}")
            st.progress(progress_val)
            
            st.markdown(f"<p style='font-size: 14px; text-transform: uppercase; color: var(--text-primary); font-weight: 700; margin-bottom: 5px;'>Focus Area: {active_key.replace('_', ' ').title()}</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size: 18px; color: var(--text-primary); font-weight: 600; line-height: 1.5;'>{active_q}</p>", unsafe_allow_html=True)
            
            ans = st.text_area("Your response:", height=150, placeholder="Type your answer here...")
            if st.button("Submit Answer", use_container_width=True):
                with st.spinner("Grading answer details..."):
                    try:
                        eval_res = evaluate_interview_answer(active_q, ans, llm)
                        st.session_state.interview_history.append({
                            "question": active_q,
                            "answer": ans,
                            "eval": eval_res
                        })
                        st.session_state.active_question_index += 1
                        st.rerun()
                    except PlatformError as e:
                        handle_platform_error(e)
        else:
            st.success("🎉 Interview Simulation Complete!")
            
            # Render evaluation summaries
            total_scores = {"technical_depth": 0, "communication": 0, "problem_solving": 0, "confidence": 0, "clarity": 0}
            count = len(st.session_state.interview_history)
            
            for h in st.session_state.interview_history:
                scores = h["eval"]["scores"]
                for k in total_scores:
                    total_scores[k] += scores.get(k, 50)
            
            avg_scores = {k: int(v / count) for k, v in total_scores.items()}
            
            col1, col2 = st.columns([1, 2])
            with col1:
                overall_avg = int(sum(avg_scores.values()) / len(avg_scores))
                st.markdown(f"""
                <div style="background: #ffffff; border: 1px solid #000000; padding: 24px; border-radius: 16px; text-align: center; color: #000000;">
                    <span style="font-size: 13px; text-transform: uppercase; font-weight: 600; letter-spacing: 0.5px;">Overall Score</span>
                    <h1 style="color: #000000 !important; font-size: 48px !important; margin: 10px 0 !important; font-family: 'Outfit'; font-weight: 800;">{overall_avg} <span style="font-size: 20px; color: #000000;">/ 100</span></h1>
                    <span style="font-size: 12px; background: #ffffff; border: 1px solid #000000; padding: 4px 8px; border-radius: 20px; color: #000000;">Assessment Complete</span>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown("<h4 style='margin-top:0;'>Category Scores</h4>", unsafe_allow_html=True)
                chips_html = '<div class="score-chip-grid">'
                for k, val in avg_scores.items():
                    label = k.replace('_', ' ').title()
                    chips_html += f"""
                    <div class="score-chip">
                        <span>{label}</span>
                        <strong>{val}/100</strong>
                    </div>
                    """
                chips_html += '</div>'
                st.markdown(chips_html, unsafe_allow_html=True)
            
            st.markdown("---")
            st.markdown("#### Detailed Diagnostic History:")
            for i, h in enumerate(st.session_state.interview_history):
                with st.expander(f"Question {i+1}: {h['question'][:60]}..."):
                    st.markdown(f"**Question:** {h['question']}")
                    st.markdown(f"**Your Answer:** {h['answer']}")
                    st.markdown(f"**Evaluation Feedback:** {h['eval']['feedback']}")
                    st.markdown("**Suggestions for Improvement:**")
                    for s in h['eval']['suggestions']:
                        st.markdown(f"- {s}")
                        
            if st.button("Reset Interviewer", use_container_width=True):
                st.session_state.interview_questions = None
                st.session_state.active_question_index = 0
                st.session_state.interview_history = []
                st.rerun()

    elif nav == "🎨 Content Studio":
        st.markdown("<h1>🎨 Document Content Studio</h1>", unsafe_allow_html=True)
        st.markdown("Convert your document files directly into professional social media copy or creative pieces.")
        st.markdown("---")
        
        content_options = [
            "LinkedIn Post",
            "Twitter Thread",
            "Blog Article",
            "Self Introduction",
            "Elevator Pitch",
            "Cover Letter",
            "Motivation Letter",
            "Speeches & Presentations",
            "Creative Story",
            "Creative Poem",
            "Creative Rap Song"
        ]
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown("### Choose Output Format")
            c_choice = st.selectbox("Format", content_options, label_visibility="collapsed")
            st.markdown("<div style='margin-bottom: 15px;'></div>", unsafe_allow_html=True)
            generate_clicked = st.button("✨ Generate Content", use_container_width=True)
            
            if generate_clicked:
                llm = get_llm()
                with st.spinner("Drafting copy..."):
                    try:
                        source_details = st.session_state.resume_data or st.session_state.doc_profile
                        draft = generate_studio_content(c_choice, source_details, llm)
                        st.session_state.studio_draft = draft
                        st.rerun()
                    except PlatformError as e:
                        handle_platform_error(e)
                        
        with col2:
            st.markdown("### Workspace Output")
            if "studio_draft" in st.session_state and st.session_state.studio_draft:
                st.text_area("Draft content", value=st.session_state.studio_draft, height=350, key="studio_draft_text", label_visibility="collapsed")
                
                btn_col1, btn_col2 = st.columns(2)
                with btn_col1:
                    st.download_button(
                        label="📥 Export as TXT",
                        data=st.session_state.studio_draft,
                        file_name=f"{c_choice.lower().replace(' ', '_')}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                with btn_col2:
                    escaped_draft = st.session_state.studio_draft.replace("`", "\\`").replace("'", "\\'").replace("\n", "\\n").replace("\r", "")
                    theme = st.session_state.get("theme", "light")
                    if theme == "dark":
                        btn_bg = "#1e293b"
                        btn_color = "#ffffff"
                        btn_border = "1px solid #475569"
                    else:
                        btn_bg = "#ffffff"
                        btn_color = "#111827"
                        btn_border = "1px solid #111827"
                    copy_js_html = f"""
                    <div style="text-align: center;">
                        <button onclick="navigator.clipboard.writeText('{escaped_draft}'); alert('Copied to clipboard!');" 
                                style="background: {btn_bg}; color: {btn_color}; border: {btn_border}; border-radius: 8px; padding: 10px 20px; font-weight: 600; cursor: pointer; width: 100%; transition: all 0.2s ease; height: 38px;">
                            📋 Copy to Clipboard
                        </button>
                    </div>
                    """
                    st.components.v1.html(copy_js_html, height=45)
            else:
                st.info("Select a format on the left and click Generate to see the output here.")

    elif nav == "📊 Knowledge Graph":
        render_knowledge_graph(st.session_state.doc_profile, st.session_state.resume_data)

    elif nav == "📈 Career Intelligence":
        st.markdown("<h1>📈 Career Intelligence & Planning</h1>", unsafe_allow_html=True)
        st.markdown("Identify your job compatibility, MLOps learning path, and skill gaps.")
        st.markdown("---")
        
        llm = get_llm()
        
        # Generate Insights
        if "career_insights" not in st.session_state or st.session_state.career_insights is None:
            with st.spinner("Evaluating profile readiness..."):
                try:
                    st.session_state.career_insights = generate_career_insights(
                        st.session_state.resume_data or st.session_state.doc_profile, llm
                    )
                    st.rerun()
                except PlatformError as e:
                    handle_platform_error(e)
                    st.stop()
                
        ci = st.session_state.career_insights
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown(f"""
            <div style="background: #ffffff; border: 1px solid #000000; border-radius: 16px; padding: 20px; margin-bottom: 20px;">
                <h4 style="margin: 0 0 10px 0; color: #000000; font-size: 14px; text-transform: uppercase; letter-spacing: 0.5px;">Market Readiness Score</h4>
                <div style="display: flex; align-items: center; gap: 15px;">
                    <span style="color:#000000; font-size:48px; font-weight:800; font-family:'Outfit';">{ci.get('market_readiness_score', 70)}%</span>
                    <div style="flex-grow: 1; background: #ffffff; border: 1px solid #000000; height: 10px; border-radius: 5px; overflow: hidden;">
                        <div style="background: #000000; width: {ci.get('market_readiness_score', 70)}%; height: 100%;"></div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("#### Job Role Compatibility")
            for j in ci.get("job_matches", []):
                role = j['role']
                score = j['score']
                st.markdown(f"""
                <div style="background: #ffffff; border: 1px solid #000000; border-radius: 10px; padding: 12px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center;">
                    <strong style="color: #000000;">{role}</strong>
                    <span style="background: #ffffff; color: #000000; border: 1px solid #000000; font-size: 12px; padding: 4px 8px; border-radius: 12px; font-weight: 600;">{score}% Match</span>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("### 🛠️ Identified Skill Gaps")
            gaps_html = "<div style='display:flex; flex-wrap:wrap; gap:8px; margin-bottom: 20px;'>"
            for gap in ci.get("skill_gaps", ["Docker", "AWS", "MLOps"]):
                gaps_html += f'<span style="background:#ffffff; color:#000000; border:1px solid #000000; padding:6px 12px; border-radius:20px; font-size:13px; font-weight:500;">{gap}</span>'
            gaps_html += "</div>"
            st.markdown(gaps_html, unsafe_allow_html=True)
            
            st.markdown("### 🗓️ 3-Month Action Plan & Roadmap")
            for i, month in enumerate(ci.get("learning_roadmap", [])):
                st.markdown(f"""
                <div style="background: #ffffff; border: 1px solid #000000; border-radius: 12px; padding: 16px; margin-bottom: 12px; border-left: 4px solid #000000;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                        <span style="font-weight: 700; color: #000000; font-size: 14px;">{month['duration']}</span>
                        <span style="background: #ffffff; color: #000000; border: 1px solid #000000; font-size: 11px; padding: 2px 6px; border-radius: 4px; font-weight: 600;">Phase {i+1}</span>
                    </div>
                    <strong style="font-size: 15px; color: #000000; display: block; margin-bottom: 6px;">{month['topic']}</strong>
                    <p style="font-size: 13px; color: #000000; margin: 0; line-height: 1.5;">{month['details']}</p>
                </div>
                """, unsafe_allow_html=True)
                
        st.markdown("---")
        col_s, col_w = st.columns(2)
        with col_s:
            st.markdown("#### 🟢 Core Strengths")
            for s in ci.get("strengths", []):
                st.markdown(f"""
                <div style="background: #ffffff; border: 1px solid #000000; border-radius: 8px; padding: 10px; margin-bottom: 8px; display: flex; align-items: center; gap: 8px; color: #000000; font-size: 14px;">
                    <span>✔</span> <strong>{s}</strong>
                </div>
                """, unsafe_allow_html=True)
        with col_w:
            st.markdown("#### 🟡 Areas of Improvement")
            for w in ci.get("weaknesses", []):
                st.markdown(f"""
                <div style="background: #ffffff; border: 1px solid #000000; border-radius: 8px; padding: 10px; margin-bottom: 8px; display: flex; align-items: center; gap: 8px; color: #000000; font-size: 14px;">
                    <span>💡</span> <strong>{w}</strong>
                </div>
                """, unsafe_allow_html=True)
                
        if st.button("Re-evaluate Career Profile", use_container_width=True):
            st.session_state.career_insights = None
            st.rerun()
