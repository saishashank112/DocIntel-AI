import streamlit as st

def apply_custom_css():
    """Apply centralized styling rules for Light and Dark themes dynamically."""
    theme = st.session_state.get("theme", "light")
    if theme == "dark":
        theme_variables = """
        :root {
            --bg-app: #0f172a;
            --text-primary: #ffffff;
            --text-secondary: #cbd5e1;
            --text-muted: #94a3b8;
            --border-color: #334155;
            --card-bg: #1e293b;
            --input-bg: #1e293b;
            --input-border: #475569;
            --button-bg: #1e293b;
            --button-border: #475569;
            --button-text: #ffffff;
            --button-hover-bg: #ffffff;
            --button-hover-text: #0f172a;
            --badge-bg: #1e293b;
            --badge-border: #334155;
            --badge-text: #cbd5e1;
        }
        """
    else:
        theme_variables = """
        :root {
            --bg-app: #ffffff;
            --text-primary: #111827;
            --text-secondary: #374151;
            --text-muted: #6b7280;
            --border-color: #e5e7eb;
            --card-bg: #f9fafb;
            --input-bg: #ffffff;
            --input-border: #cbd5e1;
            --button-bg: #ffffff;
            --button-border: #111827;
            --button-text: #111827;
            --button-hover-bg: #111827;
            --button-hover-text: #ffffff;
            --badge-bg: #ffffff;
            --badge-border: #e5e7eb;
            --badge-text: #374151;
        }
        """

    st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;600;800&display=swap');

{theme_variables}

/* ── Base typography ── */
html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
    color: var(--text-primary) !important;
}}

/* ── App-level backgrounds ── */
.stApp {{
    background-color: var(--bg-app) !important;
    color: var(--text-primary) !important;
}}

[data-testid="stAppViewContainer"] {{
    background-color: var(--bg-app) !important;
}}

[data-testid="stAppViewBlockContainer"] {{
    max-width: 900px !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
    padding-top: 3rem !important;
    padding-bottom: 6rem !important;
}}

/* ── Hide Streamlit default header bar ── */
[data-testid="stHeader"] {{
    display: none !important;
}}

/* ── Global custom header ── */
.global-header {{
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 56px;
    background-color: var(--bg-app) !important;
    border-bottom: 1px solid var(--border-color) !important;
    z-index: 999;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 24px;
    box-shadow: none;
}}

.header-spacer {{ height: 56px; }}

.header-left {{
    display: flex;
    align-items: center;
    gap: 10px;
}}

.logo-icon {{ font-size: 22px; }}

.brand-name {{
    font-family: 'Outfit', sans-serif;
    font-size: 17px;
    font-weight: 800;
    color: var(--text-primary);
    letter-spacing: -0.02em;
    display: flex;
    align-items: center;
    gap: 6px;
}}

.brand-badge {{
    background-color: var(--text-primary);
    color: var(--bg-app) !important;
    font-size: 9px;
    font-weight: 700;
    padding: 2px 6px;
    border-radius: 4px;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    border: 1px solid var(--border-color);
}}

.header-right {{
    display: flex;
    align-items: center;
    gap: 16px;
}}

.status-indicator {{
    background-color: var(--card-bg) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 20px;
    padding: 4px 12px;
    display: flex;
    align-items: center;
    gap: 8px;
}}

.status-dot {{
    width: 8px;
    height: 8px;
    background-color: #10b981 !important;
    border-radius: 50%;
    display: inline-block;
    box-shadow: 0 0 8px #10b981 !important;
}}

.status-text {{
    font-size: 11px;
    font-weight: 600;
    color: var(--text-primary);
}}

.avatar-profile {{
    width: 28px;
    height: 28px;
    background-color: var(--text-primary);
    color: var(--bg-app);
    font-size: 11px;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
}}

/* ── Sidebar ── */
[data-testid="stSidebar"] {{
    background-color: var(--bg-app) !important;
    border-right: 1px solid var(--border-color) !important;
}}

[data-testid="stSidebar"] * {{
    color: var(--text-secondary) !important;
}}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {{
    color: var(--text-primary) !important;
}}

[data-testid="stSidebar"] [data-testid="stExpander"] {{
    background-color: var(--card-bg) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 12px !important;
    margin-bottom: 10px !important;
}}

[data-testid="stSidebar"] [data-testid="stExpanderDetails"] {{
    background-color: var(--card-bg) !important;
    padding: 12px !important;
}}

/* ── Headings ── */
h1, h2, h3, h4, h5, h6 {{
    font-family: 'Outfit', sans-serif;
    color: var(--text-primary) !important;
}}

h1 {{
    font-size: 32px !important;
    font-weight: 800 !important;
    letter-spacing: -0.03em !important;
    background: none !important;
    -webkit-background-clip: initial !important;
    -webkit-text-fill-color: var(--text-primary) !important;
    color: var(--text-primary) !important;
    margin-bottom: 0.5rem !important;
}}

/* ── Markdown text ── */
.stMarkdown p {{
    font-size: 16px !important;
    line-height: 1.8 !important;
    color: var(--text-secondary) !important;
    margin-bottom: 16px !important;
}}

.stMarkdown strong {{
    color: var(--text-primary) !important;
    font-weight: 600;
}}

.stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {{
    color: var(--text-primary) !important;
}}

.stMarkdown ul li, .stMarkdown ol li {{
    font-size: 16px !important;
    line-height: 1.8 !important;
    color: var(--text-secondary) !important;
    margin-bottom: 8px;
}}

/* ── Chat messages ── */
[data-testid="stChatMessage"] {{
    background-color: var(--card-bg) !important;
    border-radius: 16px !important;
    border: 1px solid var(--border-color) !important;
    margin-bottom: 20px !important;
    padding: 16px !important;
    box-shadow: none !important;
}}

[data-testid="stChatMessage"] * {{
    color: var(--text-secondary) !important;
}}

[data-testid="stChatMessage"] strong,
[data-testid="stChatMessage"] b {{
    color: var(--text-primary) !important;
}}

[data-testid="stChatMessage"] h1,
[data-testid="stChatMessage"] h2,
[data-testid="stChatMessage"] h3,
[data-testid="stChatMessage"] h4 {{
    color: var(--text-primary) !important;
}}

/* ── Sticky Chat Input Bar (stBottom) ── */
[data-testid="stBottom"] {{
    background-color: var(--bg-app) !important;
    border-top: 1px solid var(--border-color) !important;
}}

[data-testid="stBottom"] > div {{
    background-color: var(--bg-app) !important;
}}

[data-testid="stBottom"] div,
[data-testid="stBottom"] section {{
    background-color: var(--bg-app) !important;
    color: var(--text-primary) !important;
}}

[data-testid="stChatInput"] {{
    max-width: 900px !important;
    margin: 0 auto !important;
    background-color: transparent !important;
    padding-bottom: 24px !important;
}}

[data-testid="stChatInput"] > div {{
    background-color: var(--card-bg) !important;
    border: 1px solid var(--input-border) !important;
    border-radius: 28px !important;
    box-shadow: none !important;
    padding: 4px 8px !important;
}}

[data-testid="stChatInput"] textarea {{
    background-color: transparent !important;
    border: none !important;
    color: var(--text-primary) !important;
    font-size: 15px !important;
}}

[data-testid="stChatInput"] textarea::placeholder {{
    color: var(--text-muted) !important;
    opacity: 0.8 !important;
}}

/* Chat input send button */
[data-testid="stChatInput"] button {{
    background-color: var(--text-primary) !important;
    color: var(--bg-app) !important;
    border: none !important;
    border-radius: 50% !important;
}}

/* ── AI Pipeline Status Box (stStatus) ── */
[data-testid="stStatus"] {{
    background-color: var(--card-bg) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 12px !important;
    color: var(--text-primary) !important;
}}

[data-testid="stStatus"] * {{
    color: var(--text-secondary) !important;
    background-color: transparent !important;
}}

[data-testid="stStatus"] summary,
[data-testid="stStatus"] summary * {{
    color: var(--text-primary) !important;
    font-weight: 600 !important;
    background-color: var(--card-bg) !important;
}}

/* ── Spinner ── */
[data-testid="stSpinner"] {{
    color: var(--text-primary) !important;
}}

[data-testid="stSpinner"] > div {{
    background-color: var(--bg-app) !important;
    color: var(--text-secondary) !important;
}}

/* ── Buttons ── */
button,
[data-testid="stBaseButton-secondary"],
[data-testid="stBaseButton-primary"] {{
    background-color: var(--button-bg) !important;
    color: var(--button-text) !important;
    border: 1px solid var(--button-border) !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    padding: 10px 20px !important;
    transition: all 0.2s ease !important;
}}

button:hover,
[data-testid="stBaseButton-secondary"]:hover,
[data-testid="stBaseButton-primary"]:hover {{
    background-color: var(--button-hover-bg) !important;
    color: var(--button-hover-text) !important;
    border-color: var(--button-hover-bg) !important;
}}

/* Suggested Follow-up chips */
[data-testid="stMain"] button {{
    border-radius: 20px !important;
    padding: 8px 16px !important;
    font-size: 13px !important;
    text-align: left !important;
    height: auto !important;
    white-space: normal !important;
}}

/* ── File Uploader ── */
[data-testid="stFileUploader"] {{
    background-color: var(--card-bg) !important;
    border: 1px dashed var(--border-color) !important;
    border-radius: 12px !important;
    padding: 12px !important;
}}

[data-testid="stFileUploader"] * {{
    color: var(--text-secondary) !important;
}}

[data-testid="stFileUploader"] button {{
    background-color: var(--button-bg) !important;
    color: var(--button-text) !important;
    border: 1px solid var(--button-border) !important;
}}

[data-testid="stFileUploaderDropzone"] {{
    background-color: var(--card-bg) !important;
    border: 2px dashed var(--border-color) !important;
    border-radius: 10px !important;
}}

[data-testid="stFileUploaderDropzone"] * {{
    color: var(--text-muted) !important;
}}

/* ── Text / Number Inputs ── */
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stTextArea"] textarea {{
    background-color: var(--input-bg) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--input-border) !important;
    border-radius: 8px !important;
}}

[data-testid="stTextInput"] label,
[data-testid="stNumberInput"] label,
[data-testid="stTextArea"] label {{
    color: var(--text-primary) !important;
}}

/* ── Selectbox ── */
[data-testid="stSelectbox"] input {{
    pointer-events: none !important;
    caret-color: transparent !important;
}}

div[data-baseweb="select"] > div {{
    background-color: var(--input-bg) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--input-border) !important;
}}

div[data-baseweb="select"] ul {{
    background-color: var(--card-bg) !important;
    color: var(--text-primary) !important;
}}

div[role="listbox"] li {{
    background-color: var(--card-bg) !important;
    color: var(--text-primary) !important;
}}

div[role="listbox"] li:hover {{
    background-color: var(--text-primary) !important;
    color: var(--bg-app) !important;
}}

/* ── Toggle ── */
[data-testid="stToggle"] label {{
    color: var(--text-primary) !important;
}}

/* ── Slider ── */
[data-testid="stSlider"] label,
[data-testid="stSlider"] p {{
    color: var(--text-primary) !important;
}}

/* ── Checkbox / Widget labels ── */
[data-testid="stCheckbox"] label,
[data-testid="stWidgetLabel"] p,
label {{
    color: var(--text-primary) !important;
}}

/* ── Expander ── */
[data-testid="stExpander"] {{
    background-color: var(--card-bg) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 12px !important;
}}

[data-testid="stExpanderDetails"] {{
    background-color: var(--card-bg) !important;
}}

.streamlit-expanderHeader p {{
    color: var(--text-primary) !important;
    font-size: 14px !important;
}}

[data-testid="stExpanderToggleIcon"] svg {{
    fill: var(--text-primary) !important;
}}

/* ── Alert / Info / Warning / Success / Error boxes ── */
[data-testid="stAlert"] {{
    background-color: var(--card-bg) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
}}

[data-testid="stAlert"] * {{
    color: var(--text-secondary) !important;
}}

/* ── Progress bar ── */
[data-testid="stProgress"] > div > div {{
    background-color: var(--text-primary) !important;
}}

[data-testid="stProgress"] {{
    background-color: var(--border-color) !important;
    border-radius: 10px !important;
}}

/* ── Tab overrides ── */
div[data-baseweb="tab-list"] {{
    background-color: var(--bg-app) !important;
    border-bottom: 1px solid var(--border-color) !important;
}}

button[data-baseweb="tab"] {{
    background-color: var(--bg-app) !important;
    color: var(--text-secondary) !important;
    border: none !important;
}}

button[data-baseweb="tab"]:hover {{
    color: var(--text-primary) !important;
}}

button[data-baseweb="tab"][aria-selected="true"] {{
    border-bottom: 2px solid var(--text-primary) !important;
    color: var(--text-primary) !important;
    font-weight: bold !important;
}}

/* ── Sidebar Navigation Radio ── */
div[data-testid="stSidebar"] div[data-testid="stRadio"] > div {{
    gap: 6px !important;
    padding: 0 !important;
}}

div[data-testid="stSidebar"] div[data-testid="stRadio"] label {{
    background-color: var(--card-bg) !important;
    border: 1px solid transparent !important;
    padding: 10px 14px !important;
    border-radius: 10px !important;
    color: var(--text-secondary) !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    display: flex !important;
    align-items: center !important;
    width: 100% !important;
}}

div[data-testid="stSidebar"] div[data-testid="stRadio"] label:hover {{
    background-color: var(--border-color) !important;
    color: var(--text-primary) !important;
}}

div[data-testid="stSidebar"] div[data-testid="stRadio"] label:has(input:checked) {{
    background-color: var(--text-primary) !important;
    color: var(--bg-app) !important;
    border-color: var(--text-primary) !important;
    font-weight: 600 !important;
}}

div[data-testid="stSidebar"] div[data-testid="stRadio"] input {{
    display: none !important;
}}

/* ── Table ── */
table {{
    width: 100% !important;
    border-collapse: collapse !important;
    margin: 15px 0 !important;
}}

th {{
    background-color: var(--card-bg) !important;
    color: var(--text-primary) !important;
    font-weight: 700 !important;
    text-align: left !important;
    padding: 10px 14px !important;
    border-bottom: 2px solid var(--border-color) !important;
}}

td {{
    padding: 10px 14px !important;
    border-bottom: 1px solid var(--border-color) !important;
    color: var(--text-secondary) !important;
    background-color: var(--bg-app) !important;
}}

tr:nth-child(even) td {{
    background-color: var(--card-bg) !important;
}}

tr:hover td {{
    background-color: var(--border-color) !important;
}}

/* ── Captions ── */
.stCaptionContainer, caption, small {{
    color: var(--text-muted) !important;
    font-size: 13px !important;
}}

/* ── Divider ── */
hr {{
    border-color: var(--border-color) !important;
    margin: 20px 0 !important;
}}

/* ── Sidebar Toggle Visibility ── */
div[data-testid="collapsedControl"],
button[data-testid="stSidebarCollapseButton"] {{
    opacity: 1 !important;
    visibility: visible !important;
    color: var(--text-primary) !important;
}}

/* ── Topic pills ── */
.topic-pill {{
    display: inline-block;
    background-color: var(--card-bg) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 20px;
    padding: 4px 12px;
    margin: 4px;
    font-size: 12px;
    font-weight: 500;
    color: var(--text-primary) !important;
}}

/* ── Intent badge ── */
.intent-badge {{
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    margin-bottom: 12px;
    background-color: var(--card-bg) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border-color) !important;
}}

/* ── Source card ── */
.source-card {{
    background-color: var(--card-bg) !important;
    border: 1px solid var(--border-color) !important;
    border-left: 4px solid var(--text-primary) !important;
    border-radius: 8px;
    padding: 12px 14px;
    margin-bottom: 8px;
    font-size: 13px;
    color: var(--text-secondary) !important;
    line-height: 1.6;
}}

.source-card b {{
    color: var(--text-primary) !important;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}

/* ── Grounding badge ── */
.ground-badge {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
    margin-top: 12px;
    background-color: var(--card-bg) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border-color) !important;
}}

/* ── Error Cards ── */
.error-card {{
    background-color: var(--card-bg) !important;
    border: 1px solid var(--border-color) !important;
    border-left: 4px solid var(--text-primary) !important;
    border-radius: 12px !important;
    padding: 20px !important;
    margin-bottom: 20px !important;
    box-shadow: none !important;
}}

.error-title-text {{
    font-size: 16px !important;
    font-weight: 700 !important;
    color: var(--text-primary) !important;
    margin-left: 8px !important;
    display: inline-block !important;
    vertical-align: middle !important;
}}

.error-icon-span {{
    font-size: 20px !important;
    display: inline-block !important;
    vertical-align: middle !important;
}}

.error-card-desc {{
    font-size: 14px !important;
    line-height: 1.6 !important;
    color: var(--text-secondary) !important;
    margin-top: 10px !important;
    margin-bottom: 12px !important;
}}

.error-card-fix {{
    background-color: var(--bg-app) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 8px !important;
    padding: 12px 16px !important;
    margin-top: 10px !important;
}}

.error-card-fix strong {{
    color: var(--text-primary) !important;
    font-size: 13px !important;
    display: block !important;
    margin-bottom: 6px !important;
}}

.error-card-fix p {{
    font-size: 13px !important;
    line-height: 1.5 !important;
    color: var(--text-secondary) !important;
    margin: 0 !important;
    white-space: pre-line !important;
}}

/* ── Vis.js Graph Canvas container ── */
.graph-container {{
    width: 100%;
    height: 500px;
    border: 1px solid var(--border-color) !important;
    border-radius: 12px;
    background-color: var(--bg-app) !important;
    box-shadow: none;
}}

/* ── Interview simulation cards ── */
.interview-avatar-card {{
    display: flex;
    align-items: center;
    gap: 16px;
    background-color: var(--card-bg) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 16px;
    padding: 16px;
    margin-bottom: 20px;
    box-shadow: none;
}}

.interview-avatar {{
    width: 48px;
    height: 48px;
    background-color: var(--card-bg) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
}}

.interview-avatar-text h4 {{
    margin: 0 !important;
    font-size: 16px !important;
    font-weight: 700;
    color: var(--text-primary) !important;
}}

.interview-avatar-text p {{
    margin: 0 !important;
    font-size: 12px !important;
    color: var(--text-secondary) !important;
}}

/* ── Score chips ── */
.score-chip-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
    gap: 10px;
    margin: 15px 0;
}}

.score-chip {{
    background-color: var(--card-bg) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 10px;
    padding: 10px;
    text-align: center;
}}

.score-chip span {{
    font-size: 11px;
    color: var(--text-muted) !important;
    display: block;
    text-transform: uppercase;
    font-weight: 600;
}}

.score-chip strong {{
    font-size: 18px;
    color: var(--text-primary) !important;
    font-family: 'Outfit', sans-serif;
}}

/* ── Scrollbar ── */
::-webkit-scrollbar {{ width: 6px; }}
::-webkit-scrollbar-track {{ background: var(--bg-app); }}
::-webkit-scrollbar-thumb {{ background: var(--border-color); border-radius: 3px; }}
::-webkit-scrollbar-thumb:hover {{ background: var(--text-muted); }}
</style>
""", unsafe_allow_html=True)


def render_global_header():
    """Render a premium top-bar header containing platform brand identity and model state."""
    import streamlit as st
    provider = st.session_state.get("settings_provider", "Ollama").title()
    model = st.session_state.get("settings_model", "llama3.2")
    
    header_html = f"""
    <div class="global-header">
        <div class="header-left">
            <span class="logo-icon">🧠</span>
            <span class="brand-name">DocIntel AI <span class="brand-badge">Platform</span></span>
        </div>
        <div class="header-right">
            <div class="status-indicator">
                <span class="status-dot"></span>
                <span class="status-text">{provider} · {model}</span>
            </div>
            <div class="avatar-profile">ME</div>
        </div>
    </div>
    <div class="header-spacer"></div>
    """
    st.markdown(header_html, unsafe_allow_html=True)
