"""Contextualized substance in the paper."""

from typing import Literal, Optional

import instructor  # type: ignore
from colorama import Fore  # type: ignore
from pydantic import BaseModel, Field

from .llm_config import config
from .prompts import system_rip, user_rip
from .substance import Substance


class RoleInPaperRaw(BaseModel):
    """Contextualized substance in the paper.

    Pydantic class to be filled by an LLM.
    """

    role_in_paper: Literal["main product", "intermediate", "model system"]
    parent_substance: Optional[Substance] = Field(
        description=(
            "Cases of role_in_paper: \n"
            "If model system, what substance or reaction is this system "
            "supposed to model? \n"
            "If intermediate, what is the target, or the next reaction? "
        )
    )
    chain_of_thought: str = Field(
        description=(
            "Think step by step to find the role of the query substance "
            "in this paper. State each step as a bulletpoint."
        )
    )

    @classmethod
    def from_llm(
        cls,
        client: instructor.patch,
        query_substance: str,
        context: str,
        llm: str,
    ):
        """Get the role of a substance in a paper."""
        rip = client.chat.completions.create(
            model=llm,
            response_model=cls,
            messages=[
                {"role": "system", "content": system_rip.format(context)},
                {"role": "user", "content": user_rip.format(query_substance)},
            ],
            temperature=config.temperature,
            max_retries=config.max_retries,
            timeout=config.timeout,
        )

        return rip


class RoleInPaper(RoleInPaperRaw):
    """Extended version. Include hardcoded reference_key and context."""

    reference_key: str
    context: str

    @classmethod
    def from_llm(
        cls,
        client: instructor.patch,
        query_substance: str,
        context: str,
        llm: str,
    ):
        """Initialize from LLM using context from paper."""
        rip = RoleInPaperRaw.from_llm(
            client,
            query_substance,
            context,
            llm,
        )
        return cls.from_rip(rip, query_substance, context)

    @classmethod
    def from_rip(cls, rip: RoleInPaperRaw, ref_key: str, context: str):
        """Extend the RoleInPaper using ref_key and context."""
        return cls(
            reference_key=ref_key,
            role_in_paper=rip.role_in_paper,
            parent_substance=rip.parent_substance,
            chain_of_thought=rip.chain_of_thought,
            context=context,
        )

    def __str__(self):
        """Prettyprint object."""
        return (
            f"ref_key: {self.reference_key} - {self.role_in_paper}\n"
            f"\t{self.parent_substance}\n"
            f"{Fore.RED}CoT:\n{self.chain_of_thought}\n\n{Fore.RESET}"
        )
