"""pydantic models for the substance class."""

from typing import List, Literal, Optional

from bigtree import nested_dict_to_tree  # type: ignore
from pydantic import BaseModel, Field


class Substance(BaseModel):
    """A substance in a reaction."""

    reference_key: Optional[str] = Field(
        description=(
            "Identifier for a substance described in text. "
            "It can be a number or combination of numbers and letters."
        ),
    )
    substance_name: str = Field(
        description="Name of the substance.",
    )
    role: Literal[
        "reactant", "work-up", "solvent", "product", "intermediate"
    ] = Field(
        description=(
            "What is the role of the substance in the reaction. "
            "'work-up' is reserved for substances used in subsequent "
            "steps of the reaction, such as washing, quenching, etc."
        )
    )

    @classmethod
    def from_lm(cls, s):
        """Reconvert into Substance. Fill reference_key if missing."""
        if s.reference_key is None:
            s.reference_key = s.substance_name
        return cls(**s.model_dump())

    def to_node(
        self, name_key: str = "reference_key", child_key: str = "children"
    ):
        """Convert object to node."""
        return nested_dict_to_tree(
            self.model_dump(),  # type: ignore
            name_key=name_key,
            child_key=child_key,
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
