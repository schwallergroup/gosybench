"""Data extractors for segments of chemical synthesis paragraphs."""

from typing import Any, Optional
from .rxns_si.extract import ReactionSetup


class Extractor:
    """Extract data from snippets of synthesis paragraphs.

    Initializes extractor depending on the snippet class.
    """

    def __init__(
        self,
        sclass: str,
        api_key: Optional[str] = None,
        model: str = "gpt-4-0314",
    ) -> None:
        """Initialize extractor.

        Input
        sclass : str
            Snippet class.
            One of 'rxn_setup', 'rxn_workup', 'purification', 'analysis'
        """
        self.extractor = self._init_extractor(sclass, api_key, model)

    def __call__(self, text: str) -> Any:
        """Execute the extractor."""
        return self.extractor(text)

    async def async_call(self, text: str) -> Any:
        """Execute extractor."""
        return await self.extractor.async_call(text)

    def _init_extractor(
        self,
        eclass: str,
        api_key: Optional[str] = None,
        model: str = "gpt-4-0314",
    ):
        """
        Initialize a data extractor.

        Input
        eclass : str
            Type of extractor to initialize.
        """
        if eclass == "rxn_setup":
            return ReactionSetup(api_key=api_key, model=model)
        elif eclass == "rxn_workup":
            raise NotImplementedError()
        elif eclass == "purification":
            raise NotImplementedError()
        elif eclass == "analysis":
            raise NotImplementedError()
        return None
