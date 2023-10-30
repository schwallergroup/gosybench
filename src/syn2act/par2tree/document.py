"""PDF Parsing utilities."""

import json
import os
import re
from itertools import chain
from typing import Dict, List, Optional

import fitz
from dotenv import load_dotenv
from fitz.fitz import Document

from syn2act.extract import Extractor

load_dotenv()


class SynthParagraph:
    """
    Synthesis paragraph. Contains details about preparation of a substance.
    TODO: Include all extraction capabilities here.
    """

    def __init__(self, text: str) -> None:
        """
        Input
        _____
        text: str
            paragraph text describing the synthesis.
        """
        self.text = text
        self.data: Dict[str, List[dict]] = dict()

    def __repr__(self) -> str:
        """Print the text"""

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
        ______
        extractor: Extractor
            Initialized data extractor.

        Stores extractor output internally, and returns the output.
        """

        self.data["rxn_setup"] = self._flatten_list(extractor(self.text))
        return self.data["rxn_setup"]

    def _flatten_list(self, lst: list):
        """
        Flattens a list that may contain nested lists into a single flat list.

        Parameters:
            lst (list): A list that may contain nested lists.

        Returns:
            clean_list (list): A flattened list with no nested lists.
        """

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

        if isinstance(lst, list):
            remove_nestings(lst)
        else:
            return [lst]

        return clean_list


