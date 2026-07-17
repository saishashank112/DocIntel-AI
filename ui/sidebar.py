import streamlit as st
import json
from services.llm_service import get_llm
from services.document_service import process_pdf
from providers.base_provider import PlatformError

def render_sidebar():
    """Render sidebar navigation controls and document metadata details."""
    with st.sidebar:
        st.markdown("<h2 style='font-size: 20px; font-weight: 700; margin-bottom: 2px;'>🧠 DocIntel</h2>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 11px; margin-top: 0; margin-bottom: 15px; color: #000000;'>Premium Document Intelligence</p>", unsafe_allow_html=True)
        
        # Navigation Selector
        if "navigation" not in st.session_state:
            st.session_state.navigation = "💬 Chat Assistant"
            
        nav_options = [
            "💬 Chat Assistant",
            "🎓 AI Interviewer",
            "🎨 Content Studio",
            "📊 Knowledge Graph",
            "📈 Career Intelligence",
            "⚙️ Settings Panel"
        ]
        
        st.markdown("**Navigation**")
        st.session_state.navigation = st.radio(
            "Navigation Options",
            nav_options,
            index=nav_options.index(st.session_state.navigation),
            label_visibility="collapsed"
        )
        st.markdown("<hr style='margin: 10px 0;'>", unsafe_allow_html=True)

        if st.session_state.navigation != "⚙️ Settings Panel":
            uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"], label_visibility="collapsed")

            if uploaded_file and not st.session_state.pdf_processed:
                st.markdown(f"📄 **{uploaded_file.name}**")
                if st.button("⚡ Process & Analyze", use_container_width=True):
                    llm = get_llm()
                    with st.spinner("Extracting and chunking..."):
                        try:
                            chroma_db, bm25, chunks, total_pages, doc_profile, resume_data = process_pdf(uploaded_file, llm)
                            st.session_state.chroma_db     = chroma_db
                            st.session_state.bm25          = bm25
                            st.session_state.all_chunks    = chunks
                            st.session_state.total_pages   = total_pages
                            st.session_state.doc_profile   = doc_profile
                            st.session_state.resume_data   = resume_data
                            st.session_state.pdf_filename  = uploaded_file.name
                            st.session_state.pdf_processed = True
                            if "process_error" in st.session_state:
                                del st.session_state.process_error
                            st.rerun()
                        except PlatformError as e:
                            st.session_state.process_error = {
                                "type": type(e).__name__,
                                "message": str(e),
                                "technical_details": e.technical_details
                            }
                            st.rerun()
                        except Exception as e:
                            st.session_state.process_error = {
                                "type": "RetrievalError",
                                "message": "An unexpected error occurred during document processing.",
                                "technical_details": str(e)
                            }
                            st.rerun()

            if st.session_state.pdf_processed and st.session_state.doc_profile:
                profile = st.session_state.doc_profile
                doc_type = profile.get("document_type", "other").replace("_", " ").title()
                
                st.markdown(f"<h3 style='font-size: 15px; margin-bottom: 2px;'>📄 {profile.get('title', 'Document')}</h3>", unsafe_allow_html=True)
                st.markdown(f"<span style='font-size: 11px; color: #000000; font-weight: 600;'>{doc_type}</span> <span style='font-size: 11px;'>· {st.session_state.total_pages} pages</span>", unsafe_allow_html=True)
                st.markdown("<div style='margin-bottom: 10px;'></div>", unsafe_allow_html=True)

                with st.expander("📋 Document Overview", expanded=True):
                    st.markdown(f"<p style='font-size: 12px; line-height: 1.5; margin: 0;'>{profile.get('executive_summary', '')}</p>", unsafe_allow_html=True)

                with st.expander("🏷️ Key Topics", expanded=False):
                    topics = profile.get("key_topics", [])
                    if topics:
                        pills_html = "".join([f'<span class="topic-pill">{t}</span>' for t in topics])
                        st.markdown(pills_html, unsafe_allow_html=True)
                    else:
                        st.caption("No key topics identified.")

                with st.expander("🔍 Entities & Details", expanded=False):
                    entities = profile.get("main_entities", [])
                    if entities:
                        st.markdown("<p style='font-size: 11px; font-weight: 600; margin-bottom: 2px; color: #000000;'>Core Entities:</p>", unsafe_allow_html=True)
                        st.markdown(f"<p style='font-size: 12px; margin: 0;'>{', '.join(entities[:12])}</p>", unsafe_allow_html=True)
                    else:
                        st.caption("No entities identified.")

                if st.session_state.resume_data:
                    rd = st.session_state.resume_data
                    with st.expander("👤 Candidate Details", expanded=False):
                        st.markdown(f"**Name:** {rd.get('name', 'Unknown')}")
                        if rd.get("headline"):
                            st.markdown(f"*{rd['headline']}*")
                        
                        skills = rd.get("skills", [])
                        if skills:
                            st.markdown("<p style='font-size: 11px; font-weight: 600; margin-bottom: 2px; color: #000000; margin-top: 6px;'>Top Skills:</p>", unsafe_allow_html=True)
                            st.markdown(f"<p style='font-size: 12px; margin: 0;'>{', '.join(skills[:12])}</p>", unsafe_allow_html=True)

                with st.expander("⚙️ Metadata & Actions", expanded=False):
                    fn = st.session_state.get("pdf_filename", "Unknown File")
                    st.markdown(f"<p style='font-size: 11px; margin: 0 0 10px 0;'><strong>File Name:</strong> {fn}<br><strong>Total Pages:</strong> {st.session_state.total_pages}</p>", unsafe_allow_html=True)
                    if st.button("🗑️ Clear & Start Over", use_container_width=True):
                        for key in ["messages", "pdf_processed", "pdf_filename", "followups", "doc_profile",
                                    "resume_data", "chroma_db", "bm25", "all_chunks",
                                    "total_pages", "conversation_history", "process_error"]:
                            st.session_state[key] = [] if key in ("messages", "followups", "conversation_history") else None if key not in ("pdf_processed",) else False
                            if key == "pdf_filename":
                                st.session_state[key] = ""
                        st.rerun()

        st.markdown("---")
        if "theme" not in st.session_state:
            st.session_state.theme = "light"
        theme_toggle = st.toggle("🌙 Dark Theme Mode", value=(st.session_state.theme == "dark"))
        st.session_state.theme = "dark" if theme_toggle else "light"

