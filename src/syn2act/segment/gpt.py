from langchain.llms import OpenAI
from langchain import chains

from .prompt import *
from api import OPENAI_API_KEY

# language model
llm = OpenAI(model_name="gpt-4",
    temperature=0.1,
    max_tokens=2048,
    request_timeout=3000,
    openai_api_key=OPENAI_API_KEY,
)

# build up a chain
chain = chains.LLMChain(
    prompt = ptemplate,
    llm = llm
)
