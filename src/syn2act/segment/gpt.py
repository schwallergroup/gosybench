import os

from dotenv import load_dotenv
from langchain import chains
from langchain.llms import OpenAI

from .prompt import *

# Load OPENAI API key
load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")

# language model
llm = OpenAI(
    model_name="gpt-4",
    temperature=0.1,
    max_tokens=2048,
    request_timeout=3000,
    openai_api_key=openai_key,
)

# build up a chain
chain = chains.LLMChain(prompt=ptemplate, llm=llm)
