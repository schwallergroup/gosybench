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


@click.command()
@click.option(
    "--model",
    default="gpt-3.5-turbo",
    type=click.Choice(["gpt-3.5-turbo", "gpt-4-turbo", "gpt-4-0613", "claude-opus-20240229", "mistral-small-latest", "mistral-large-latest"]),
    help="LLM to use for synthesis extraction.",
)
def main(model):
    """main"""

    synthex = SynthesisExtract(model=model)
    metrics = TreeMetrics()

    tree = synthex("notebooks/data/1c10539")
    m = metrics(tree)
    print(m)


if __name__ == "__main__":
    main()
