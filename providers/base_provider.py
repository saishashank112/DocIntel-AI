from abc import ABC, abstractmethod
from typing import Iterator, List

class LLMResponse:
    def __init__(self, content: str):
        self.content = content

class PlatformError(Exception):
    """Base exception for DocIntel AI Platform."""
    def __init__(self, message: str, technical_details: str = None):
        super().__init__(message)
        self.technical_details = technical_details

class ProviderConnectionError(PlatformError):
    """Failed to connect to the model provider endpoint."""
    pass

class ProviderConfigurationError(PlatformError):
    """Missing or invalid credentials, keys, or endpoints."""
    pass

class ProviderModelError(PlatformError):
    """Selected model is invalid, not pulled, or not supported."""
    pass

class RetrievalError(PlatformError):
    """Error during document indexing, retrieval, or embedding extraction."""
    pass

class ValidationError(PlatformError):
    """Failed validation check on inputs or parameters."""
    pass

class BaseProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        """Generate response text for the given prompt."""
        pass

    @abstractmethod
    def embed(self, text: str) -> List[float]:
        """Generate numerical embedding list for the given text."""
        pass

    @abstractmethod
    def stream(self, prompt: str) -> Iterator[str]:
        """Stream response generator for the given prompt."""
        pass

    @abstractmethod
    def health_check(self) -> bool:
        """Check status / connection capability of the provider."""
        pass

    def invoke(self, prompt: str) -> LLMResponse:
        """Helper to mimic LangChain invocation footprint."""
        return LLMResponse(self.generate(prompt))

