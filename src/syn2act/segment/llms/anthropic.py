"""LLMChains for segmentation with Anthropic's model Claude-v1.3"""

import os

from dotenv import load_dotenv
from langchain import chains
from langchain.chat_models import ChatAnthropic

from .prompts import *

load_dotenv()
openai_key = os.getenv("ANTHROPIC_API_KEY")

llm_claude = ChatAnthropic(
    model="claude-v1.3",
    temperature=0.1,
    anthropic_api_key=anthropic_api_key,
    max_tokens_to_sample=2000,
)

claude_segment = chains.LLMChain(prompt=gpt_prompt_tmplt, llm=llm_anthropicai)
