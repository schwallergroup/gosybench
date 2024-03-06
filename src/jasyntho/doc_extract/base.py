"""Base classes for document extraction."""

import json
import os
import re
from typing import Tuple

import fitz
from pydantic import BaseModel


class ResearchDoc(BaseModel):
    """A research paper and its SI."""

    doc_src: str
    fitz_paper: fitz.fitz.Document
    fitz_si: fitz.fitz.Document
    paper: str = ""
    si: str = ""
    si_dict: dict = {}

    class Config:
        """Pydantic config."""

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
            si=si_text,
        )

    @classmethod
    def load(cls, path: str) -> Tuple[fitz.fitz.Document, str]:
        """Load a PDF as a string."""
        doc = fitz.open(path)
        text = ""
        for p in doc:
            text += p.get_text()
        return doc, text
