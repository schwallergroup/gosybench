"""LLMs for segmentation with fine-tuned Flan-T5 models (base, large)."""

import ast
import os
import pathlib
from typing import List, Optional, Union

import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

from .base import Segmentor


class SegFlanT5(Segmentor):
    """Segmentator with Flan-T5. Allows batch inference."""

    def __init__(self):
        """Segmentor class with Flan-T5 fine-tuned models."""

        adapter = "doncamilom/OChemSegm-flan-T5-large"

        self.model = AutoModelForSeq2SeqLM.from_pretrained(
            "google/flan-t5-large",
        )

        # Load adapter and tokenizer
        self.model.load_adapter(adapter, source="hf", set_active=True)
        self.tokenizer = AutoTokenizer.from_pretrained(adapter)

        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)

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

        raw_outputs = self.model.generate(**inputs, max_length=2048, early_stopping=True)
        outputs = self.tokenizer.batch_decode(raw_outputs, skip_special_tokens=True)

        return outputs

    def _parse_llm_segm(self, llm_output: str) -> List[dict]:
        """
        Parse the output of an LLM for paragraph segmentation into a JSON object.
        For FlanT5 is simply a literal eval of a JSON.

        Input
        _____
            llm_segm: the (string) output of a segmentation LLM.
        Output
        ______
            JSON object with ['segment', 'class', 'order'] properties for each segment.
        """

        try:
            output = ast.literal_eval(llm_output)
        except:
            output = []

        return output
