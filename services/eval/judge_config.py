"""
Judge LLM configuration for RAG evaluation.

Default: gemma4:cloud via Ollama Cloud (free tier) — deliberately a different
model family from the generation model (gpt-oss:120b-cloud) to avoid
self-preference bias in evaluation scores.

Override via environment variables:
  JUDGE_PROVIDER=ollama        → gemma4:cloud via local/cloud Ollama (default)
  JUDGE_PROVIDER=gemini        → Google AI Studio / Gemini API (requires GEMINI_API_KEY or GOOGLE_API_KEY)
  JUDGE_PROVIDER=openrouter    → requires OPENROUTER_API_KEY
  JUDGE_PROVIDER=anthropic     → requires ANTHROPIC_API_KEY

  JUDGE_MODEL=<model-name>     → override the model within the chosen provider
"""
import os

from langchain_openai import ChatOpenAI
from ragas.llms import LangchainLLMWrapper


def get_judge_llm() -> LangchainLLMWrapper:
    """
    Returns a Ragas-compatible LangchainLLMWrapper for the judge model.

    The judge model is deliberately chosen from a different model family than
    the generation model (gpt-oss:120b-cloud) to avoid self-preference bias —
    a known failure mode where the same model family consistently rates its own
    outputs higher than an independent evaluator would.
    """
    provider = os.getenv("JUDGE_PROVIDER", "ollama").lower()

    if provider == "ollama":
        llm = ChatOpenAI(
            model=os.getenv("JUDGE_MODEL", "gemma4:cloud"),
            base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434") + "/v1",
            api_key="ollama",  # placeholder — Ollama does not require a real key
            temperature=0,
        )
    elif provider in ("gemini", "google"):
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY or GOOGLE_API_KEY must be set when JUDGE_PROVIDER=gemini")
        llm = ChatOpenAI(
            model=os.getenv("JUDGE_MODEL", "gemini-2.0-flash").strip(),
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
            api_key=api_key,
            temperature=0,
        )
    elif provider == "openrouter":
        llm = ChatOpenAI(
            model=os.getenv("JUDGE_MODEL", "nvidia/nemotron-3-ultra-550b-a55b:free"),
            base_url="https://openrouter.ai/api/v1",
            api_key=os.environ["OPENROUTER_API_KEY"],
            temperature=0,
        )
    elif provider == "anthropic":
        llm = ChatOpenAI(
            model=os.getenv("JUDGE_MODEL", "claude-sonnet-4-5"),
            base_url="https://api.anthropic.com/v1",
            api_key=os.environ["ANTHROPIC_API_KEY"],
            temperature=0,
        )
    else:
        raise ValueError(
            f"Unknown JUDGE_PROVIDER: {provider!r}. "
            "Valid values: ollama, gemini, openrouter, anthropic"
        )

    return LangchainLLMWrapper(llm)


def get_judge_llm_raw() -> ChatOpenAI:
    """
    Returns the raw ChatOpenAI instance (for DeepEval which wraps it itself).
    """
    provider = os.getenv("JUDGE_PROVIDER", "ollama").lower()

    if provider == "ollama":
        return ChatOpenAI(
            model=os.getenv("JUDGE_MODEL", "gemma4:cloud"),
            base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434") + "/v1",
            api_key="ollama",
            temperature=0,
            model_kwargs={"response_format": {"type": "json_object"}},
        )
    elif provider in ("gemini", "google"):
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY or GOOGLE_API_KEY must be set when JUDGE_PROVIDER=gemini")
        return ChatOpenAI(
            model=os.getenv("JUDGE_MODEL", "gemini-2.0-flash").strip(),
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
            api_key=api_key,
            temperature=0,
        )
    elif provider == "openrouter":
        return ChatOpenAI(
            model=os.getenv("JUDGE_MODEL", "nvidia/nemotron-3-ultra-550b-a55b:free"),
            base_url="https://openrouter.ai/api/v1",
            api_key=os.environ["OPENROUTER_API_KEY"],
            temperature=0,
        )
    elif provider == "anthropic":
        return ChatOpenAI(
            model=os.getenv("JUDGE_MODEL", "claude-sonnet-4-5"),
            base_url="https://api.anthropic.com/v1",
            api_key=os.environ["ANTHROPIC_API_KEY"],
            temperature=0,
        )
    else:
        raise ValueError(
            f"Unknown JUDGE_PROVIDER: {provider!r}. "
            "Valid values: ollama, gemini, openrouter, anthropic"
        )


def get_judge_embeddings():
    """
    Returns a local HuggingFace embedding model for Ragas metrics
    (like AnswerRelevancy) so it does not fallback to OpenAI API.
    """
    from langchain_huggingface import HuggingFaceEmbeddings
    # all-MiniLM-L6-v2 is the same default model Chroma uses locally.
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


try:
    from deepeval.models.base_model import DeepEvalBaseLLM

    class DeepEvalJudgeLLM(DeepEvalBaseLLM):
        def __init__(self, chat_model: ChatOpenAI):
            self.model = chat_model

        def load_model(self):
            return self.model

        def generate(self, prompt: str) -> str:
            res = self.model.invoke(prompt)
            return str(res.content)

        async def a_generate(self, prompt: str) -> str:
            res = await self.model.ainvoke(prompt)
            return str(res.content)

        def get_model_name(self) -> str:
            return getattr(self.model, "model_name", getattr(self.model, "model", "judge_model"))

    def get_deepeval_judge_llm() -> DeepEvalJudgeLLM:
        return DeepEvalJudgeLLM(get_judge_llm_raw())
except ImportError:
    pass
