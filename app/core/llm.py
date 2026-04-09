from langchain_core.language_models import BaseLanguageModel
from config.settings import settings

# Module-level singleton — reuse the same client instance across requests
_llm_instance = None


def get_llm() -> BaseLanguageModel:
    global _llm_instance
    if _llm_instance is None:
        from langchain_anthropic import ChatAnthropic
        _llm_instance = ChatAnthropic(
            model=settings.llm_model,
            api_key=settings.anthropic_api_key,
            temperature=0,
        )
    return _llm_instance
