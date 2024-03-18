"""Classes to extract substances from a text."""

from typing import List

import instructor
from openai import OpenAI
from pydantic import BaseModel, Field


class Substance(BaseModel):
    """Substance base class."""

    reference_key: str = Field(
        description=(
            "Identifier for a substance described in text. "
            "combination of letters and numbers, like "
            "'S1', '14', '22a', or more complex like 'C8-epi-20' etc."
        )
    )


class ExSubstances(BaseModel):
    """Extract substances from a text."""

    chain_of_thought: str = Field(
        description="Think step by step to extract the requested information.",
    )
    substances: List[Substance] = Field(
        description="A list of all the substances mentioned in the input text.",
        default_factory=list,
    )

    @classmethod
    def from_context(cls, context: str):
        """Extract the substances in a reaction."""
        client = instructor.patch(OpenAI())
        slist = client.chat.completions.create(
            model="gpt-3.5-turbo",
            response_model=cls,
            messages=[
                {"role": "user", "content": context},
            ],
        )
        return slist
