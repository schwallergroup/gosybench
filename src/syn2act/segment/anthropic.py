"""LLMChains for segmentation with Anthropic's model Claude-v1.3"""

import os
from typing import List, Optional, Union

from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain.chat_models import ChatAnthropic

from .base import Segmentor
from .prompts import *


class SegClaude(Segmentor):
    """Segmentator with Anthropic's Claude."""

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
        anthropic_api_key = api_key or os.getenv("ANTHROPIC_API_KEY")

        llm = ChatAnthropic(
            model="claude-v1.3",
            temperature=0.1,
            anthropic_api_key=anthropic_api_key,
            max_tokens_to_sample=2000,
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
