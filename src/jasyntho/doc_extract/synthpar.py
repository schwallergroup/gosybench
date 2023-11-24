"""
Defines the SynthParagraph class.

Extract and contain all data from a synthesis paragraph.
"""

from typing import Dict, List, Optional


class SynthParagraph:
    """
    Synthesis paragraph.

    Contains details about preparation of a (set of) substances.
    TODO: Include all extraction capabilities here
          (extend to work-up, purification, analysis).
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

    def extract(self, extractor) -> List[dict]:
        """Extract information from this paragraph in a standard format.

        Input
        extractor: Extractor
            Initialized data extractor.

        Output:
        extracted_data: List[dict]
            Extracted list of products with preparation metadata.
        """

        raw_output = extractor(self.text)
        return raw_output

        self.data["rxn_setup"] = self._flatten_list(raw_output)

        return self.data["rxn_setup"]

    async def async_extract(self, extractor) -> List[dict]:
        """Extract information from this paragraph in a standard format.

        Input
        extractor: Extractor
            Initialized data extractor.

        Output:
        extracted_data: List[dict]
            Extracted list of products with preparation metadata.
        """

        raw_output = await extractor.async_call(self.text)
        self.data["rxn_setup"] = self._flatten_list(raw_output.model_dump())

        return self.data["rxn_setup"]

    def _flatten_list(self, in_list: list) -> Optional[list]:
        """
        Flattens a list that may contain nested lists into a single flat list.

        Input:
        in_list: list
            A list that may contain nested lists.

        Output:
        cl_list: list
            A flattened list with no nested lists.
        AB: This seems to be needed as the output of LLM
        is not always a flat list.
        """

        if in_list['reference_key'] is None:
            return None

        clean_list = []

        def remove_nestings(lst):
            """
            Recursively check if there are lists and extract their elements
            """
            for elem in lst:
                if type(elem) is list:
                    remove_nestings(elem)
                else:
                    clean_list.append(elem)

        if isinstance(in_list, list):
            remove_nestings(in_list)
        else:
            return [in_list]

        return clean_list
