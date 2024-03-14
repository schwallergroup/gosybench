"""Pydantic model configuration for the LLM API."""

from __future__ import annotations

from pydantic import BaseModel


class LLMConfig(BaseModel):
    """Pydantic model configuration."""

    temperature: float = 0.2
    timeout: int = 120
    max_retries: int = 2


config = LLMConfig()
