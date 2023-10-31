# -*- coding: utf-8 -*-

"""Command line interface for :mod:`jasyntho`."""


import logging

import click

from .api import segment_sample

__all__ = [
    "main",
]

logger = logging.getLogger(__name__)


@click.command()
@click.option(
    "--model",
    default="gpt35",
    type=click.Choice(["gpt4", "gpt35"]),
    help="What model to use for the segmentation pipeline.",
)
def main(model):
    """main"""
    segment_sample(model)


if __name__ == "__main__":
    main()
