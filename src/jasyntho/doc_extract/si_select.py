"""
Select the relevant part of the SI.

That is, the part containing the synthesis procedures.
"""

import re
import os
import fitz  # type: ignore
from pydantic import BaseModel
import numpy as np
from scipy.signal import find_peaks


class ResearchDoc(BaseModel):
    """A research paper and its SI."""

    #fitz_paper: fitz.fitz.Document
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
        #fitz_paper, paper = ResearchDoc.load(paper_path)
        fitz_si, si = ResearchDoc.load(si_path)
        return cls(
            #fitz_paper=fitz_paper,
            fitz_si=fitz_si,
            #paper=paper,
            si=si
            )

    @classmethod
    def load(cls, path: str) -> str:
        """Load a PDF as a string."""
        doc = fitz.open(path)
        text = ""
        for p in doc:
            text += p.get_text()
        return doc, text

        
    #def acquire_context(
    #    self, query_substance: str, n: int = 5, max_len: int = 200
    #):
    #    """Find references to query substance in paper."""
    #    doc = self.paper
    #    context = ""
    #    for i, m in enumerate(re.finditer(query_substance, doc)):
    #        segm = doc[m.start() - max_len : m.start() + max_len].replace(
    #            "\n", " "
    #        )
    #        context += f"Segment {i+1}: '{segm}'\n" "Source: main paper\n\n"
    #        if i == n:
    #            break
    #    return context

class SISplitter(BaseModel):
    """Identify relevant part of the SI."""

    plot: bool = False
    window_size: int = 20
    signal_threshold: int = 200
    text_regex: str = r'[A-Z][a-z]'
    special_regex: str = r'[a-zA-Z!@#$%^&*()\-_=+{}[\];:,.<>?/|~`]'

    sdict: dict = {}
    sents: list = []
    pages: tuple = (0, 0)

    def select_relevant(self, doc: ResearchDoc):
        """Select the relevant part of the SI."""
        self.pages = self.find_pages(doc)
        return self.cut_si(doc)

    def find_pages(self, doc: ResearchDoc):
        """Find page number range, where SI contains procedures."""
        ratios = self.map_ratio(doc)
        ranges = self.find_longest_true(ratios > self.signal_threshold)
        p0 = self.sdict.get(ranges[0]+self.window_size, False)
        p1 = self.sdict.get(ranges[1]+self.window_size, False)
        if not p1:
            p1 = self.sdict.get(ranges[1], False)

        if self.plot:
            self.plot_signal(ratios, ranges)

        if p0 and p1:
            print(f'Selected: {p0, p1}')
            return p0, p1
        else:
            raise ValueError(f'Could not find relevant part of SI in {self.pages}.')

    def plot_signal(self, ratios, ranges):
        """Plot the signal and the selected range."""
        import matplotlib.pyplot as plt
        plt.plot(ratios)
        plt.axvline(ranges[0], color='r')
        plt.axvline(ranges[1], color='k')
        plt.show()

    def cut_si(self, doc: ResearchDoc):
        """Slice the SI to the relevant part."""
        p0, p1 = self.pages
        if p0 > p1:
            raise ValueError(f'Invalid page range {self.pages}.')
        else:
            doc.fitz_si.delete_pages(from_page=p1+1, to_page=len(doc.fitz_si)-1)
            if p0 != 0:
                doc.fitz_si.delete_pages(from_page=0, to_page=p0-1)
        return doc.fitz_si

    def map_ratio(self, doc: ResearchDoc):
        """Split the SI into sentences and calculate the ratio.
        Returns ratio: page for each sentence."""
        self.sentence_dict(doc.fitz_si)
        ratios = [self._ratio_si(s) for s in self.sents]
        ratios = self._smooth_signal(ratios)
        return ratios

    def sentence_dict(self, doc: ResearchDoc, split_pattern='\n'):
        """Create list of sentences and a dictionary mapping sentence idx to page."""
        self.sdict = {}
        self.sents = []
        for p in doc:
            p_number = p.number
            sents = p.get_text().split(split_pattern)
            idict = {i+len(self.sdict): p_number for i, s in enumerate(sents)}
            self.sdict.update(idict)
            self.sents += sents
        return self.sdict

    def _ratio_si(self, sentence):
        """Calculate the ratio of special characters to text."""
        text = len(re.findall(self.text_regex, sentence))
        spec = len(re.findall(self.special_regex, sentence))
        return spec/(text+1)

    def _smooth_signal(self, ratios):
        """Smooth the signal using a moving average."""
        conv = np.convolve(ratios, np.ones(self.window_size), 'valid')    
        conv = conv/np.mean(np.sort(conv)[-30:])  # normalize
        return conv

    def find_longest_true(self, bools):
        """Find the longest sequence of True values."""
        max_len = 0
        max_start = 0
        max_end = 0
        start = 0
        for i, b in enumerate(bools):
            if b:
                if start == 0:
                    start = i
            else:
                if start != 0:
                    if i - start > max_len:
                        max_len = i - start
                        max_start = start
                        max_end = i
                    start = 0
        return max_start, max_end

