"""Base classes for document extraction."""

import json
import os
import re
from typing import Any, List, Optional, Tuple

import fitz
from pydantic import BaseModel


class ResearchDoc(BaseModel):
    """A research paper and its SI."""

    doc_src: str
    fitz_paper: fitz.Document
    fitz_si: fitz.Document
    paper: str = ""
    si: str = ""
    si_dict: dict = {}
    logger: Any = None

    class Config:
        """Pydantic config."""

        arbitrary_types_allowed = True

    @classmethod
    def from_dir(cls, paper_dir: str, logger: Any = None):
        """
        Initialize ResearchDoc object.

        paper_dir: directory containing the paper and SI.
            SI must be named si_0.pdf,
            paper must be named paper.pdf.
        """
        paper_path = os.path.join(paper_dir, "paper.pdf")
        paper_fitz, paper_text = ResearchDoc.load(paper_path)
        si_fitz, si_text = ResearchDoc.load_si(paper_dir)
        return cls(
            doc_src=paper_dir,
            fitz_paper=paper_fitz,
            fitz_si=si_fitz,
            paper=paper_text,
            si=si_text,
            logger=logger,
        )

    @classmethod
    def load(cls, path: str) -> Tuple[fitz.Document, str]:
        """Load a PDF as a string."""
        doc = fitz.open(path)
        text = ""
        for p in doc:
            text += p.get_text()
        return doc, text

    @classmethod
    def load_si(cls, path: str) -> Tuple[fitz.Document, str]:
        """Load an SI from a directory, potentially multiple files."""
        doc = fitz.open()
        text = ""

        si_paths = [os.path.join(path, f) for f in os.listdir(path)]
        for si in si_paths:
            if re.match(r".*si_\d+\.pdf", si):
                doc.insert_file(si)

        for p in doc:
            text += p.get_text()

        return doc, text

    def acquire_context(
        self,
        query: str,
        doc: Optional[str] = None,
        n: int = 5,
        max_len: int = 200,
    ) -> List[str]:
        """Find any references to some query in the document."""
        if doc is None:
            doc = self.paper

        lbreak = self._find_most_frequent_linebreaker(doc)
        chunks = re.split(lbreak, doc)
        clist = [c for c in chunks if query in c]
        return clist

    def _find_most_frequent_linebreaker(self, text):
        """Find the most frequent line breaker pattern in the text."""
        patterns = [
            r"\.\s?\n",
            r"\n\s?\.",
            r"\n\n+",
            r"\n\s+\n",
        ]

        # Initialize a dictionary to store the counts of each line breaker
        linebreaker_counts = {pattern: 0 for pattern in patterns}

        # Count the occurrences of each line breaker pattern in the text
        for pattern in patterns:
            linebreaker_counts[pattern] = len(re.findall(pattern, text))

        # Return the most frequent line breaker pattern
        most_frequent_linebreaker = max(
            linebreaker_counts, key=linebreaker_counts.get
        )
        return most_frequent_linebreaker
