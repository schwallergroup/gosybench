"""LLMs for segmentation with fine-tuned Flan-T5 models (base, large)."""

import os
from typing import List, Optional, Union

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

from .base import Segmentor


class SegFlanT5(Segmentor):
    """Segmentator with Flan-T5. Allows batch inference."""

    def __init__(self):
        """Segmentor class with Flan-T5 fine-tuned models.
        Input
        _____
        model: str
            one of `base` or `large`
        """

        # TODO download model if not there
        self.model = AutoModelForSeq2SeqLM.from_pretrained(
            "google/flan-t5-large", map_device="auto"
        )
        self.tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-large")
        self.device = "cuda:0"

    def _run(self, inputs: Union[List, str]) -> Union[List, str]:
        """
        Segment a synthetic paragraph or list of them.
        Input
        _____
        inputs: Optional[List, str]
            synthetic paragraph to segment
        """
        if isinstance(inputs, str):
            inputs = [inputs]

        inputs = self.tokenizer(inputs, return_tensors="pt", padding=True).to(self.device)

        raw_outputs = self.model.generate(**inputs, min_new_tokens=512)
        outputs = self.tokenizer.batch_decode(raw_outputs, skip_special_tokens=True)

        return outputs
