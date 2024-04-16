"""Pydantic model configuration for the LLM API."""

from __future__ import annotations

from pydantic import BaseModel


class LLMConfig(BaseModel):
    """Pydantic model configuration."""

    temperature: float = 0.05
    timeout: int = 120
    max_retries: int = 2
    max_tokens: int = 2000


config = LLMConfig()
