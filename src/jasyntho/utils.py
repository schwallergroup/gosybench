"""Utils for the Jasyntho package."""

import json
import os

import dspy
import requests
from dsp.modules.databricks import custom_client_chat_request, custom_client_completions_request
from pydantic import BaseModel


class Something(BaseModel):
    """A Pydantic model."""

    name: str
    age: int

    def from_lm(cls, s):
        """Reconvert into Something."""
        return cls(name=s.name, age=s.age)


class Mistral(dspy.Databricks):
    """Mistral API client."""

    def __init__(self, model, api_key, api_base, model_type="chat", **kwargs):
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
