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

        import pathlib

        root_dir = pathlib.Path(__file__).parent.resolve()
        model_dir = f'{root_dir}/../../../models/segment_flant5_large'
        self.model = AutoModelForSeq2SeqLM.from_pretrained(
            model_dir,
            device_map="auto"
        )
        self.tokenizer = AutoTokenizer.from_pretrained(model_dir)
        self.device = "cuda:0"

        adapter_model = "paragraph_segmentation"
        self.model.set_active_adapters(adapter_model)



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

        raw_outputs = self.model.generate(
            **inputs,
            max_length = 2048,
            early_stopping = True
        )
        outputs = self.tokenizer.batch_decode(
            raw_outputs,
            skip_special_tokens=True
        )

        return outputs
