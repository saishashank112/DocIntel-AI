import streamlit as st
from langchain_ollama import OllamaEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
from config.settings import EMBEDDING_MODEL

@st.cache_resource
def get_embeddings():
    """Retrieve and cache the selected embedding interface model."""
    if "settings_embeddings" not in st.session_state:
        st.session_state.settings_embeddings = "Ollama nomic-embed-text"
        
    choice = st.session_state.settings_embeddings
    if "sentence-transformers" in choice.lower() or "local" in choice.lower():
        # Fallback to local sentence-transformers model
        return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    else:
        return OllamaEmbeddings(model=EMBEDDING_MODEL)
