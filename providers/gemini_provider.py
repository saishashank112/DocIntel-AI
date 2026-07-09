import requests
from typing import Iterator, List
from providers.base_provider import BaseProvider

class GeminiProvider(BaseProvider):
    def __init__(self, api_key: str, model: str = "gemini-1.5-flash"):
        self.api_key = api_key
        self.model = model

    def generate(self, prompt: str) -> str:
        if not self.api_key:
            return "Gemini Error: API key is missing. Configure it in Settings."
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
            resp = requests.post(url, json={
                "contents": [{"parts": [{"text": prompt}]}]
            }, timeout=30)
            if resp.status_code == 200:
                return resp.json()["candidates"][0]["content"]["parts"][0]["text"]
            return f"Gemini Error: Status {resp.status_code}"
        except Exception as e:
            return f"Gemini Connection Error: {str(e)}"

    def embed(self, text: str) -> List[float]:
        return []

    def stream(self, prompt: str) -> Iterator[str]:
        yield self.generate(prompt)

    def health_check(self) -> bool:
        if not self.api_key:
            return False
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
            resp = requests.post(url, json={
                "contents": [{"parts": [{"text": "ping"}]}]
            }, timeout=5)
            return resp.status_code == 200
        except Exception:
            return False
