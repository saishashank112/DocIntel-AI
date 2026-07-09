# DocIntel AI Platform: Complete Project Documentation

Welcome to the official developer documentation for the **DocIntel AI Platform**. This document serves as the single source of truth for the codebase architecture, multi-provider AI backends, specialized cognitive engines, settings systems, and onboarding procedures.

---

## Section 1: Project Overview

The **DocIntel AI Platform** is an enterprise-ready, local-first document intelligence workspace. Rather than acting as a standard RAG search box, it transforms uploaded documents into active cognitive assets for career matching, interactive mock interview prep, content creation, digital twin simulation, and knowledge mapping.

### Key Value Pillars
- **Multi-LLM Integration:** Seamless switching between local Ollama instances (for offline privacy) and commercial backends (OpenAI, Anthropic, Gemini, Grok, and OpenRouter).
- **Interactive Interview Mode:** Contextual mock recruiter that evaluates user answers against structured depth, clarity, and communication rubrics with progress tracking.
- **Digital Twin Persona:** Simulates first-person chats with the author or subject of the document.
- **Content Studio:** Dynamic multi-format generator creating LinkedIn posts, Twitter threads, presentations, blog articles, cover letters, and creative writing.
- **Knowledge Graph Visualizer:** Zoomable, draggable relationship mapping showing links between entities, companies, and skills.
- **Career Intelligence:** Job match percentage calculator, MLOps learning roadmap builder, and skill gaps diagnostic tool.

---

## Section 2: High-Level Architecture

The platform uses a modular, decoupled structure to process metadata, routing, and user flows:

```
                  [ Upload PDF Document ]
                             │
                             ▼
                  [ Document Parsing ] (pdfplumber)
                             │
            ┌────────────────┴────────────────┐
            ▼                                 ▼
   [ Text Splitter ]                 [ Document Profiler ]
  (Overlap Chunks 1000)             (Summary & Resume Parser)
            │                                 │
            ├─────────────────┐               │
            ▼                 ▼               ▼
     [ Vector Store ]     [ Keywords ]    [ Session State ]
       (ChromaDB)           (BM25)        (Profile Metadata)
            │                 │               │
            └────────┬────────┘               │
                     ▼                        │
               [ User Input ]                 │
                     │                        │
                     ▼                        ▼
             [ Intent Classifier ] ──► [ Workflow Selection ]
                     │                 (Interviewer, Twin, Studio)
                     │                        │
                     ▼                        ▼
             [ Retrieval Flow ]        [ Prompt Registry ]
             (Hybrid + Reranker)              │
                     │                        ▼
                     └───────────────┬────────┘
                                     ▼
                             [ Model Provider ]
                             (Ollama, OpenAI, Anthropic)
                                     │
                                     ▼
                             [ Grounding Check ]
                                     │
                                     ▼
                               [ UI Visuals ]
```

---

## Section 3: Folder Structure

The directory structure separates orchestration from individual domains:

```
project/
├── app.py                      # UI router, page config, and view orchestration
├── PROJECT_DOCUMENTATION.md    # Developer onboarding wiki
├── requirements.txt            # Package dependencies
├── .env                        # Environment configurations
├── .streamlit/
│   └── config.toml             # Streamlit base theme configuration (forces light mode base)
├── config/
│   └── settings.py             # Settings configurations and metadata
├── prompts/
│   ├── prompt_registry.py      # Prompt mapping index
│   ├── doc_overview.txt        # PDF metadata analyzer prompt
│   ├── resume_extract.txt      # Resume key-value parser prompt
│   ├── intent.txt              # Intent classifier prompt
│   ├── expand.txt              # Synonym expansion prompt
│   ├── summary_intent.txt      # Profile summarization prompt
│   ├── resume_intent.txt       # Candidate detail analysis prompt
│   ├── rag_answer.txt          # Dynamic length RAG synthesis prompt
│   ├── grounding.txt           # Fact check evaluation prompt
│   └── followups.txt           # Followup builder prompt
├── providers/
│   ├── base_provider.py        # Abstract BaseProvider with invoke wrappers
│   ├── ollama_provider.py      # Local Ollama endpoint connector
│   ├── openai_provider.py      # OpenAI API connector
│   ├── anthropic_provider.py   # Anthropic API connector
│   ├── gemini_provider.py      # Google Gemini API connector
│   ├── grok_provider.py        # Grok/xAI API connector
│   └── openrouter_provider.py  # OpenRouter API completions connector
├── services/
│   ├── llm_service.py          # Dynamic LLM provider factory
│   ├── embedding_service.py    # Dynamic embedding model factory
│   ├── reranker_service.py     # Caches local CrossEncoder rerankers
│   ├── document_service.py     # Extraction, chunking, and index building
│   ├── interview_engine.py     # Generates mock questions & evaluates answers
│   ├── persona_engine.py       # Manages Digital Twin chat templates
│   ├── content_studio.py       # Handles studio copy-drafting
│   ├── knowledge_graph.py      # Maps and renders node relations in Streamlit
│   └── career_engine.py        # Matched scores, gaps, and roadmap timelines
├── routing/
│   ├── intent_classifier.py    # Classifies user query intents
│   └── response_router.py      # Selects RAG prompt templates
├── rag/
│   ├── retrieval.py            # Hybrid vector + BM25 retrieval pipeline
│   └── grounding.py            # Fact check verdicts
├── ui/
│   ├── styling.py              # Injects theme-aware CSS; covers ALL Streamlit components
│   ├── sidebar.py              # Sidebar navigation controls and file uploaders
│   └── chat.py                 # Renders the app chat interface
└── utils/
    └── prompt_loader.py        # Prompt template file loader
```

---

## Section 4: Technology Stack

- **UI Orchestrator: Streamlit** — Responsive web client canvas wrapper.
- **RAG Embedding Layer: ChromaDB + sentence-transformers** — Vector store and local Cross-Encoder reranking.
- **Keyword Retrieval: rank-bm25** — Matches literal search queries.
- **Parser Engine: pdfplumber** — Extracted pages with coordinate tolerances to retain table layouts.

---

## Section 5: Resume Intelligence System

The system parses resumes to extract candidate details:
1. **Detection:** Checks document profile metadata. If the profile's `document_type` is classified as `resume`, the system triggers extraction.
2. **Extraction:** Parses the resume to extract skills, project names, duration, and work highlights, storing them in the session state.
3. **Sidebar Details:** Displays candidate details (Headline, Name, Top Skills, and Projects) in the sidebar.
4. **Context Enrichment:** Blends the structured resume details into the retrieved context for queries related to skills, projects, or creative writing (e.g. writing cover letters).

---

## Section 6: Creative Generation System (Content Studio)

The **Content Studio** uses document details as source material for creative generation tasks (e.g., poems, stories, or LinkedIn posts):
- **LinkedIn Posts:** Drafts copy highlighting achievements, projects, and skills.
- **Self Introductions / elevator pitches:** Creates elevator pitches based on candidate experience.
- **Poems / Rap Songs:** Drafts creative rhymes based on candidate details.

---

## Section 7: Retrieval Flow

The retrieval pipeline processes queries in a step-by-step flow:
1. **Query Expansion:** The original query is expanded with synonyms.
2. **Hybrid Search:** Retrieves the top 15 results from vector search and the top 15 results from BM25.
3. **Deduplication:** Merges overlapping chunks into a single list.
4. **Reranking:** The Cross-Encoder model scores and ranks results, selecting the top 5 chunks.
5. **Context Building:** Selected chunks are formatted into a context block with page markers.
6. **LLM Generation:** The LLM generates a response based on the context.
7. **Grounding Evaluation:** Evaluates the generated response for factual consistency.

---

## Section 8: Grounding and Verification

The **Factual Grounding Engine** prevents hallucinations using an LLM-as-a-judge check:
- **`Fully Grounded`**: The answer is supported by the context.
- **`Partially Grounded`**: Supported with minor inferences.
- **`Reasoned Inference`**: Supported through logical deduction.
- **`Not Grounded`**: The answer is unsupported by the context.

Users can view validation verdicts in chat badges and expand the **Sources & Evidence** drop-down to view the referenced source text.

---

## Section 9: UI Theming & Accessibility System

### Architecture Overview

The theming system is managed entirely in `ui/styling.py` via `apply_custom_css()`. All visual styles are driven by CSS custom properties (variables) injected into the `<style>` block via `st.markdown(..., unsafe_allow_html=True)`.

### Theme Variable Sets

Two variable sets are defined — light (default) and dark:

| Variable | Light Value | Dark Value |
|---|---|---|
| `--bg-app` | `#ffffff` | `#0f172a` |
| `--text-primary` | `#111827` | `#ffffff` |
| `--text-secondary` | `#374151` | `#cbd5e1` |
| `--text-muted` | `#6b7280` | `#94a3b8` |
| `--border-color` | `#e5e7eb` | `#334155` |
| `--card-bg` | `#f9fafb` | `#1e293b` |
| `--input-bg` | `#ffffff` | `#1e293b` |
| `--button-bg` | `#ffffff` | `#1e293b` |

### Theme Switch Mechanism

1. The `render_sidebar()` function renders a "🌙 Dark Theme Mode" toggle.
2. `st.session_state.theme` is set to `"dark"` or `"light"` accordingly.
3. After the sidebar renders, `apply_custom_css()` is called in `app.py` — **critically, after `render_sidebar()`** — so the theme session state is already committed before CSS variables are generated.

### Streamlit Base Theme

A `.streamlit/config.toml` file forces Streamlit's native component theme to `light` base, which ensures native components (file uploaders, number inputs, expanders, tabs, etc.) inherit the correct base styling before custom CSS overrides are applied on top.

### Components Covered by Custom CSS

Every Streamlit native component is explicitly styled:

| Component | Selector |
|---|---|
| App background | `.stApp`, `[data-testid="stAppViewContainer"]` |
| Sidebar | `[data-testid="stSidebar"]` |
| Chat messages | `[data-testid="stChatMessage"]` |
| Chat input bar | `[data-testid="stBottom"]`, `[data-testid="stChatInput"]` |
| AI Status pipeline | `[data-testid="stStatus"]` |
| Spinner | `[data-testid="stSpinner"]` |
| File uploader | `[data-testid="stFileUploader"]`, `[data-testid="stFileUploaderDropzone"]` |
| Text / number inputs | `[data-testid="stTextInput"]`, `[data-testid="stNumberInput"]` |
| Text area | `[data-testid="stTextArea"]` |
| Selectbox / listbox | `div[data-baseweb="select"]`, `div[role="listbox"]` |
| Expanders | `[data-testid="stExpander"]`, `[data-testid="stExpanderDetails"]` |
| Alerts / info boxes | `[data-testid="stAlert"]` |
| Progress bar | `[data-testid="stProgress"]` |
| Tabs | `div[data-baseweb="tab-list"]`, `button[data-baseweb="tab"]` |
| Buttons | `button`, `[data-testid="stBaseButton-*"]` |
| Toggle / checkbox / slider | `[data-testid="stToggle"]`, `[data-testid="stSlider"]` |

### Custom Semantic Components

The following custom HTML/CSS class components are defined in `styling.py` and used across `chat.py`, `app.py`, and `services/`:

- `.intent-badge` — Intent classification label above AI responses
- `.source-card` — Source evidence snippets inside expanders
- `.ground-badge` — Factual grounding verdict pill
- `.error-card`, `.error-card-*` — Error display cards
- `.topic-pill` — Key topic tags in sidebar
- `.interview-avatar-card` — AI recruiter intro card
- `.score-chip`, `.score-chip-grid` — Interview score display grid
- `.global-header` — Fixed top navigation bar
- `.graph-container` — Knowledge graph canvas wrapper

---

## Section 10: Developer Onboarding

Follow these steps to set up the project locally:

### 1. Clone the Project
```powershell
git clone <repository_url>
cd "Chat With Your PDF"
```

### 2. Configure Virtual Environment
```powershell
python -m venv venv
.\venv\Scripts\activate
```

### 3. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 4. Configure Models (via Ollama)
Ensure Ollama is running, then pull the required models:
```powershell
ollama pull llama3.2
ollama pull nomic-embed-text
```

### 5. Start Application
```powershell
streamlit run app.py
```
Open **[http://localhost:8501](http://localhost:8501)** in your browser to test the application.

---

## Section 11: Error Handling System

The platform uses a structured error hierarchy defined in `providers/base_provider.py`:

| Error Class | Trigger Condition |
|---|---|
| `ProviderConnectionError` | Ollama not running / network failure |
| `ProviderConfigurationError` | Missing or invalid API key |
| `ProviderModelError` | Selected model not available |
| `RetrievalError` | Document chunking / index failure |
| `ValidationError` | Generic validation failures |

Each error is caught and rendered as a dedicated **Error Card** component (`render_error_card()` in `ui/chat.py`) displaying:
- Error type icon and title
- Plain-language description  
- Step-by-step suggested fix
- Collapsible technical details (full stack trace)

---

## Section 12: Known Issues & Troubleshooting

### Ollama Connection Timeout
**Symptom:** `ProviderConnectionError: Request to Ollama timed out`

**Cause:** The local Ollama server is not running, or the model is not pulled.

**Fix:**
1. Run `ollama serve` in a terminal window
2. Verify the model: `ollama list`
3. Pull the model if missing: `ollama pull llama3.2`
4. Ensure port `11434` is accessible

### JSON Parsing Errors (KeyError on document_type)
**Symptom:** `KeyError: '\n  "document_type"'` during PDF processing

**Cause:** The LLM returned a malformed JSON profile (extra whitespace or truncation).

**Fix:** Implemented in `services/document_service.py` — JSON is cleaned and stripped of markdown code fences before `json.loads()` is called. If the error persists, try a different model or adjust the chunk size in Settings → Advanced Settings.

### Dark Background on Chat Toolbar
**Symptom:** The bottom chat input area shows a dark background even in light mode.

**Fix:** Resolved. `[data-testid="stBottom"]` and all child selectors are explicitly targeted with `var(--bg-app)` in `ui/styling.py`. A `.streamlit/config.toml` base theme of `light` also prevents native Streamlit components from defaulting to dark.
