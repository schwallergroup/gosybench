"""LLMChains for segmentation with OpenAI models GPT-4 and GPT-3.5."""

import os
from typing import List, Optional, Union

from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI

from .base import Segmentor
from .prompts import *


class SegGPT(Segmentor):
    """Segmentator with GPT-3/4."""

    def __init__(self, model: Optional[str] = "gpt-4", api_key: Optional[str] = None) -> None:
        """Segmentor class with OpenAI GPT models for Chat.
        Input
        _____
        model: str
            one of `gpt-4` or `gpt-3.5-turbo-16k`
        openai_key: str
            api_key for OpenAI
        """

        load_dotenv()
        openai_key = api_key or os.getenv("OPENAI_API_KEY")

        llm = ChatOpenAI(
            model_name=model,
            temperature=0.1,
            max_tokens=2048,
            request_timeout=3000,
            openai_api_key=openai_key,
        )

        self.llmchain = LLMChain(prompt=gpt_prompt_tmplt, llm=llm)

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

        outputs = [self.llmchain.run({"example": human_example, "paragraph": p}) for p in inputs]

        return outputs
