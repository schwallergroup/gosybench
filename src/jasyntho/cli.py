# -*- coding: utf-8 -*-

"""Command line interface for :mod:`jasyntho`."""


import json
import logging
import os

import click
from .api import run_single

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
    "open-mixtral-8x22b",
]


@click.command()
@click.option(
    "--paper",
    default=None,
    type=click.Path(exists=True),
    help="Source of the paper to process.",
)
@click.option(
    "--inst_llm",
    default="gpt-3.5-turbo",
    type=str,
    help="LLM to use for paragraph processing (can be async).",
)
@click.option(
    "--dspy_llm_1",
    default="gpt-3.5-turbo",
    type=click.Choice(llm_list),
    help="LLM to use for elaborate graph building.",
)
@click.option(
    "--dspy_llm_2",
    default="gpt-3.5-turbo",
    type=click.Choice(llm_list),
    help="LLM to use for elaborate graph building.",
)
@click.option(
    "-w",
    "--wandb_project",
    default="jasyntho-routes",
    type=str,
    help="What project name to log the results to.",
)
def run(paper, inst_llm, dspy_llm_1, dspy_llm_2, wandb_project):
    """Run the synthesis extraction on a single paper."""
    run_single(
        paper=paper,
        inst_model=inst_llm,
        dspy_model_1=dspy_llm_1,
        dspy_model_2=dspy_llm_2,
        wandb_pname=wandb_project
    )

@click.command()
@click.option(
    "--inst_llm",
    default="gpt-3.5-turbo",
    type=click.Choice(llm_list),
    help="LLM to use for paragraph processing (can be async).",
)
@click.option(
    "--dspy_llm",
    default="gpt-3.5-turbo",
    type=click.Choice(llm_list),
    help="LLM to use for paragraph processing (can be async).",
)
@click.option(
    "-d",
    "--directory",
    default="../../data/",
    type=click.Path(exists=True),
    help="Directory to the papers to process.",
)
@click.option(
    "-w",
    "--wandb_project",
    default="jasyntho-routes",
    type=str,
    help="What project name to log the results to.",
)
def these_papers(inst_llm, dspy_llm, directory, wandb_project):
    papers = os.listdir(directory)
    for p in papers:
        plink = os.path.join(directory, p)
        try:
            run_single(
                paper=plink,
                inst_model=inst_llm,
                dspy_model_1=dspy_llm,
                dspy_model_2=dspy_llm,
                wandb_pname=wandb_project
            )
        except:
            continue

@click.group()
@click.version_option()
def main():
    """CLI for SACCrow."""

main.add_command(run)
main.add_command(these_papers)


if __name__ == "__main__":
    main()
