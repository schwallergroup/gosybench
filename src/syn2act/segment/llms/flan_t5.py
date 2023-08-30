"""LLMs for segmentation with fine-tuned Flan-T5 models (base, large).
TODO
"""

import os
from typing import Optional, List
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

from ..segment import Segmentor


class SegFlanT5(Segmentor):
    def __init__(self):
        # TODO download model if not there
        self.model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-large")
        self.tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-large")
        self.device = 'cuda:0'

    def run(self, inputs: Optional[List, str]) -> Optional[List, str]:
        """
        Segment a synthetic paragraph or list of them.
        Input
        _____
        inputs: Optional[List, str]
            synthetic paragraph to segment
        """

        inputs = tokenizer(
            inputs,
            return_tensors="pt",
            padding=True
        ).to(self.device)

        raw_outputs = self.model.generate(**inputs, min_new_tokens = 512)
        outputs = self.tokenizer.batch_decode(raw_outputs, skip_special_tokens=True)


def flant5_segment():
    """
    Initialize GPT-3.5 for segmentation.

    Input
    _____
    """
    a = 0
    return None
