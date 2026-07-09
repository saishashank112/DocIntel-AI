import requests
from typing import Iterator, List
from providers.base_provider import BaseProvider, ProviderConnectionError, ProviderModelError, PlatformError

class OllamaProvider(BaseProvider):
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama3.2", embed_model: str = "nomic-embed-text"):
        self.base_url = base_url
        self.model = model
        self.embed_model = embed_model

    def generate(self, prompt: str) -> str:
        try:
            resp = requests.post(f"{self.base_url}/api/generate", json={
                "model": self.model,
                "prompt": prompt,
                "stream": False
            }, timeout=90)
            if resp.status_code == 200:
                return resp.json().get("response", "")
            
            # Extract Ollama message if any
            err_msg = resp.text
            try:
                err_json = resp.json()
                if "error" in err_json:
                    err_msg = err_json["error"]
            except Exception:
                pass
            
            if resp.status_code == 404 or "not found" in err_msg.lower():
                raise ProviderModelError(
                    f"Selected model '{self.model}' is not installed in Ollama.",
                    technical_details=f"Ollama returned status {resp.status_code}: {err_msg}"
                )
            raise ProviderConnectionError(
                f"Ollama returned error status {resp.status_code}",
                technical_details=f"Response: {err_msg}"
            )
        except requests.exceptions.Timeout as e:
            raise ProviderConnectionError(
                "Request to Ollama timed out. The local model is taking too long to load or respond.",
                technical_details=str(e)
            )
        except requests.exceptions.ConnectionError as e:
            raise ProviderConnectionError(
                "Could not connect to Ollama. Verify that Ollama is running and accessible.",
                technical_details=str(e)
            )
        except PlatformError:
            raise
        except Exception as e:
            raise ProviderConnectionError(
                "An unexpected error occurred while communicating with Ollama.",
                technical_details=str(e)
            )

    def embed(self, text: str) -> List[float]:
        try:
            resp = requests.post(f"{self.base_url}/api/embeddings", json={
                "model": self.embed_model,
                "prompt": text
            }, timeout=10)
            if resp.status_code == 200:
                return resp.json().get("embedding", [])
            return []
        except Exception:
            return []

    def stream(self, prompt: str) -> Iterator[str]:
        try:
            resp = requests.post(f"{self.base_url}/api/generate", json={
                "model": self.model,
                "prompt": prompt,
                "stream": True
            }, stream=True, timeout=90)
            
            if resp.status_code != 200:
                err_msg = resp.text
                try:
                    err_json = resp.json()
                    if "error" in err_json:
                        err_msg = err_json["error"]
                except Exception:
                    pass
                if resp.status_code == 404 or "not found" in err_msg.lower():
                    raise ProviderModelError(f"Model '{self.model}' not found.", technical_details=err_msg)
                raise ProviderConnectionError(f"Ollama stream error {resp.status_code}", technical_details=err_msg)

            for line in resp.iter_lines():
                if line:
                    import json
                    data = json.loads(line.decode("utf-8"))
                    yield data.get("response", "")
        except requests.exceptions.Timeout as e:
            raise ProviderConnectionError("Request to Ollama timed out.", technical_details=str(e))
        except requests.exceptions.ConnectionError as e:
            raise ProviderConnectionError("Could not connect to Ollama.", technical_details=str(e))
        except PlatformError:
            raise
        except Exception as e:
            raise ProviderConnectionError("Unexpected error in Ollama streaming.", technical_details=str(e))

    def health_check(self) -> bool:
        try:
            resp = requests.get(self.base_url, timeout=3)
            if resp.status_code == 200:
                # Also verify if model exists/works if possible, but basic status is enough
                return True
            return False
        except Exception:
            return False
