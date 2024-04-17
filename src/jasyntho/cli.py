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
    "claude-3-haiku-20240307",
    "claude-3-sonnet-20240229",
    "claude-3-opus-20240229",
    "mistral-small-latest",
    "mistral-large-latest",
    "mistral-medium-latest",
    "open-mixtral-8x7b",
]


@click.command()
@click.option(
    "--paper",
    default=None,
    type=click.Path(exists=True),
    help="Source of the paper to process.",
)
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
def main(paper, inst_model, dspy_model):

    # Initialize stuff
    synthex = SynthesisExtract(inst_model=inst_model, dspy_model=dspy_model)
    metrics = TreeMetrics()

    # Try with paper_src = "notebooks/data/angewandte_01"
    # "notebooks/data/1c10539"

    # Run
    tree = synthex(paper)
    m = metrics(tree)
    print(m)

    # Save json
    tjson = tree.export()
    with open(os.path.join(paper, "tree.json"), "w") as f:
        json.dump(tjson, f, indent=4)


if __name__ == "__main__":
    main()
