"""LLMChains for segmentation with OpenAI models GPT-4 and GPT-3.5."""

import os

from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI

from .prompts import *


def gpt4_segment(api_key: str) -> LLMChain:
    """
    Initialize GPT-4 for segmentation.

    Input
    _____
    api_key : str
        OpenAI API key.
    """

    load_dotenv()
    openai_key = api_key or os.getenv("OPENAI_API_KEY")

    llm_gpt4 = ChatOpenAI(
        model_name="gpt-4",
        temperature=0.1,
        max_tokens=2048,
        request_timeout=3000,
        openai_api_key=openai_key,
    )

    gpt4_segment = LLMChain(prompt=gpt_prompt_tmplt, llm=llm_gpt4)
    return gpt4_segment


def gpt35_segment(api_key: str) -> LLMChain:
    """
    Initialize GPT-3.5 for segmentation.

    Input
    _____
    api_key : str
        OpenAI API key.
    """

    load_dotenv()
    openai_key = api_key or os.getenv("OPENAI_API_KEY")

    llm_gpt35_turbo = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0.1,
        max_tokens=2048,
        request_timeout=3000,
        openai_api_key=openai_key,
    )

    gpt35_segment = LLMChain(prompt=gpt_prompt_tmplt, llm=llm_gpt35_turbo)
    return gpt35_segment
