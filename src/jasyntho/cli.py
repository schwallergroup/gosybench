# -*- coding: utf-8 -*-

"""Command line interface for :mod:`jasyntho`."""


import logging

import click

from jasyntho.metrics import TreeMetrics
from .api import SynthesisExtract

__all__ = [
    "main",
]

logger = logging.getLogger(__name__)

llm_list = [
    "gpt-3.5-turbo",
    "gpt-4-turbo",
    "gpt-4-0613",
    "claude-opus-20240229",
    "mistral-small-latest",
    "mistral-large-latest",
]

@click.command()
@click.option(
    "--inst_model",
    default="gpt-3.5-turbo",
    type=click.Choice(llm_list),
    help="LLM to use for paragraph processing (can be async).",
)
@click.option(
    "--dspy_model",
    default="gpt-3.5-turbo",
    type=click.Choice(llm_list),
    help="LLM to use for elaborate graph building.",
)
def main(inst_model, dspy_model):
    """main"""

    synthex = SynthesisExtract(inst_model=inst_model, dspy_model=dspy_model)
    metrics = TreeMetrics()

    tree = synthex("notebooks/data/1c10539")
    m = metrics(tree)
    print(m)


if __name__ == "__main__":
    main()
