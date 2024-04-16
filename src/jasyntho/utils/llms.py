"""Utils for the Jasyntho package."""

import json
import os

import dspy
import requests
from dsp.modules.databricks import custom_client_chat_request, custom_client_completions_request


class Mistral(dspy.Databricks):
    """Mistral API client."""

    def __init__(
        self,
        model,
        api_key,
        api_base="https://api.mistral.ai/v1/",
        model_type="chat",
        **kwargs,
    ):
        """Initialize Mistral API client."""
        super().__init__(model, api_key, api_base, model_type, **kwargs)

    def basic_request(self, prompt: str, **kwargs):
        """Make a basic request to the API.
        Only change is removing some kwargs."""
        raw_kwargs = kwargs

        kwargs = {**self.kwargs, **kwargs}

        kwargs.pop("body", None)
        kwargs.pop("n", None)

        if self.model_type == "chat":
            kwargs["messages"] = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ]
            kwargs = {"stringify_request": json.dumps(kwargs)}
            response = custom_client_chat_request(**kwargs).model_dump_json()
            response = json.loads(response)
        else:
            kwargs["prompt"] = prompt
            response = custom_client_completions_request(
                **kwargs
            ).model_dump_json()
            response = json.loads(response)

        history = {
            "prompt": prompt,
            "response": response,
            "kwargs": kwargs,
            "raw_kwargs": raw_kwargs,
        }
        self.history.append(history)
        return response

    def __call__(
        self, prompt, only_completed=True, return_sorted=False, **kwargs
    ):
        response = self.request(prompt, **kwargs)
        completions = [result["text"] for result in response["content"]]
        return completions


class Claude(dspy.Databricks):
    """Claude API client."""

    def __init__(
        self,
        model,
        api_key,
        api_base="https://api.anthropic.com/v1/messages",
        model_type="chat",
        max_tokens=1000,
        **kwargs,
    ):
        """Initialize Claude API client."""
        super().__init__(model, api_key, api_base, model_type, **kwargs)
        self.model = model
        self.api_key = api_key
        self.base_url = api_base
        self.model_type = model_type
        self.max_tokens = max_tokens

    def basic_request(self, prompt: str, **kwargs):
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "anthropic-beta": "messages-2023-12-15",
            "content-type": "application/json",
        }

        data = {
            **kwargs,
            "max_tokens": self.max_tokens,
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
        }

        response = requests.post(self.base_url, headers=headers, json=data)
        response = response.json()

        self.history.append(
            {
                "prompt": prompt,
                "response": response,
                "kwargs": kwargs,
            }
        )
        return response

    def __call__(
        self, prompt, only_completed=True, return_sorted=False, **kwargs
    ):
        response = self.request(prompt, **kwargs)

        completions = [result["text"] for result in response["content"]]

        return completions

    # def basic_request(self, prompt: str, **kwargs):
    #     """Make a basic request to the API.
    #     Only change is removing some kwargs."""
    #     raw_kwargs = kwargs

    #     kwargs = {**self.kwargs, **kwargs}

    #     # kwargs.pop("body", None)
    #     # kwargs.pop("n", None)

    #     if self.model_type == "chat":
    #         kwargs["messages"] = [
    #             {"role": "system", "content": "You are a helpful assistant."},
    #             {"role": "user", "content": prompt},
    #         ]
    #         kwargs = {"stringify_request": json.dumps(kwargs)}
    #         response = custom_client_chat_request(**kwargs).model_dump_json()
    #         response = json.loads(response)
    #     else:
    #         kwargs["prompt"] = prompt
    #         response = custom_client_completions_request(
    #             **kwargs
    #         ).model_dump_json()
    #         response = json.loads(response)

    #     history = {
    #         "prompt": prompt,
    #         "response": response,
    #         "kwargs": kwargs,
    #         "raw_kwargs": raw_kwargs,
    #     }
    #     self.history.append(history)
    #     return response

    # def __call__(self, prompt, only_completed=True, return_sorted=False, **kwargs):
    #     response = self.request(prompt, **kwargs)
    #     completions = [result["text"] for result in response["content"]]
    #     return completions


# class Claude(LM):
#     def __init__(self, model, api_key):
#         self.model = model
#         self.api_key = api_key
#         self.provider = "default"
#         self.base_url =

#     def basic_request(self, prompt: str, **kwargs):
#         headers = {
#             "x-api-key": self.api_key,
#             "anthropic-version": "2023-06-01",
#             "anthropic-beta": "messages-2023-12-15",
#             "content-type": "application/json"
#         }

#         data = {
#             **kwargs,
#             "model": self.model,
#             "messages": [
#                 {"role": "user", "content": prompt}
#             ]
#         }

#         response = requests.post(self.base_url, headers=headers, json=data)
#         response = response.json()

#         self.history.append({
#             "prompt": prompt,
#             "response": response,
#             "kwargs": kwargs,
#         })
#         return response

#     def __call__(self, prompt, only_completed=True, return_sorted=False, **kwargs):
#         response = self.request(prompt, **kwargs)

#         completions = [result["text"] for result in response["content"]]

#         return completions


# Make something like this for instructor. Can we set a global LLM?
def set_llm(llm_nodes: str = "gpt-4-0613", llm_dspy: str = "gpt-4-0613"):
    """Define the llms to be used."""

    from dotenv import load_dotenv

    load_dotenv()

    T = 0.05
    max_len = 1000

    # First setup LLM for nodes (using instructor atm)
    if llm_nodes.startswith("gpt"):
        pass

    # Now setup LLM for dspy
    if llm_dspy.startswith("gpt"):
        language_model = dspy.OpenAI(
            model=llm_dspy,
            temperature=T,
            max_tokens=max_len,
        )
    elif llm_dspy.startswith("mistral"):

        mistral_key = os.getenv("MISTRAL_API_KEY")
        language_model = Mistral(
            model=llm_dspy,
            api_key=mistral_key,
            temperature=T,
            max_tokens=max_len,
        )
    elif llm_dspy.startswith("claude"):
        anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        language_model = Claude(
            model=llm_dspy,
            api_key=anthropic_key,
            temperature=T,
            max_tokens=max_len,
        )
    else:
        raise ValueError(f"Language model {llm_dspy} not recognized.")

    dspy.settings.configure(lm=language_model)
    return language_model
