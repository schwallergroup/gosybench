"""Run all benchmarks on multiple models."""

import json
import os

import re
import click

import wandb
from jasyntho.api import SynthesisExtract
from jasyntho.metrics import TreeMetrics
from jasyntho.extract import Extractor
from jasyntho.utils import RetrieveName, set_llm

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

def run_products(inst_model):
    pdata = json.load(open("data/benchmarks/products.json", "r"))
    synthex = Extractor("rxn_setup", model=inst_model)

    def check_reacts(gold, pred):
        """Check if the list of reactants is the same."""

        gold_reacts = set(
            [
                r["reference_key"]
                for r in gold["children"]
                if r["role_in_reaction"] == "reactant"
            ]
        )
        pred_reacts = set(
            [
                r.reference_key
                for r in pred[0].children
                if r.role_in_reaction == "reactant"
            ]
        )

        # make all lower case
        gold_reacts = set([r.lower() for r in gold_reacts])
        pred_reacts = set([r.lower() for r in pred_reacts])

        ratio = len(gold_reacts.intersection(pred_reacts)) / len(gold_reacts)
        return ratio

    def check_solvents(gold, pred):
        """Check if the list of solvents is the same."""

        gold_solvs = set(
            [
                r["reference_key"]
                for r in gold["children"]
                if r["role_in_reaction"] == "solvent"
            ]
        )
        pred_solvs = set(
            [
                r.reference_key
                for r in pred[0].children
                if r.role_in_reaction == "solvent"
            ]
        )

        # make all lower case
        gold_solvs = set([r.lower() for r in gold_solvs])
        pred_solvs = set([r.lower() for r in pred_solvs])
        ratio = len(gold_solvs.intersection(pred_solvs)) / len(gold_solvs)
        return ratio

    def check_prdname(gold, pred):
        """Check if the product names are the same."""
        gold_prdname = gold["substance_name"]
        pred_prdname = pred[0].substance_name
        return gold_prdname == pred_prdname

    def check_prdkey(gold, pred):
        """Check if the product keys are the same."""
        gold_prdkey = gold["reference_key"]
        pred_prdkey = pred[0].reference_key
        return gold_prdkey == pred_prdkey

    def calc_all_metrics(gold, pred):
        """Calculate all metrics."""
        return {
            "reacts": check_reacts(gold, pred),
            "solvs": check_solvents(gold, pred),
            "prdname": check_prdname(gold, pred),
            "prdkey": check_prdkey(gold, pred),
        }

    lp = [synthex(p["text"]) for p in pdata]

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
    for i, (gold, pred) in enumerate(zip(pdata, lp)):
        m = calc_all_metrics(gold, pred)
        l.append(m)
        wandb.log(m)

    df = pd.DataFrame(l)
    print(df.mean(axis=0))

    wandb.summary.update(df.mean(axis=0).to_dict())

def run_badprods(inst_model):
    pdata = list(open("data/benchmarks/bad_products.json", "r").readlines())
    synthex = Extractor("rxn_setup", model=inst_model)

    # Basically we want to check that extracted products are empty

    def empty_prod(p):
        return {"empty": p.isempty()}

    lp = [synthex(p)[0] for p in pdata]

    def jdump(p):
        return str(json.dumps([c.model_dump() for c in p.children], indent=2))

    t = [
        [i, jdump(p), json.dumps(g, indent=2)]
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

def run_nameretrieve(inst_model):

    set_llm(llm_dspy=inst_model)

    pdata = json.load(open("data/benchmarks/samples_iupac.json", "r"))

    # Check that name is the same
    def exact_match(gold, pred):
        return gold["content"]["name"] == pred.name[0]

    def loose_match(gold, pred):
        return gold["content"]["name"].lower() in [c.lower() for c in pred.name]

    def loose_match_rm_key(gold, pred):
        subs_label = gold["content"]["ref_key"]
        names = pred.name
        namesl = []
        for name in names:
            if subs_label in name:
                regex = f"\(?{subs_label}\)?"
                name = re.sub(regex, "", name.lower())
                namesl.append(name)
                print(name)
            else:
                namesl.append(name.lower())

        return gold["content"]["name"].lower() in namesl

    def calc_all_metrics(gold, pred):
        if pred is not None:
            return {
                "exact_match": exact_match(gold, pred),
                "loose_match": loose_match(gold, pred),
                "loose_match_rm_key": loose_match_rm_key(gold, pred),
            }
        else:
            return {
                "exact_match": False,
                "loose_match": False,
                "loose_match_rm_key": False,
            }

    gname = RetrieveName()
    def cname(p):
        try:
            return gname(context=p["content"]["text"], substance=p["content"]["ref_key"])
        except:
            return None
        
    lp = [cname(p) for p in pdata]

    t = [
        [json.dumps(dict(name=p.name if p is not None else ""), indent=2), json.dumps(g, indent=2)]
        for i, (p, g) in enumerate(zip(lp, pdata))
    ]

    table = wandb.Table(data=t, columns=["extracted", "gold"])
    wandb.log({"extraction": table})

    import pandas as pd

    l = []
    for i, (pred, gold) in enumerate(zip(lp, pdata)):
        m = calc_all_metrics(gold, pred)
        l.append(m)
        wandb.log(m)

    df = pd.DataFrame(l)
    print(df.mean(axis=0))

    wandb.summary.update(df.mean(axis=0).to_dict())


# @click.command()
# @click.option(
#     "--llm",
#     default="gpt-3.5-turbo",
#     type=click.Choice(llm_list),
#     help="LLM to use for paragraph processing (can be async).",
# )
def main(llm):
    wandb.init(
        project="jasyntho-benchmark-llms",
        config=dict(
            llm=llm,
        ),
    )
    try:
        print(f"Running prods {llm}")
        run_products(inst_model=llm)
    except Exception as e:
        print(f"Run failed", e)
    try:
        print(f"Running badprods {llm}")
        run_badprods(inst_model=llm)
    except Exception as e:
        print(f"Run failed", e)
    try:
        print(f"Running nameretrieve {llm}")
        run_nameretrieve(inst_model=llm)
    except Exception as e:
        print(f"Run failed", e)

    wandb.finish()

if __name__ == "__main__":
    for llm in llm_list:
        main(llm)
