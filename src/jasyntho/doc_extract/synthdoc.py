"""
SynthDocument class.

Creates a collection of SynthParagraphs from a paper.
"""

import asyncio
import json
import os
import re
from itertools import chain
from typing import List, Optional

import fitz  # type: ignore
from colorama import Fore  # type: ignore
from dotenv import load_dotenv

from pydantic import BaseModel
from jasyntho.extract import Extractor

from .synthpar import SynthParagraph
from .si_select import SISplitter


class ResearchDoc(BaseModel):
    """A research paper and its SI."""

    doc_src: str
    fitz_paper: fitz.fitz.Document
    fitz_si: fitz.fitz.Document
    paper: str = ""
    si: str = ""
    si_dict: dict = {}

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def from_dir(cls, paper_dir: str):
        """
        Initialize ResearchDoc object.

        paper_dir: directory containing the paper and SI.
            SI must be named si_0.pdf,
            paper must be named paper.pdf.
        """
        paper_path = os.path.join(paper_dir, "paper.pdf")
        si_path = os.path.join(paper_dir, "si_0.pdf")
        paper_fitz, paper_text = ResearchDoc.load(paper_path)
        si_fitz, si_text = ResearchDoc.load(si_path)
        return cls(
            doc_src=paper_dir,
            fitz_paper=paper_fitz,
            fitz_si=si_fitz,
            paper=paper_text,
            si=si_text
        )

    @classmethod
    def load(cls, path: str) -> str:
        """Load a PDF as a string."""
        doc = fitz.open(path)
        text = ""
        for p in doc:
            text += p.get_text()
        return doc, text


class SISynthesis(ResearchDoc):
    """Synthesis document."""

    rxn_extract: Optional[Extractor] = None
    paragraphs: List[SynthParagraph] = []
    v: bool = True

    def select_syntheses(self) -> None:
        """Select the part of the SI where syntheses are described."""
        si_split = SISplitter()

        si_split.signal_threshold = 0.35
        si_split.window_size = 150
        if verbose:
            si_split.plot = True

        doc = self.from_dir(self.doc_src)
        relevant_si = si_split.select_relevant(doc)
        relev_si_src = os.path.join(self.doc_src, "si_syntheses.pdf")
        relevant_si.save(relev_si_src)

    def extract_rss(self) -> list:
        """Extract reaction setups for each paragraph in the doc."""
        relev_si_src = os.path.join(self.doc_src, "si_syntheses.pdf")
        self.paragraphs = self._get_paragraphs(relev_si_src)

        self.raw_prodlist = [
            p.extract(self.rxn_extract) for p in self.paragraphs
        ]
        self.raw_prods = list(chain(*self.raw_prodlist))  # type: ignore
        self._report_process(self.raw_prods)
        products = [p for p in self.raw_prods if not p.isempty()]
        return products

    async def async_extract_rss(self) -> list:
        """Extract reaction setups for each paragraph in the doc."""
        relev_si_src = os.path.join(self.doc_src, "si_syntheses.pdf")
        self.paragraphs = self._get_paragraphs(relev_si_src)

        self.raw_prodlist = await asyncio.gather(
            *[p.async_extract(self.rxn_extract) for p in self.paragraphs]
        )
        self.raw_prods = list(chain(*self.raw_prodlist))  # type: ignore
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
        self,
        doc_src: str
    ) -> List[SynthParagraph]:
        """
        Create list of paragraphs from document.

        Input
            doc_src: address of the pdf document.
        """
        end = self.fitz_si.page_count

        parags_pages = self._get_pars_per_page(0, end)
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
            json_data = self.fitz_si[i].get_text("json")
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
