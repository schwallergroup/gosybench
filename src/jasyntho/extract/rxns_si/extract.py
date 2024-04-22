"""Extract data from paragraphs in the SI of papers."""

import os
from typing import List

import instructor  # type: ignore
from anthropic import Anthropic, AsyncAnthropic  # type: ignore
from dotenv import load_dotenv
from openai import AsyncOpenAI, OpenAI  # type: ignore

from ..substances import Product


class ReactionSetup:
    """Extraction of structured data from reaction-setup snippet."""

    def __init__(self, api_key=None, model="gpt-4-0613"):
        """Initialize the extractor."""
        load_dotenv()

        self.llm = model
        self.set_llm(model)

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

    def set_llm(self, model: str):
        """Set the language model to be used."""

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
