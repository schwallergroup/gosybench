"""pydantic models for the product class."""

from typing import List, Literal, Optional

import instructor  # type: ignore
import openai
from colorama import Fore  # type: ignore
from pydantic import ValidationError

from .llm_config import config
from .substance import SubstanceInReaction, SubstanceInReactionList


class Product(SubstanceInReaction):
    """Substance with children and properites.

    Args:
        reference_key: Identifier for a substance described in text.
        substance_name: Name of the substance.
        children: List of substances that are children of this substance.
        props: Dictionary of properties of this substance.
    """

    role_in_reaction: str = "main product"  # type: ignore
    children: List[SubstanceInReaction]
    origin: str = "SI"
    edge_type: Literal[
        "lab reaction", "failed reaction", "model system", "other"
    ] = "lab reaction"
    text: Optional[str] = None
    chain_of_thought: str
    note: Optional[str] = None

    @classmethod
    def from_substancelist(cls, slist: SubstanceInReactionList):
        """Convert from SubstanceInReactionList."""
        s_list = [SubstanceInReaction.from_lm(s) for s in slist.substances]

        # 1. Identify the product
        prods_list = [
            s for s in s_list if s.role_in_reaction == "main product"
        ]
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
        child_list = [
            s for s in s_list if s.role_in_reaction != "main product"
        ]
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
                if any([s.role_in_reaction == "reactant" for s in same_key]):
                    for s in same_key:
                        if s.role_in_reaction != "reactant":
                            clean_ch.remove(s)
                else:
                    for s in same_key[1:]:  # remove all but first
                        clean_ch.remove(s)

        child_final = [SubstanceInReaction.from_lm(s) for s in clean_ch]

        return cls(
            reference_key=pkey,
            substance_name=pname,
            children=child_final,
            chain_of_thought=slist.chain_of_thought,
        )

    @classmethod
    def from_paragraph(cls, prgr: str, client: instructor.patch, llm: str):
        """Extract the substances in a reaction."""
        try:
            subs_list = client.chat.completions.create(
                model=llm,
                response_model=SubstanceInReactionList,
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
                response_model=SubstanceInReactionList,
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
            chain_of_thought="",
        )

    def isempty(self):
        """Tell if object is empty."""
        if self.reference_key is None:
            return True
        return False
