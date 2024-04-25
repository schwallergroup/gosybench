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
    "claude-3-haiku-20240307",
    "claude-3-sonnet-20240229",
    "claude-3-opus-20240229",
    "mistral-small-latest",
    "mistral-large-latest",
    "mistral-medium-latest",
    "open-mixtral-8x7b",
    "open-mixtral-8x22b",
]

from jasyntho.extract import Extractor


def run_eval(inst_model):
    # Load products dataset
    pdata = list(open("data/benchmarks/bad_products.json", "r").readlines())

    # Load list from bad_products.json
    synthex = Extractor("rxn_setup", model=inst_model)

    # Basically we want to check that extracted products are empty

    def empty_prod(p):
        return {"empty": p[0].isempty()}

    wandb.init(
        project="jasyntho-badprod-benchmark-llms",
        config=dict(
            llm=inst_model,
        ),
    )

    lp = [synthex(p) for p in pdata]

    def jdump(p):
        return str(json.dumps([c.model_dump() for c in p.children], indent=2))

    t = [
        [i, jdump(p[0]), json.dumps(g, indent=2)]
        for i, (p, g) in enumerate(zip(lp, pdata))
    ]

    table = wandb.Table(data=t, columns=["index", "extracted", "gold"])
    wandb.log({"extraction": table})

    import pandas as pd

    l = []
    for i, pred in enumerate(lp):
        m = empty_prod(pred)
        l.append(m)
        wandb.log(m)

    df = pd.DataFrame(l)
    print(df.mean(axis=0))

    wandb.summary.update(df.mean(axis=0).to_dict())

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
        plink = os.path.join("notebooks/data/", p)
        run_jasyntho(inst_model=llm, paper=plink)


if __name__ == "__main__":
    # main()

    for llm in llm_list:
        try:
            print(f"Running {llm}")
            run_eval(inst_model=llm)
        except Exception as e:
            print(f"Run failed", e)
            wandb.finish()
