from dataclasses import dataclass

import requests

from config import (
    GROQ_API_KEY,
    GROQ_MODEL,
    LLM_PROVIDER,
    OLLAMA_BASE_URL,
    OLLAMA_MODEL,
    OPENROUTER_API_KEY,
    OPENROUTER_MODEL,
)


@dataclass
class LLMResult:
    text: str
    provider: str
    model: str


def call_llm(prompt: str, system: str = "", provider: str | None = None) -> LLMResult:
    selected = (provider or LLM_PROVIDER or "mock").lower()
    if selected == "groq" and GROQ_API_KEY:
        return _call_openai_compatible(
            "https://api.groq.com/openai/v1/chat/completions",
            GROQ_API_KEY,
            GROQ_MODEL,
            prompt,
            system,
            "groq",
        )
    if selected == "openrouter" and OPENROUTER_API_KEY:
        return _call_openai_compatible(
            "https://openrouter.ai/api/v1/chat/completions",
            OPENROUTER_API_KEY,
            OPENROUTER_MODEL,
            prompt,
            system,
            "openrouter",
        )
    if selected == "ollama":
        return _call_ollama(prompt, system)
    return LLMResult(text="", provider="mock", model="deterministic-fallback")


def _call_openai_compatible(
    url: str,
    api_key: str,
    model: str,
    prompt: str,
    system: str,
    provider: str,
) -> LLMResult:
    response = requests.post(
        url,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={
            "model": model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.8,
        },
        timeout=90,
    )
    response.raise_for_status()
    text = response.json()["choices"][0]["message"]["content"]
    return LLMResult(text=text, provider=provider, model=model)


def _call_ollama(prompt: str, system: str) -> LLMResult:
    response = requests.post(
        f"{OLLAMA_BASE_URL}/api/chat",
        json={
            "model": OLLAMA_MODEL,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
            "stream": False,
        },
        timeout=180,
    )
    response.raise_for_status()
    return LLMResult(
        text=response.json()["message"]["content"],
        provider="ollama",
        model=OLLAMA_MODEL,
    )
