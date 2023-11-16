"""Typing for the OpenAI API."""

from typing import List, Literal, Optional
from pydantic import BaseModel, Field


class Substance(BaseModel):
    """A substance in a reaction."""

    reference_key: Optional[str] = Field(
        description=("Identifier for a substance described in paragraph. "),
    )
    substance_name: str = Field(
        description="Name of the substance.",
    )
    role: Literal["reactant", "work-up", "solvent", "product"] = Field(
        description=(
            "What is the role of the substance in the reaction. "
            "'work-up' is reserved for substances used in subsequent "
            "steps of the reaction, such as washing, quenching, etc."
        )
    )


class SubstanceList(BaseModel):
    """List of substances in a reaction.

    Instructions: `reference_key` is the reference number given to the
    substance. `reference_key` is a combination of letters and numbers, like
    'S1', '14', '22a', or more complex like 'C8-epi-20' etc.
    Some might have longer specifiers, like C8-epi-20.
    Example: If "alkene 17a" is mentioned, then `reference_key`=="17a".
    """

    substances: List[Substance] = Field(..., default_factory=list)
