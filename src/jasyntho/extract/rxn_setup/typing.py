"""pydantic models for the substance classes."""

import instructor
from typing import List, Literal, Optional, Dict, Union
from pydantic import BaseModel, Field


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

    role: str = 'product'  # type: ignore
    children: List[Substance]
    props: Optional[Dict[str, str]] = None

    @classmethod
    def from_substancelist(cls, slist: SubstanceList):
        """Convert from SubstanceList."""
        child = {}
        pkey = ''
        pname = ''
        for s in slist.substances:
            if s.role == 'product':
                pname = s.substance_name
                pkey = s.reference_key
                if pkey is None:
                    pkey = pname
            else:
                # TODO: handle multiple children
                child[s.reference_key] = Substance.from_lm(s)
        return cls(
            reference_key=pkey,
            substance_name=pname,
            children=list(child.values())
        )

    @classmethod
    def from_paragraph(
            cls,
            prgr: str,
            client: instructor.patch,
            llm: str
    ):
        """Extract the substances in a reaction."""
        prgr = prgr[:700]

        try:
            subs_list = client.chat.completions.create(
                model=llm,
                response_model=SubstanceList,
                messages=[
                    {"role": "user", "content": prgr},
                ],
                temperature=0.2,
                max_retries=2,
                timeout=60,
            )
            return cls.from_substancelist(subs_list)
        except:
            return cls()


    @classmethod
    async def async_from_paragraph(
            cls,
            prgr: str,
            aclient: instructor.apatch,
            llm: str
    ):
        """Extract the substances in a reaction."""
        prgr = prgr[:700]

        # try:
        subs_list = await aclient.chat.completions.create(
            model=llm,
            response_model=SubstanceList,
            messages=[
                {"role": "user", "content": prgr},
            ],
            temperature=0.2,
            max_retries=2,
            timeout=60,
        )
        return cls.from_substancelist(subs_list)
        #except:
        #    return cls()
