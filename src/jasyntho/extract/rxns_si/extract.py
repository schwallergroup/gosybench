"""Extract data from paragraphs in the SI of papers."""

from typing import List

import instructor  # type: ignore
from dotenv import load_dotenv
from openai import AsyncOpenAI, OpenAI  # type: ignore

from ..substances import Product


class ReactionSetup:
    """Extraction of structured data from reaction-setup snippet."""

    def __init__(self, api_key=None, model="gpt-4-0314"):
        """Initialize the extractor."""
        load_dotenv()

        self.llm = model
        self.client = instructor.patch(OpenAI())
        self.aclient = instructor.apatch(AsyncOpenAI())

    def __call__(self, text: str) -> List[Product]:
        """Execute the extraction pipeline for a single paragraph."""
        print(text)
        print(self.client)
        print(self.llm)
        product = Product.from_paragraph(text, self.client, self.llm)
        return product

    async def async_call(self, text: str) -> List[Product]:
        """Execute the extraction pipeline for a paragraph asynchronously."""
        product = await Product.async_from_paragraph(
            text, self.aclient, self.llm
        )
        return product
