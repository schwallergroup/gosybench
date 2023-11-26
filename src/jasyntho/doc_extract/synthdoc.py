"""Defines the SynthDocument class, which creates a collection of SynthParagraphs."""

import asyncio
import json
import os
import re
from itertools import chain
from typing import Dict, List, Optional, Union

import fitz
from dotenv import load_dotenv

from jasyntho.extract import Extractor

from .synthpar import SynthParagraph

load_dotenv()


class SynthDocument:
    """Synthesis doc composed of multiple synth paragraphs.

    Initialize from pdf files.
    """

    def __init__(self, doc_src: str, api_key: Optional[str] = None) -> None:
        """
        Initialize a synthesis document.

        Input
        ______
        doc_src: Union[str, list]
            if str: path to the pdf file
            if list: list of extracted entities->out of extract.Extractor
        """
        self.rxn_setup = None

        api_key = api_key or os.environ["OPENAI_API_KEY"]
        self.rs_extractor = Extractor("rxn_setup", api_key)
        self.paragraphs = self._build_doc(doc_src)

    def extract_rss(self) -> None:
        """Extract reaction setups for each paragraph in the doc."""
        rxn_setups = [p.extract(self.rs_extractor) for p in self.paragraphs]

        self.rxn_setups = []
        for p in rxn_setups:
            if p.reference_key is not None or p.reference_key != "":
                self.rxn_setups.append(p.model_dump())

    async def async_extract_rss(self) -> None:
        """Extract reaction setups for each paragraph in the doc."""
        rxn_setups = await asyncio.gather(
            *[p.async_extract(self.rs_extractor) for p in self.paragraphs]
        )

        self.rxn_setups = []
        for p in rxn_setups:
            if p.reference_key is not None or p.reference_key != "":
                self.rxn_setups.append(p.model_dump())


    def _build_doc(
        self, doc_src: str, start: int = 0, end: Optional[int] = None
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
        doc = fitz.open(doc_src)
        self.doc = doc

        if end is None:
            end = int(doc.page_count)
        else:
            end = int(end)

        if start < 0:
            raise ValueError("start must be >= 0")
        elif start >= doc.page_count:
            raise ValueError("start must be < the doc page count")
        elif start > end:
            raise ValueError("start must be < end")

        if end > int(doc.page_count):
            end = doc.page_count

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
                                not re.search(r"S\d+", text)
                                or (re.search(r"S\d+", text) and ("Bold" in font or "bold" in font))
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
