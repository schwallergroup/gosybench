"""Data extractors for segments of chemical synthesis paragraphs."""

import os
from typing import Any, List, Optional

import instructor  # type: ignore
from anthropic import Anthropic, AsyncAnthropic  # type: ignore
from dotenv import load_dotenv
from openai import AsyncOpenAI, OpenAI  # type: ignore
from pydantic import BaseModel, model_validator

from .substances import Product


class ExtractReaction(BaseModel):
    llm: str = "gpt-4-0613"
    client: Optional[Any] = None
    aclient: Optional[Any] = None

    def __call__(self, text: str) -> List[Product]:
        """Execute the extraction pipeline for a single paragraph."""
        product = Product.from_paragraph(text, self.client, self.llm)
        return product

    async def async_call(self, text: str) -> List[Product]:
        """Execute the extraction pipeline for a paragraph asynchronously."""
        product = await Product.async_from_paragraph(
            text, self.aclient, self.llm
        )
        return product

    @model_validator(mode="after")
    def init_llm_synthex(self):
        """Set the llm and synthesis extractor."""

        self.set_llm(self.llm)
        return self

    def set_llm(self, model: str):
        """Set the language model to be used."""

        load_dotenv()
        if model.startswith("gpt"):
            self.client = instructor.patch(OpenAI())
            self.aclient = instructor.apatch(AsyncOpenAI())

        elif model.startswith("mistral") or ("mixtral" in model):
            url = "https://api.mistral.ai/v1/"
            api_key = os.getenv("MISTRAL_API_KEY")

            self.client = instructor.from_openai(
                OpenAI(base_url=url, api_key=api_key),
                mode=instructor.Mode.JSON,
            )
            self.aclient = instructor.from_openai(
                AsyncOpenAI(base_url=url, api_key=api_key),
                mode=instructor.Mode.JSON,
            )

        elif model.startswith("claude"):

            self.client = instructor.from_anthropic(
                Anthropic(
                    api_key=os.getenv("ANTHROPIC_API_KEY"),
                ),
            )
            self.aclient = instructor.from_anthropic(
                AsyncAnthropic(
                    api_key=os.getenv("ANTHROPIC_API_KEY"),
                ),
            )
        else:
            raise ValueError(f"Model {model} not recognized.")
