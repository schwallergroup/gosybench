"""Load and use a research paper from the corpus."""

import re

import fitz  # type: ignore
from pydantic import BaseModel


class Document(BaseModel):
    """A research paper and its SI."""

    paper: str = ""
    si: str = ""

    def acquire_context(
        self, query_substance: str, n: int = 5, max_len: int = 200
    ):
        """Find references to query substance in paper."""
        doc = self.paper
        context = ""
        for i, m in enumerate(re.finditer(query_substance, doc)):
            segm = doc[m.start() - max_len : m.start() + max_len].replace(
                "\n", " "
            )
            context += f"Segment {i+1}: '{segm}'\n" "Source: main paper\n\n"
            if i == n:
                break
        return context

    @classmethod
    def from_dir(cls, paper_dir: str):
        """
        Initialize Document object.

        paper_dir: directory containing the paper and SI.
            SI must be named si_0.pdf,
            paper must be named must be named paper.pdf.
        """
        paper_path = paper_dir + "/paper.pdf"
        si_path = paper_dir + "/si_0.pdf"
        paper = Document.load(paper_path)
        si = Document.load(si_path)
        return cls(paper=paper, si=si)

    @classmethod
    def load(cls, path: str) -> str:
        """Load a PDF as a string."""
        doc = fitz.open(path)
        text = ""
        for p in doc:
            text += p.get_text()
        return text
