import pdfplumber
import re
import json
import streamlit as st
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from rank_bm25 import BM25Okapi

from config.settings import CHUNK_SIZE, CHUNK_OVERLAP
from prompts.prompt_registry import get_prompt
from services.embedding_service import get_embeddings
from providers.base_provider import ProviderConnectionError, RetrievalError

def extract_full_text(pdf_file):
    """Extract clean text from PDF using pdfplumber with fallback."""
    pages_text = []
    with pdfplumber.open(pdf_file) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text(x_tolerance=2, y_tolerance=2)
            if text and len(text.strip()) > 30:
                pages_text.append((i + 1, text.strip()))
    return pages_text, len(pdf.pages)

def safe_json_parse(raw: str, fallback: dict) -> dict:
    """Robustly parse JSON from an LLM response."""
    try:
        raw = raw.strip()
        # Strip markdown code fences
        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw)
        return json.loads(raw)
    except Exception:
        return fallback

def generate_doc_overview(full_text: str, llm) -> dict:
    """Run LLM to generate document overview/profile."""
    sample = full_text[:3000]
    prompt_tpl = get_prompt("doc_overview")
    response = llm.invoke(prompt_tpl.replace("{text}", sample))
    return safe_json_parse(response.content, {
        "document_type": "other",
        "title": "Uploaded Document",
        "executive_summary": "A document was uploaded and processed.",
        "key_topics": [],
        "main_entities": [],
        "themes": []
    })

def extract_resume_structure(full_text: str, llm) -> dict:
    """Extract structured resume fields via LLM."""
    prompt_tpl = get_prompt("resume_extract")
    response = llm.invoke(prompt_tpl.replace("{text}", full_text[:4000]))
    return safe_json_parse(response.content, {
        "name": "Unknown",
        "headline": "",
        "education": [],
        "experience": [],
        "skills": [],
        "projects": [],
        "certifications": [],
        "contact": ""
    })

def process_pdf(pdf_file, llm):
    """Full document processing: extraction, profiling, chunking, indexing."""
    pages_text, total_pages = extract_full_text(pdf_file)
    full_text = "\n\n".join([text for _, text in pages_text])

    # Build LangChain Documents
    docs = [
        Document(page_content=text, metadata={"page_number": page_num})
        for page_num, text in pages_text
    ]

    # Chunk documents
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", "  ", " ", ""]
    )
    chunks = splitter.split_documents(docs)
    for i, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"] = i

    # Embed into ChromaDB
    embeddings = get_embeddings()
    try:
        chroma_db = Chroma.from_documents(chunks, embeddings)
    except Exception as e:
        err_msg = str(e)
        if "connection" in err_msg.lower() or "connect" in err_msg.lower() or "refused" in err_msg.lower() or "ollama" in err_msg.lower():
            raise ProviderConnectionError(
                "Failed to connect to the embedding service endpoint.",
                technical_details=f"Embedding service: {st.session_state.get('settings_embeddings', 'Unknown')}\nDetails: {err_msg}"
            )
        else:
            raise RetrievalError(
                "Failed to index document chunks into vector database.",
                technical_details=err_msg
            )

    # BM25 index
    tokenized = [c.page_content.lower().split() for c in chunks]
    bm25 = BM25Okapi(tokenized)

    # Document Profiling
    doc_profile = generate_doc_overview(full_text, llm)
    resume_data = None
    if doc_profile.get("document_type") == "resume":
        resume_data = extract_resume_structure(full_text, llm)

    return chroma_db, bm25, chunks, total_pages, doc_profile, resume_data
