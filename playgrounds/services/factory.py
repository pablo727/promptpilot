from .openai_service.py import OpenAIService


def get_llm_service(provider_name):
    if provider_name == "openai":
        return OpenAIService()
    raise ValueError(f"Unsupported provider: {provider_name}")
