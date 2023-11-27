"""pydantic models for the substance classes."""

from typing import List, Literal, Optional

import instructor  # type: ignore
import openai
from colorama import Fore  # type: ignore
from pydantic import BaseModel, Field, ValidationError


class LLMConfig(BaseModel):
    """Pydantic model configuration."""

    temperature: float = 0.2
    timeout: int = 120
    max_retries: int = 2


config = LLMConfig()


class Substance(BaseModel):
    """A substance in a reaction."""

    reference_key: Optional[str] = Field(
        description=("Identifier for a substance described in text. "),
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

    @classmethod
    def from_lm(cls, s):
        """Reconvert into Substance. Fill reference_key if missing."""
        if s.reference_key is None:
            s.reference_key = s.substance_name
        return cls(**s.model_dump())


class SubstanceList(BaseModel):
    """List of substances in a reaction.

    Instructions: `reference_key` is the reference number given to the
    substance. `reference_key` is a combination of letters and numbers, like
    'S1', '14', '22a', or more complex like 'C8-epi-20' etc.
    Some might have longer specifiers, like C8-epi-20.
    Example: If "alkene 17a" is mentioned, then `reference_key`=="17a".
    """

    substances: List[Substance] = Field(..., default_factory=list)


class Product(Substance):
    """Substance with children and properites.

    Args:
        reference_key: Identifier for a substance described in text.
        substance_name: Name of the substance.
        children: List of substances that are children of this substance.
        props: Dictionary of properties of this substance.
    """

    role: str = "product"  # type: ignore
    children: List[Substance]
    text: Optional[str] = None
    note: Optional[str] = None

    @classmethod
    def from_substancelist(cls, slist: SubstanceList):
        """Convert from SubstanceList."""
        s_list = [Substance.from_lm(s) for s in slist.substances]

        # 1. Identify the product
        prods_list = [s for s in s_list if s.role == "product"]
        nprod = len(prods_list)
        if nprod == 0:
            return cls.empty(note="No product found")
        elif nprod > 1:
            print(Fore.RED, "More than one product in reaction. TODO")
            return cls.empty(note="More than one product found")
        else:
            pkey = prods_list[0].reference_key
            pname = prods_list[0].substance_name

        # 2. Identify the children
        # Identify which reactants have same name as product
        child_list = [s for s in s_list if s.role != "product"]
        clean_ch = [s for s in child_list if s.reference_key != pkey]

        # Identify children that have same reference_key
        keys = [s.reference_key for s in clean_ch]
        # Count the occurence of each unique value in keys
        counts = {k: keys.count(k) for k in set(keys)}

        multiple_keys = [k for k, v in counts.items() if v > 1]
        if len(multiple_keys) > 0:
            for k in multiple_keys:
                print(f"Found key '{k}' in multiple children.")
                # Find the substances with this key
                same_key = [s for s in clean_ch if s.reference_key == k]

                # Remove any that isn't a reactant
                if any([s.role == "reactant" for s in same_key]):
                    for s in same_key:
                        if s.role != "reactant":
                            clean_ch.remove(s)
        child_final = [Substance.from_lm(s) for s in clean_ch]

        return cls(
            reference_key=pkey, substance_name=pname, children=child_final
        )

    @classmethod
    def from_paragraph(cls, prgr: str, client: instructor.patch, llm: str):
        """Extract the substances in a reaction."""
        try:
            subs_list = client.chat.completions.create(
                model=llm,
                response_model=SubstanceList,
                messages=[
                    {"role": "user", "content": prgr},
                ],
                temperature=config.temperature,
                max_retries=config.max_retries,
                timeout=config.timeout,
            )
            prd = cls.from_substancelist(subs_list)
        except (openai.APITimeoutError, ValidationError) as e:  # type: ignore
            if isinstance(e, openai.APITimeoutError):  # type: ignore
                prd = cls.empty(note=e.message)
            else:
                prd = cls.empty(note="Validation error.")

        prd.text = prgr
        return prd

    @classmethod
    async def async_from_paragraph(
        cls, prgr: str, aclient: instructor.apatch, llm: str
    ):
        """Extract the substances in a reaction."""
        try:
            subs_list = await aclient.chat.completions.create(
                model=llm,
                response_model=SubstanceList,
                messages=[
                    {"role": "user", "content": prgr},
                ],
                temperature=config.temperature,
                max_retries=config.max_retries,
                timeout=config.timeout,
            )
            prd = cls.from_substancelist(subs_list)
        except (openai.APITimeoutError, ValidationError) as e:  # type: ignore
            if isinstance(e, openai.APITimeoutError):  # type: ignore
                prd = cls.empty(note=e.message)
            else:
                prd = cls.empty(note="Validation error.")

        prd.text = prgr
        return prd

    @classmethod
    def empty(cls, note):
        """Return an empty product."""
        return cls(
            reference_key=None,
            substance_name="",
            children=[],
            props=None,
            note=note,
        )

    def isempty(self):
        """Tell if object is empty."""
        if self.reference_key is None:
            return True
        return False
