"""
LLMChain for extraction. Prepared for GPT-4
"""

import os

from dotenv import load_dotenv
from langchain import chains
from langchain.chat_models import ChatAnthropic, ChatOpenAI

from .prompt import *

# Load OPENAI API key
load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")


# language model
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

llm_anthropicai = ChatAnthropic(
    model="claude-v1.3",
    temperature=0.1,
    anthropic_api_key=anthropic_api_key,
    max_tokens_to_sample=2000,
)


# build up a chain
chain_gpt4 = chains.LLMChain(prompt=ptemplate, llm=llm_gpt4)

chain_gpt35_turbo = chains.LLMChain(prompt=ptemplate, llm=llm_gpt35_turbo)

chain_anthropicai = chains.LLMChain(prompt=ptemplate, llm=llm_anthropicai)
