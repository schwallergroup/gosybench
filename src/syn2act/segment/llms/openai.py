"""LLMChains for segmentation with OpenAI models GPT-4 and GPT-3.5."""

import os

from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI

from .prompts import *

load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")

llm_gpt4 = ChatOpenAI(
    model_name="gpt-4",
    temperature=0.1,
    max_tokens=2048,
    request_timeout=3000,
    openai_api_key=openai_key,
)

llm_gpt35_turbo = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    temperature=0.1,
    max_tokens=2048,
    request_timeout=3000,
    openai_api_key=openai_key,
)

# build up a chain
gpt4_segment = LLMChain(prompt=gpt_prompt_template, llm=llm_gpt4)
gpt35_segment = LLMChain(prompt=gpt_prompt_template, llm=llm_gpt35_turbo)
