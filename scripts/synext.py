import os
import json
import wandb
from jasyntho.metrics import TreeMetrics
from jasyntho.api import SynthesisExtract


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

def main(inst_model, dspy_model, paper):

    # Initialize stuff
    synthex = SynthesisExtract(inst_model=inst_model, dspy_model=dspy_model)
    metrics = TreeMetrics()

    # notebooks/data/angewandte_01
    # notebooks/data/1c10539
    # notebooks/data/jacs.0c11025
    # notebooks/data/jacs.0c07433
    # notebooks/data/jacs.0c09520
    # notebooks/data/jacs.1c00457
    # notebooks/data/jacs.1c01135

    # Init before to keep track of time
    wandb.init(
        project="jasyntho-routes",
        config=dict(
            paper=paper.strip('/').split('/')[-1],
            start_model=inst_model,
            dspy_model=dspy_model,
        )
    )

    # Run
    tree = synthex(paper)
    m = metrics(tree)
    wandb.summary.update(m)

    # Upload plot of SI split
    wandb.log({"si_split": wandb.Image(os.path.join(paper, "SIsignal.png"))})
    wandb.finish()

if __name__ == "__main__":
    for llm in llm_list:
        main(inst_model=llm, dspy_model=llm, paper='data/1c10539')
