"""pydantic models for the substance class."""

from typing import List, Literal, Optional

from pydantic import BaseModel, Field


class Substance(BaseModel):
    """Substance base class."""

    reference_key: Optional[str] = Field(
        description=(
            "Identifier for a substance described in text. "
            "combination of letters and numbers, like "
            "'S1', '14', '22a', or more complex like 'C8-epi-20' etc."
        )
    )
    substance_name: str = Field(
        description="Name of the substance.",
    )

    @classmethod
    def from_lm(cls, s):
        """Reconvert into Substance. Fill reference_key if missing."""
        if s.reference_key is None or s.reference_key == "null":
            s.reference_key = s.substance_name
        return cls(**s.model_dump())


class SubstanceInReaction(Substance):
    """A substance in a reaction."""

    role_in_reaction: Literal[
        "reactant",
        "work-up",
        "solvent",
        "main product",
        "by-product",
        "intermediate",
        "catalyst",
        "reagent",
        "other",
    ] = Field(
        description=(
            "What is the role of the substance in the reaction. "
            "'main product' is reserved to only the main, or intended product "
            "of the reaction. This can be one or multiple, and can be "
            "mentioned in the header. Beware of potenitial typos in text. \n"
            "Other non-main products are 'by-product'. "
            "'work-up' is reserved for substances used in subsequent "
            "steps of the reaction, such as washing, quenching, etc."
        )
    )


class SubstanceInReactionList(BaseModel):
    """List of substances in reaction.
    Instructions: reference_key is the reference number given to the
    substance. reference_key is a combination of letters and numbers, like
    'S1', '14', '22a', or more complex like 'C8-epi-20' etc.
    Some might have longer specifiers, like C8-epi-20.
    Example: If "alkene 17a" is mentioned, then reference_key=="17a"."""

    chain_of_thought: str = Field(
        description=(
            "Think step by step about what is the role of each substance mentioned. "
        )
    )
    substances: List[SubstanceInReaction] = Field(..., default_factory=list)
