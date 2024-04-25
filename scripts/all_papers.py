import json
import os

import click

import wandb
from jasyntho.api import SynthesisExtract
from jasyntho.metrics import TreeMetrics

llm_list = [
    "gpt-3.5-turbo",
    "gpt-4-turbo",
    "gpt-4-0613",
    "gpt-4-turbo-2024-04-09",
    "claude-3-haiku-20240307",
    "claude-3-sonnet-20240229",
    "claude-3-opus-20240229",
    "mistral-small-latest",
    "mistral-large-latest",
    "mistral-medium-latest",
    "open-mixtral-8x7b",
    "open-mixtral-8x22b",
]

papers = [
    "jacs.0c00969",
    "jacs.0c05479",
    "jacs.1c01356",
    "jacs.0c07397",
    "jacs.1c01372",
    "ja074300t",
    "jacs.0c13424",
    "jacs.0c10053",
    "jacs.0c06354",
    "jacs.0c02513",
    "angewandte_01",
    "jacs.0c11025",
    "jacs.0c07433",
    "jacs.0c09520",
    "jacs.1c00457",
    "jacs.1c01135",
]


def run(inst_model, dspy_model, paper):

    # Initialize stuff
    synthex = SynthesisExtract(inst_model=inst_model, dspy_model=dspy_model)
    metrics = TreeMetrics()

    # Init before to keep track of time
    wandb.init(
        project="jasyntho-routes",
        config=dict(
            paper=paper.strip("/").split("/")[-1],
            start_model=inst_model,
            dspy_model=dspy_model,
        ),
    )

    # Run
    tree = synthex(paper, logger=wandb.run)
    m = metrics(tree)
    wandb.summary.update(m)

    # Upload plot of SI split
    wandb.log({"si_split": wandb.Image(os.path.join(paper, "SIsignal.png"))})
    wandb.finish()


@click.command()
@click.option(
    "--llm",
    default="gpt-3.5-turbo",
    type=click.Choice(llm_list),
    help="LLM to use for paragraph processing (can be async).",
)
def main(llm):
    for p in papers:
        plink = os.path.join('../../data/', p)
        try:
            run(inst_model=llm, dspy_model=llm, paper=plink)
        except:
            continue


if __name__ == "__main__":
    main()
