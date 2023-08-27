"""PDF Parsing utilities."""

import json
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


class SynthDocument:
    """Synthesis document composed of multiple synthesis paragraph within a given context.
    Initialize from pdf files.
    """

    def __init__(self, doc_src: str) -> None:
        """
        Input
        ______
        doc_src: str
            path to the pdf file
        """

        self.rs_extractor = Extractor(
            "rxn_setup", "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"
        )

        self.doc = fitz.open(doc_src)
        self.paragraphs = self._build_doc(self.doc)[:5]

    def extract_rss(self) -> None:
        """
        Extract the reaction setups for each paragraph in the document.
        """

        for p in self.paragraphs:
            p.extract(self.rs_extractor)
            print(p)

        rxn_setups = [p.data["rxn_setup"] for p in self.paragraphs]
        self.rxn_setups = list(chain(*[p for p in rxn_setups if p[0]]))

    def _build_doc(
        self, doc_pdf: str, start: int = 0, end: Optional[int] = None
    ) -> List[SynthParagraph]:
        """
        Creates a list of paragraphs from the document

        Args:
            doc_src: address of the pdf document.
            start: Page to start obtaining paragraphs from. Defaults to 0.
            end: Last page to obtain paragraphs from. Defaults to 'a', signaling all.

        Returns:
            List of strings corresponding to the paragraphs
        """

        if end is None:
            end = int(self.doc.page_count)
        else:
            end = int(end)

        if start < 0:
            raise ValueError("start must be >= 0")
        elif start >= self.doc.page_count:
            raise ValueError("start must be < the doc page count")
        elif start > end:
            raise ValueError("start must be < end")

        if end > int(self.doc.page_count):
            end = self.doc.page_count

        parags_pages = self._get_pars_per_page(start, end)
        return self._clean_up_pars(parags_pages)

    def _clean_up_pars(self, pars):
        """Merge and filter out paragraphs."""

        all_paragraphs = []
        new_paragraph = ""

        for par in pars:
            if par[0] == "bold":
                if new_paragraph != "" and not new_paragraph.isspace():
                    all_paragraphs.append(SynthParagraph(new_paragraph))
                new_paragraph = ""
            new_paragraph += par[1]

        return all_paragraphs

    def _get_pars_per_page(self, start, end):
        """
        Get all paragraphs in this page.
        """
        all_paragraphs = []

        # iterate over pages of document
        for i in range(start, end):
            # make a dictionary
            json_data = self.doc[i].get_text("json")
            json_page = json.loads(json_data)
            page_blocks = json_page["blocks"]

            page_paragraphs = []
            new_paragraph = ""
            bold_txt = ""
            start_bold = False

            for j in range(len(page_blocks)):
                line = page_blocks[j]

                if "lines" in list(line.keys()):
                    for n in line["lines"]:
                        text_boxes = n["spans"]

                        for k in range(len(text_boxes)):
                            font = text_boxes[k]["font"]
                            text = text_boxes[k]["text"].replace("\n", "")
                            # to check if it is a superscript
                            flags = int(text_boxes[k]["flags"])

                            if (
                                not re.search("S\d+", text)
                                or (re.search("S\d+", text) and ("Bold" in font or "bold" in font))
                                or re.search("[T|t]able", text)
                                or re.search("[F|f]igure", text)
                            ):
                                if flags & 2**0:
                                    text = " " + text

                                if k == (len(text_boxes) - 1) and j == (len(page_blocks) - 1):
                                    new_paragraph += text
                                    if start_bold:
                                        page_paragraphs.append(["bold", new_paragraph])
                                    else:
                                        page_paragraphs.append(["plain", new_paragraph])
                                    new_paragraph = ""
                                else:
                                    if "Bold" in font or "bold" in font:
                                        bold_txt += text
                                    else:
                                        if len(bold_txt) > 5:
                                            if start_bold:
                                                page_paragraphs.append(["bold", new_paragraph])
                                            else:
                                                page_paragraphs.append(["plain", new_paragraph])

                                            start_bold = True
                                            new_paragraph = ""
                                            new_paragraph += bold_txt
                                            bold_txt = ""
                                        else:
                                            new_paragraph += bold_txt
                                            bold_txt = ""

                                        if new_paragraph == "":
                                            start_bold = False

                                        new_paragraph += text

            all_paragraphs.extend(page_paragraphs)

        return all_paragraphs
