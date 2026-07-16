import re

import logfire
from langchain_groq import ChatGroq
from nemoguardrails import RailsConfig, LLMRails

from app.config import settings
from app.guardrails.colang_rules import (
    COLANG_CONTENT,
    YAML_CONTENT,
    RAIL_INDICATORS,
    HEURISTIC_RULES,
)


_rails: LLMRails | None = None


def _apply_heuristic_guardrails(message: str) -> tuple[bool, str | None]:
    """Apply deterministic keyword-based guardrails before the LLM-based runtime."""
    if not message or not message.strip():
        return False, None

    normalized = re.sub(r"[^a-z0-9]+", " ", message.lower()).strip()
    if not normalized:
        return False, None

    for _, pattern, response in HEURISTIC_RULES:
        if re.search(pattern, normalized):
            return True, response

    return False, None


def initialize_rails() -> None:
    """
    Build the NeMo LLMRails singleton at app startup.
    Uses llama-3.1-8b-instant for fast intent classification at the gate —
    the heavier llama-3.3-70b-versatile is reserved for the RAG pipeline.
    """
    global _rails

    guard_llm = ChatGroq(
        api_key=settings.GROQ_API_KEY,
        model="llama-3.1-8b-instant",
        temperature=0
    )

    config = RailsConfig.from_content(
        colang_content=COLANG_CONTENT,
        yaml_content=YAML_CONTENT
    )

    _rails = LLMRails(config, llm=guard_llm)
    logfire.info("🛡️ NeMo Guardrails initialised (llama-3.1-8b-instant).")
    
    


def guard(message: str) -> tuple[bool, str | None]:
    """
    Run a user message through the guardrail gate.

    Returns:
        (True,  rail_response) — a rail fired; return this response immediately,
                                skip the RAG pipeline entirely.
        (False, None)          — message is clean; proceed to LangGraph.
    """
    heuristic_fired, heuristic_response = _apply_heuristic_guardrails(message)
    if heuristic_fired:
        logfire.info(f"🛡️ Guardrails fired via heuristic | query='{message[:80]}'")
        return True, heuristic_response

    if _rails is None:
        logfire.warning("⚠️ Guardrails not initialised — skipping gate.")
        return False, None

    with logfire.span("🛡️ Guardrails Check"):
        try:
            result = _rails.generate(messages=[{"role": "user", "content": message}])
        except Exception as exc:
            logfire.warning(f"⚠️ Guardrails LLM check failed: {exc}")
            return False, None

        # NeMo returns {'role': 'assistant', 'content': '...'} — extract text
        content = result.get("content", "") if isinstance(result, dict) else str(result)

        fired = any(indicator in content for indicator in RAIL_INDICATORS)

        if fired:
            logfire.info(f"🛡️ Guardrails fired | query='{message[:80]}'")
            return True, content

        logfire.info("✅ Guardrails passed.")
        return False, None