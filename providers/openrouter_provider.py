import requests
from typing import Iterator, List
from providers.openai_provider import OpenAIProvider

class OpenRouterProvider(OpenAIProvider):
    def __init__(self, api_key: str, model: str = "google/gemini-2.0-flash-exp:free"):
        super().__init__(api_key, model=model)
        self.headers.update({
            "HTTP-Referer": "https://localhost:8501",
            "X-Title": "DocIntel AI Platform"
        })

    def generate(self, prompt: str) -> str:
        if not self.api_key:
            return "OpenRouter Error: API key is missing. Configure it in Settings."
        try:
            resp = requests.post("https://openrouter.ai/api/v1/chat/completions", json={
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}]
            }, headers=self.headers, timeout=30)
            if resp.status_code == 200:
                return resp.json()["choices"][0]["message"]["content"]
            return f"OpenRouter Error: Status {resp.status_code} - {resp.text}"
        except Exception as e:
            return f"OpenRouter Connection Error: {str(e)}"

    def stream(self, prompt: str) -> Iterator[str]:
        if not self.api_key:
            yield "OpenRouter Error: API key is missing."
            return
        try:
            resp = requests.post("https://openrouter.ai/api/v1/chat/completions", json={
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "stream": True
            }, headers=self.headers, stream=True, timeout=30)
            for line in resp.iter_lines():
                if line:
                    decoded = line.decode("utf-8").strip()
                    if decoded.startswith("data: ") and decoded != "data: [DONE]":
                        import json
                        data = json.loads(decoded[6:])
                        delta = data["choices"][0].get("delta", {})
                        if "content" in delta:
                            yield delta["content"]
        except Exception as e:
            yield f"\nOpenRouter Stream Error: {str(e)}"
