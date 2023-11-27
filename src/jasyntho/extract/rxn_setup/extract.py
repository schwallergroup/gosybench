"""Data extraction from reaction setup text segments."""

import instructor  # type: ignore
from dotenv import load_dotenv
from openai import AsyncOpenAI, OpenAI  # type: ignore

from .typing import Product


class ReactionSetup:
    """Extraction of structured data from reaction-setup snippet."""

    def __init__(self, api_key=None):
        """Initialize the extractor."""
        load_dotenv()

        self.llm = "gpt-3.5-turbo"
        self.llm = "gpt-4-1106-preview"
        self.llm = "gpt-4"
        self.client = instructor.patch(OpenAI())
        self.aclient = instructor.apatch(AsyncOpenAI())

    def __call__(self, text: str) -> Product:
        """Execute the extraction pipeline for a single paragraph."""
        product = Product.from_paragraph(text, self.client, self.llm)
        return product

    async def async_call(self, text: str) -> Product:
        """Execute the extraction pipeline for a paragraph asynchronously."""
        product = Product.async_from_paragraph(text, self.aclient, self.llm)
        return await product
