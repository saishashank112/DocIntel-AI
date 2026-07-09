# DocIntel AI Platform 🧠🤖

An enterprise-ready, local-first document intelligence platform that transforms standard document reading into active cognitive assets. Beyond basic search and retrieval, DocIntel AI offers interactive interviewer modes, digital twin persona chat, content creation studios, knowledge graphs, and career alignment diagnostics.

---

## 🌟 Key Value Pillars

- **Multi-LLM Integration:** Seamless switching between local Ollama instances (for offline privacy) and commercial backends (OpenAI, Anthropic, Gemini, Grok, and OpenRouter).
- **Interactive Interview Mode:** A contextual mock recruiter that evaluates user answers against structured depth, clarity, and communication rubrics with progress tracking.
- **Digital Twin Persona:** Simulates first-person chats with the author or subject of the document.
- **Content Studio:** Dynamic multi-format content generator creating LinkedIn posts, Twitter threads, presentations, blog articles, cover letters, and creative writing.
- **Knowledge Graph Visualizer:** Zoomable, draggable relationship mapping showing links between entities, companies, and skills.
- **Career Intelligence:** Job match percentage calculator, customized MLOps learning roadmap builder, and skill gaps diagnostic tool.

---

## ⚙️ High-Level Architecture

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

## 📁 Repository Structure

The codebase is organized modularly to separate orchestration from core business domains:

```
project/
├── app.py                      # UI router, page config, and view orchestration
├── PROJECT_DOCUMENTATION.md    # Developer onboarding wiki
├── README.md                   # Project overview & startup instructions
├── requirements.txt            # Package dependencies
├── .env                        # Environment configurations
├── .streamlit/
│   └── config.toml             # Streamlit base theme configuration
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
│   └── openrouter_provider.py  # OpenRouter completions connector
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
│   ├── styling.py              # Injects theme-aware CSS for custom UI elements
│   ├── sidebar.py              # Sidebar navigation controls and file uploaders
│   └── chat.py                 # Renders the app chat interface
└── utils/
    └── prompt_loader.py        # Prompt template file loader
```

---

## 🛠️ Tech Stack & Dependencies

- **Frontend / UI**: [Streamlit](https://streamlit.io/) — Responsive dashboard and chat interface.
- **RAG & Embeddings**: [ChromaDB](https://www.trychroma.com/) + `sentence-transformers` for semantic similarity, vector indexing, and local Cross-Encoder reranking.
- **Keyword Retrieval**: `rank-bm25` for token matching and hybrid search.
- **PDF Extraction**: `pdfplumber` to extract structured texts and tables.
- **AI Orchestration**: Built-in support for LangChain structures.

---

## 🚀 Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/saishashank112/DocIntel-AI.git
cd DocIntel-AI
```

### 2. Set Up a Virtual Environment
```bash
python -m venv venv
# On Windows (Command Prompt)
venv\Scripts\activate
# On Windows (PowerShell)
.\venv\Scripts\Activate.ps1
# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configuration
Create a `.env` file in the root directory (or edit the existing one) to specify your preferred default models and provider keys:

```ini
# Default Provider Configuration
DEFAULT_PROVIDER=ollama
DEFAULT_MODEL=llama3.2

# LLM Providers Configuration
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
GEMINI_API_KEY=your_gemini_api_key
GROK_API_KEY=your_grok_api_key
OPENROUTER_API_KEY=your_openrouter_api_key
OLLAMA_BASE_URL=http://localhost:11434
```

### 5. Running the Application
Run the Streamlit application:
```bash
streamlit run app.py
```
Open the provided local server URL (usually `http://localhost:8501`) in your web browser.
