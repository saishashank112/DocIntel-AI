import requests
from typing import Iterator, List
from providers.base_provider import BaseProvider

class AnthropicProvider(BaseProvider):
    def __init__(self, api_key: str, model: str = "claude-3-5-sonnet-20241022"):
        self.api_key = api_key
        self.model = model
        self.headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }

    def generate(self, prompt: str) -> str:
        if not self.api_key:
            return "Anthropic Error: API key is missing. Configure it in Settings."
        try:
            resp = requests.post("https://api.anthropic.com/v1/messages", json={
                "model": self.model,
                "max_tokens": 4000,
                "messages": [{"role": "user", "content": prompt}]
            }, headers=self.headers, timeout=30)
            if resp.status_code == 200:
                return resp.json()["content"][0]["text"]
            return f"Anthropic Error: {resp.json().get('error', {}).get('message', 'Unknown error')}"
        except Exception as e:
            return f"Anthropic Connection Error: {str(e)}"

    def embed(self, text: str) -> List[float]:
        # Anthropic does not provide default embedding APIs.
        return []

    def stream(self, prompt: str) -> Iterator[str]:
        if not self.api_key:
            yield "Anthropic Error: API key is missing."
            return
        try:
            resp = requests.post("https://api.anthropic.com/v1/messages", json={
                "model": self.model,
                "max_tokens": 4000,
                "messages": [{"role": "user", "content": prompt}],
                "stream": True
            }, headers=self.headers, stream=True, timeout=30)
            for line in resp.iter_lines():
                if line:
                    import json
                    decoded = line.decode("utf-8").strip()
                    if decoded.startswith("data: "):
                        data = json.loads(decoded[6:])
                        if data.get("type") == "content_block_delta":
                            yield data["delta"].get("text", "")
        except Exception as e:
            yield f"\nAnthropic Stream Error: {str(e)}"

    def health_check(self) -> bool:
        if not self.api_key:
            return False
        try:
            resp = requests.post("https://api.anthropic.com/v1/messages", json={
                "model": self.model,
                "max_tokens": 5,
                "messages": [{"role": "user", "content": "ping"}]
            }, headers=self.headers, timeout=5)
            return resp.status_code == 200
        except Exception:
            return False
