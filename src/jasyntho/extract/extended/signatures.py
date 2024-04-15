"""DSPy Signatures for connection extraction."""

from typing import List

import dspy
from pydantic import BaseModel, Field


class ExperimentalConnection(dspy.Signature):
    """Determine if substance is used to produce another product. If so, find which."""

    context: str = dspy.InputField(desc="Relevant facts about the substance.")
    substance: str = dspy.InputField(desc="The substance to ask about.")

    reaction_description: str = dspy.OutputField(
        desc="Description of the reaction. Describe the substance's role in the reaction, as well as the product."
    )
    is_reactant: bool = dspy.OutputField(
        desc="Is substance explicitly used as a reactant?."
    )
    product: str = dspy.OutputField(
        desc="If is_reactant, what is the product?. Else, None."
    )


class SimpleSubstance(BaseModel):
    """Simple Substance."""

    reference_key: str = Field(
        description=(
            "Identifier for a substance described in text. "
            "combination of letters and numbers, like "
            "'S1', '14', '22a', or more complex like 'C8-epi-20' etc."
        )
    )
    all_names: List[str] = Field(
        description=(
            "Names given to the substance. "
            "The substance can be referred to by different names, sometimes used in combination. "
        ),
        default_factory=list,
    )


class SynthConnection(dspy.Signature):
    """Extract reactants and product from a reaction description."""

    context = dspy.InputField(desc="Short description of a reaction.")
    substance = dspy.InputField(desc="Substance to ask about.")

    reactants: List[SimpleSubstance] = dspy.OutputField(
        desc="Substances used in the reaction as reactants."
    )
    product: SimpleSubstance = dspy.OutputField(
        desc="Substance obtained in the reaction as a product."
    )
