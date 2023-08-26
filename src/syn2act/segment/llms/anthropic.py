"""LLMChains for segmentation with Anthropic's model Claude-v1.3"""

import os

from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain.chat_models import ChatAnthropic

from .prompts import *


def claude_segment(api_key: str) -> LLMChain:
    """
    Initialize Claude-v1.3 for segmentation.

    Input
    _____
    api_key : str
        Anthropic API key.
    """

    load_dotenv()
    anthropic_api_key = api_key or os.getenv("ANTHROPIC_API_KEY")

    llm_claude = ChatAnthropic(
        model="claude-v1.3",
        temperature=0.1,
        anthropic_api_key=anthropic_api_key,
        max_tokens_to_sample=2000,
    )

    claude_segment = LLMChain(prompt=gpt_prompt_tmplt, llm=llm_claude)

    return claude_segment
