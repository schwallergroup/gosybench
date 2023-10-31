"""Data extractors for segments of chemical synthesis paragraphs."""

from typing import List, Optional

from langchain.chains import LLMChain

from .rxn_setup.extract import ReactionSetup


class Extractor:
    """
    Extract data from snippets of synthesis paragraphs in a standardized format.
    Initializes extractor depending on the snippet class.
    """

    def __init__(self, sclass: str, api_key: Optional[str] = None) -> None:
        """
        Input
        _____
        sclass : str
            Snippet class.
            One of 'rxn_setup', 'rxn_workup', 'purification', 'analysis'
        """
        self.extractor = self._init_extractor(sclass, api_key)

    def __call__(self, snippet: str) -> List[dict]:
        """Execute the extractor."""

        out = self.extractor(snippet)
        return out

    def _init_extractor(self, sclass: str, api_key: Optional[str] = None) -> LLMChain:
        """
        Initialize a chain for data extraction.
        Input
        _____
        sclass : str
            Segment type to extract data from.
        """
        if api_key is None:
            pass
        else:
            if sclass == "rxn_setup":
                return ReactionSetup()
            elif sclass == "rxn_workup":
                raise NotImplementedError()
            elif sclass == "purification":
                raise NotImplementedError()
            elif sclass == "analysis":
                raise NotImplementedError()
        return None
