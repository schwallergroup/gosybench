"""
Defines the SynthParagraph class.

Extract and contain all data from a synthesis paragraph.
"""

from typing import Dict, List
from jasyntho.extract.rxn_setup.typing import Product


class SynthParagraph:
    """
    Synthesis paragraph.

    Contains details about preparation of a substance.
    """

    def __init__(self, text: str) -> None:
        """
        Initialize a synthesis paragraph.

        Input
        text: str
            paragraph text describing the synthesis.
        """
        self.text = text
        self.data: Dict[str, List[dict]] = dict()

    def __repr__(self) -> str:
        """Print the text."""
        if len(self.data) == 0:
            return self.text
        else:
            s = f"Paragraph text: {self.text}\n\n"
            for k, v in self.data.items():
                s += f"{k}: {v}\n"
            return s

    def extract(self, extractor) -> Product:
        """Extract data from paragraph.

        Input
        extractor: Extractor
            Initialized data extractor.
        """
        raw_output = extractor(self.text)
        return raw_output

    async def async_extract(self, extractor) -> Product:
        """Extract data from paragraph. Asynchronous.

        Input
        extractor: Extractor
            Initialized data extractor.
        """
        raw_output = await extractor.async_call(self.text)
        return raw_output
