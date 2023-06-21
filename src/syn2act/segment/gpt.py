"""
LLMChain for extraction. Prepared for GPT-4
"""

import os

from dotenv import load_dotenv
from langchain import chains
from langchain.chat_models import ChatOpenAI
from langchain import llms

from .prompt import *

load_dotenv()

# Load OPENAI API key
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

llm_gpt35_turbo = = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    temperature=0.1,
    max_tokens=2048,
    request_timeout=3000,
    openai_api_key=openai_key,
)

llm_anthropicai = llms.Anthropic(
    model='claude-v1.3',
    temperature=0.1,
    anthropic_api_key=anthropic_api_key,
    max_tokens_to_sample=2000,
    openai_api_key=openai_key,

)


# build up a chain
chain = chains.LLMChain(prompt=ptemplate, llm=llm)
