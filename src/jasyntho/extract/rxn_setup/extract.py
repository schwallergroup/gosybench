"""Data extraction from reaction setup text segments."""

from typing import Union
import instructor  # type: ignore
from dotenv import load_dotenv
from openai import OpenAI, AsyncOpenAI  # type: ignore
from pydantic import ValidationError

from .typing import Product

load_dotenv()


class ReactionSetup:
    """Extraction of structured data from reaction-setup snippet."""

    def __init__(self, api_key=None):
        """Initialize LLMChain for data extraction with GPT-4."""
        load_dotenv()

        self.llm = 'gpt-4-1106-preview'
        # self.llm = 'gpt-3.5-turbo'
        self.client = instructor.patch(OpenAI())
        self.aclient = instructor.apatch(AsyncOpenAI())

    def __call__(self, text: str) -> Union[dict, list]:
        """Execute the extraction pipeline for a single paragraph."""
        try:
            product = Product.from_paragraph(text, self.client, self.llm)
            return product
        except ValidationError:
            return Product.empty()

    async def async_call(self, text: str) -> Union[dict, list]:
        """Execute the extraction pipeline for a paragraph asynchronously."""
        try:
            product = Product.async_from_paragraph(
                text, self.aclient, self.llm
            )
            return await product
        except ValidationError:
            return Product.empty()
