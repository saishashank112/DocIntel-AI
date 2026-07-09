import streamlit as st
from config.settings import LLM_MODEL
from providers.ollama_provider import OllamaProvider
from providers.openai_provider import OpenAIProvider
from providers.anthropic_provider import AnthropicProvider
from providers.gemini_provider import GeminiProvider
from providers.grok_provider import GrokProvider
from providers.openrouter_provider import OpenRouterProvider

def get_llm():
    """Instantiate and return the selected provider dynamically based on settings."""
    # Enforce default settings in session state
    if "settings_provider" not in st.session_state:
        st.session_state.settings_provider = "ollama"
    if "settings_model" not in st.session_state:
        st.session_state.settings_model = "llama3.2"
    if "api_keys" not in st.session_state:
        st.session_state.api_keys = {
            "openai": "",
            "anthropic": "",
            "grok": "",
            "gemini": "",
            "openrouter": ""
        }

    provider = st.session_state.settings_provider.lower()
    model = st.session_state.settings_model
    keys = st.session_state.api_keys

    if provider == "openai":
        return OpenAIProvider(api_key=keys.get("openai", ""), model=model)
    elif provider == "anthropic":
        return AnthropicProvider(api_key=keys.get("anthropic", ""), model=model)
    elif provider == "gemini":
        return GeminiProvider(api_key=keys.get("gemini", ""), model=model)
    elif provider == "grok":
        return GrokProvider(api_key=keys.get("grok", ""), model=model)
    elif provider == "openrouter":
        return OpenRouterProvider(api_key=keys.get("openrouter", ""), model=model)
    else:
        return OllamaProvider(model=model)
