import requests
from typing import Iterator, List
from providers.base_provider import BaseProvider, ProviderConnectionError, ProviderConfigurationError, ProviderModelError, PlatformError

class OpenAIProvider(BaseProvider):
    def __init__(self, api_key: str, model: str = "gpt-4o", embed_model: str = "text-embedding-3-small"):
        self.api_key = api_key
        self.model = model
        self.embed_model = embed_model
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def generate(self, prompt: str) -> str:
        if not self.api_key:
            raise ProviderConfigurationError("OpenAI API key is missing. Configure it in Settings.")
        try:
            resp = requests.post("https://api.openai.com/v1/chat/completions", json={
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0
            }, headers=self.headers, timeout=30)
            if resp.status_code == 200:
                return resp.json()["choices"][0]["message"]["content"]
            
            err_data = resp.json().get('error', {})
            err_msg = err_data.get('message', 'Unknown error')
            err_code = err_data.get('code', '')
            
            if resp.status_code == 401:
                raise ProviderConfigurationError(f"OpenAI Authentication Failed: {err_msg}", technical_details=f"Status: 401, Code: {err_code}")
            elif resp.status_code == 404:
                raise ProviderModelError(f"OpenAI Model Error: {err_msg}", technical_details=f"Status: 404, Code: {err_code}")
            
            raise ProviderConnectionError(f"OpenAI API error {resp.status_code}: {err_msg}")
        except PlatformError:
            raise
        except Exception as e:
            raise ProviderConnectionError(f"OpenAI connection error: {str(e)}")

    def embed(self, text: str) -> List[float]:
        if not self.api_key:
            return []
        try:
            resp = requests.post("https://api.openai.com/v1/embeddings", json={
                "model": self.embed_model,
                "input": text
            }, headers=self.headers, timeout=10)
            if resp.status_code == 200:
                return resp.json()["data"][0]["embedding"]
            return []
        except Exception:
            return []

    def stream(self, prompt: str) -> Iterator[str]:
        if not self.api_key:
            raise ProviderConfigurationError("OpenAI API key is missing.")
        try:
            resp = requests.post("https://api.openai.com/v1/chat/completions", json={
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "stream": True
            }, headers=self.headers, stream=True, timeout=30)
            if resp.status_code != 200:
                err_msg = resp.json().get('error', {}).get('message', 'Unknown error')
                raise ProviderConnectionError(f"OpenAI stream error {resp.status_code}: {err_msg}")
            for line in resp.iter_lines():
                if line:
                    decoded = line.decode("utf-8").strip()
                    if decoded.startswith("data: ") and decoded != "data: [DONE]":
                        import json
                        data = json.loads(decoded[6:])
                        delta = data["choices"][0].get("delta", {})
                        if "content" in delta:
                            yield delta["content"]
        except PlatformError:
            raise
        except Exception as e:
            raise ProviderConnectionError(f"\nOpenAI Stream Error: {str(e)}")

    def health_check(self) -> bool:
        if not self.api_key:
            return False
        try:
            resp = requests.post("https://api.openai.com/v1/chat/completions", json={
                "model": self.model,
                "messages": [{"role": "user", "content": "ping"}],
                "max_tokens": 5
            }, headers=self.headers, timeout=5)
            return resp.status_code == 200
        except Exception:
            return False
