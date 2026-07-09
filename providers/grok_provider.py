import requests
from typing import Iterator, List
from providers.openai_provider import OpenAIProvider

class GrokProvider(OpenAIProvider):
    def __init__(self, api_key: str, model: str = "grok-2-1212"):
        super().__init__(api_key, model=model)

    def generate(self, prompt: str) -> str:
        if not self.api_key:
            return "Grok Error: API key is missing. Configure it in Settings."
        try:
            resp = requests.post("https://api.x.ai/v1/chat/completions", json={
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0
            }, headers=self.headers, timeout=30)
            if resp.status_code == 200:
                return resp.json()["choices"][0]["message"]["content"]
            return f"Grok Error: Status {resp.status_code}"
        except Exception as e:
            return f"Grok Connection Error: {str(e)}"

    def stream(self, prompt: str) -> Iterator[str]:
        if not self.api_key:
            yield "Grok Error: API key is missing."
            return
        try:
            resp = requests.post("https://api.x.ai/v1/chat/completions", json={
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
            yield f"\nGrok Stream Error: {str(e)}"
