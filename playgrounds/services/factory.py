from .openai_service import OpenAIService
from .ollama_service import OllamaService


def get_llm_service(provider_name):
    if provider_name == "openai":
        return OpenAIService()
    elif provider_name == "ollama":
        return OllamaService()
    else:
        raise ValueError(f"Unsupported provider: {provider_name}")
