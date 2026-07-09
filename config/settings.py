# Model Constants
CHUNK_SIZE       = 1000
CHUNK_OVERLAP    = 200
EMBEDDING_MODEL  = "nomic-embed-text"
LLM_MODEL        = "llama3.2"
RERANKER_MODEL   = "cross-encoder/ms-marco-MiniLM-L-6-v2"
MAX_HISTORY_TURNS = 3

# Intent Metadata definitions
INTENT_META = {
    "document_summary":      {"label": "📋 Summary",            "color": "#6366f1"},
    "section_summary":       {"label": "📖 Section Summary",    "color": "#8b5cf6"},
    "fact_lookup":           {"label": "🔍 Fact Lookup",       "color": "#64748b"},
    "entity_extraction":     {"label": "🏷️ Entity Extraction",  "color": "#0ea5e9"},
    "project_extraction":    {"label": "🚀 Projects",           "color": "#10b981"},
    "skill_extraction":      {"label": "🛠️ Skills",             "color": "#ec4899"},
    "timeline_extraction":   {"label": "🗓️ Timeline",           "color": "#f59e0b"},
    "comparison":            {"label": "⚖️ Comparison",        "color": "#059669"},
    "analysis":              {"label": "🧠 Analysis",          "color": "#7c3aed"},
    "career_analysis":       {"label": "📈 Career Analysis",   "color": "#eab308"},
    "creative_writing":      {"label": "✍️ Creative Writing",   "color": "#f43f5e"},
    "story_generation":      {"label": "📖 Storytelling",       "color": "#10b981"},
    "poem_generation":       {"label": "🎵 Poetry",             "color": "#a855f7"},
    "song_generation":       {"label": "🎤 Songwriting",        "color": "#3b82f6"},
    "rap_generation":        {"label": "🎧 Rap Generation",     "color": "#14b8a6"},
    "linkedin_post":         {"label": "💼 LinkedIn Post",      "color": "#0077b5"},
    "blog_post":             {"label": "📝 Blog Writing",       "color": "#f97316"},
    "self_introduction":     {"label": "🤝 Introduction",       "color": "#10b981"},
    "cover_letter":          {"label": "✉️ Cover Letter",       "color": "#6366f1"},
    "interview_preparation":  {"label": "💼 Interview Prep",     "color": "#8b5cf6"},
    "custom_content":        {"label": "🎨 Custom Content",     "color": "#ec4899"},
}
