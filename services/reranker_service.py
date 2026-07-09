import streamlit as st
from sentence_transformers import CrossEncoder
from config.settings import RERANKER_MODEL

@st.cache_resource
def get_reranker():
    """Cache and return CrossEncoder instance."""
    return CrossEncoder(RERANKER_MODEL, max_length=512)
