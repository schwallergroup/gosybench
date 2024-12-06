import json
import os

import click

import wandb
from gosybench import TreeMetrics
from gosybench.api import SynthesisExtract


def run(inst_model, dspy_model_1, dspy_model_2, paper):

    # Initialize stuff
    synthex = SynthesisExtract(
        inst_model=inst_model,
        dspy_model_1=dspy_model_1,
        dspy_model_2=dspy_model_2,
    )
    metrics = TreeMetrics()

    # Init before to keep track of time
    wandb.init(
        project="jasyntho-all-jacs",
        config=dict(
            paper=paper.strip("/").split("/")[-1],
            start_model=inst_model,
            dspy_model_1=dspy_model_1,
            dspy_model_2=dspy_model_2,
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
    "--llm1",
    default="gpt-3.5-turbo",
    type=str,
    help="LLM to use for paragraph processing (can be async).",
)
@click.option(
    "--llm2",
    default="gpt-3.5-turbo",
    type=str,
    help="LLM for extra connection finding",
)
@click.option(
    "--llm3",
    default="gpt-3.5-turbo",
    type=str,
    help="LLM for recovering IUPAC names",
)
@click.option(
    "--dir_",
    default="data/papers/",
    type=click.Path(exists=True),
    help="Path to directory containing papers.",
)
def main(llm1, llm2, llm3, dir_):

    papers = os.listdir(dir_)
    print(papers)

    for p in papers:
        plink = os.path.join(dir_, p)
        print(plink)
        try:
            run(
                inst_model=llm1,
                dspy_model_1=llm2,
                dspy_model_2=llm3,
                paper=plink,
            )
            print(f"Succesfully ran {plink}")
        except:
            continue


if __name__ == "__main__":
    main()
