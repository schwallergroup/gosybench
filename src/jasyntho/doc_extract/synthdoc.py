"""
SynthDocument class.

Creates a collection of SynthParagraphs from a paper.
"""

import asyncio
import json
import os
import re
from typing import List, Optional

import fitz  # type: ignore
from colorama import Fore  # type: ignore
from dotenv import load_dotenv

from jasyntho.extract import Extractor

from .synthpar import SynthParagraph


class SynthDocument:
    """Synthesis document."""

    def __init__(
        self,
        doc_src: str,
        api_key: Optional[str] = None,
        model: str = "gpt-4-0314",
        startp: int = 0,
        endp: Optional[int] = None,
        verbose: bool = True,
    ) -> None:
        """
        Initialize a synthesis document.

        Input
        doc_src: Optional[str]
            path to the pdf file
        """
        load_dotenv()
        api_key = api_key or os.environ["OPENAI_API_KEY"]

        self.v = verbose
        self.rxn_extract = Extractor("rxn_setup", api_key, model=model)
        self.paragraphs = self._get_paragraphs(doc_src, start=startp, end=endp)

    def extract_rss(self) -> list:
        """Extract reaction setups for each paragraph in the doc."""
        self.raw_prods = [p.extract(self.rxn_extract) for p in self.paragraphs]
        self._report_process(self.raw_prods)
        products = [p for p in self.raw_prods if not p.isempty()]
        return products

    async def async_extract_rss(self) -> list:
        """Extract reaction setups for each paragraph in the doc."""
        self.raw_prods = await asyncio.gather(
            *[p.async_extract(self.rxn_extract) for p in self.paragraphs]
        )
        self._report_process(self.raw_prods)
        products = [p for p in self.raw_prods if not p.isempty()]
        return products

    def _report_process(self, raw_prods) -> None:
        """Print a report of results of prgr processing."""
        if not self.v:
            return None

        correct = 0
        empty = 0
        notes = []
        for p in raw_prods:
            if p.isempty():
                empty += 1
                notes.append(p.note)
            else:
                correct += 1

        def printm(message):
            """Print report message."""
            print(Fore.LIGHTYELLOW_EX + message + Fore.RESET)

        printm(f"Total paragraphs: {len(self.paragraphs)}")
        printm(f"Processed paragraphs: {correct}")
        printm(f"Found {empty} empty paragraphs.")
        for n in set(notes):
            printm(f"\t{n}: {notes.count(n)}")

    def _get_paragraphs(
        self, doc_src: str, start: int = 0, end: Optional[int] = None
    ) -> List[SynthParagraph]:
        """
        Create list of paragraphs from document.

        Input
            doc_src: address of the pdf document.
            start: Page to read paragraphs from.
            end: Last page to read paragraphs from.
        """
        self.doc = fitz.open(doc_src)
        end = end or self.doc.page_count

        if start < 0 or start >= self.doc.page_count:
            raise ValueError("start must be >= 0 and < the doc page count")

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
        """Get all paragraphs in this page.

        This is one of these functions you simply don't touch.
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
                                or (
                                    re.search(r"S\d+", text)
                                    and ("Bold" in font or "bold" in font)
                                )
                                or re.search("[T|t]able", text)
                                or re.search("[F|f]igure", text)
                            ):
                                if flags & 2**0:
                                    text = " " + text

                                if k == (len(text_boxes) - 1) and j == (
                                    len(page_blocks) - 1
                                ):
                                    new_paragraph += text
                                    if start_bold:
                                        page_paragraphs.append(
                                            ["bold", new_paragraph]
                                        )
                                    else:
                                        page_paragraphs.append(
                                            ["plain", new_paragraph]
                                        )
                                    new_paragraph = ""
                                else:
                                    if "Bold" in font or "bold" in font:
                                        bold_txt += text
                                    else:
                                        if len(bold_txt) > 5:
                                            if start_bold:
                                                page_paragraphs.append(
                                                    ["bold", new_paragraph]
                                                )
                                            else:
                                                page_paragraphs.append(
                                                    ["plain", new_paragraph]
                                                )

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
