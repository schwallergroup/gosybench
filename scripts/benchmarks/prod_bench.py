import os
import json
import click
import wandb
from jasyntho.metrics import TreeMetrics
from jasyntho.api import SynthesisExtract


llm_list = [
#    "gpt-3.5-turbo",
#    "gpt-4-turbo",
#    "gpt-4-0613",
#    "claude-3-haiku-20240307",
#    "claude-3-sonnet-20240229",
#    "claude-3-opus-20240229",
#    "mistral-small-latest",
#    "mistral-large-latest",
#    "mistral-medium-latest",
    "open-mixtral-8x7b",
    "open-mixtral-8x22b",
]

papers = [
 'jacs.0c09520',
 'jacs.0c12998',
 'jacs.0c13424',
 'jacs.0c10636',
 'jacs.0c12569',
 'jacs.0c12194',
 'jacs.0c01774',
 'jacs.0c06354',
 'jacs.0c03842',
 'jacs.1c01356',
 'jacs.1c00283',
 'jacs.0c06477',
 'jacs.0c03592',
 'jacs.0c12242',
 'jacs.0c03535',
 'jacs.0c10122',
 'jacs.0c02425',
 'jacs.0c04742',
 'jacs.0c07397',
 'jacs.0c12484',
 'jacs.0c07390',
    'jacs.0c00969', 'jacs.0c05479', 'jacs.1c01356', 'jacs.0c07397',
    'jacs.1c01372', 'ja074300t', 'jacs.0c13424', 'jacs.0c10053',
    'jacs.0c06354', 'jacs.0c02513',
    'angewandte_01',
    'jacs.0c11025',
    'jacs.0c07433',
    'jacs.0c09520',
    'jacs.1c00457',
    'jacs.1c01135',
    'jacs.0c03346',
 'jacs.0c09015',
 'jacs.0c00751',
 'ja5131963',
 'jacs.0c09842',
 'jacs.0c10361',
 'jacs.0c13465',
 'jacs.0c12948',
 'jacs.0c05766',
 'jacs.1c00525',
 'jacs.0c03202',
 'jacs.0c02143',
 'jacs.1c01865',
 'jacs.0c11960',
 'jacs.0c06312',
 'ja512124c',
]

papers = set(papers)

def run_jasyntho(inst_model, dspy_model, paper):

    # Initialize stuff
    synthex = SynthesisExtract(inst_model=inst_model, dspy_model=dspy_model)
    metrics = TreeMetrics()

    # Init before to keep track of time
    wandb.init(
        project="jasyntho-product-benchmark-gen",
        config=dict(
            paper=paper.strip('/').split('/')[-1],
            start_model=inst_model,
            #dspy_model=dspy_model,
        )
    )

    # Run
    try:
        tree = synthex(paper, logger=wandb.run)

        # Store trees
        with open(os.path.join(paper, "prods.json"), "w") as f:
            json.dump(tree.raw_prods, f, default=lambda x: x.__dict__, indent=2)

        # Upload plot of SI split
        wandb.log({"si_split": wandb.Image(os.path.join(paper, "SIsignal.png"))})
        wandb.finish()

        return tree

    except Exception as e:
        print(f"Error processing {paper}: {e}")
        wandb.finish()


from jasyntho.extract import Extractor
def run_eval(inst_model):
    # Load products dataset
    pdata = json.load(open("data/benchmarks/products.json", 'r'))

    synthex = Extractor("rxn_setup", model=inst_model)

    def check_reacts(gold, pred):
        """Check if the list of reactants is the same."""

        gold_reacts = set([r['reference_key'] for r in gold['children'] if r['role_in_reaction'] == 'reactant'])
        pred_reacts = set([r.reference_key for r in pred[0].children if r.role_in_reaction == 'reactant'])

        # make all lower case
        gold_reacts = set([r.lower() for r in gold_reacts])
        pred_reacts = set([r.lower() for r in pred_reacts])

        ratio = len(gold_reacts.intersection(pred_reacts))/len(gold_reacts)
        print(ratio)
        return ratio

    def check_solvents(gold, pred):
        """Check if the list of solvents is the same."""

        gold_solvs = set([r['reference_key'] for r in gold['children'] if r['role_in_reaction'] == 'solvent'])
        pred_solvs = set([r.reference_key for r in pred[0].children if r.role_in_reaction == 'solvent'])

        # make all lower case
        gold_solvs = set([r.lower() for r in gold_solvs])
        pred_solvs = set([r.lower() for r in pred_solvs])

        ratio = len(gold_solvs.intersection(pred_solvs))/len(gold_solvs)
        print(ratio)
        return ratio
    
    def check_prdname(gold, pred):
        """Check if the product names are the same."""
        gold_prdname = gold['substance_name']
        pred_prdname = pred[0].substance_name

        return gold_prdname == pred_prdname
    
    def check_prdkey(gold, pred):
        """Check if the product keys are the same."""
        gold_prdkey = gold['reference_key']
        pred_prdkey = pred[0].reference_key

        return gold_prdkey == pred_prdkey
    
    def calc_all_metrics(gold, pred):
        """Calculate all metrics."""
        return {
            'reacts': check_reacts(gold, pred),
            'solvs': check_solvents(gold, pred),
            'prdname': check_prdname(gold, pred),
            'prdkey': check_prdkey(gold, pred),
        }


    wandb.init(
        project="jasyntho-prod-benchmark-llms", 
        config=dict(
            llm=inst_model,
        )
    )

    lp = [synthex(p['text']) for p in pdata]


    def jdump(p):
        return str(json.dumps(
            [c.model_dump() for c in p.children],
            indent=2
        ))

    t = [[i, jdump(p[0]), json.dumps(g, indent=2)] for i, (p, g) in enumerate(zip(lp, pdata))]

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

    wandb.finish()






    # Compare against the actual products
    # Calculate metrics






@click.command()
@click.option(
    "--llm",
    default="gpt-3.5-turbo",
    type=click.Choice(llm_list),
    help="LLM to use for paragraph processing (can be async).",
)
def main(llm):
    for p in papers:
        plink = os.path.join('notebooks/data/', p)
        run_jasyntho(inst_model=llm, paper=plink)


if __name__ == "__main__":
    # main()

    for llm in llm_list:
        try:
            print(f"Running {llm}")
            run_eval(inst_model=llm)
        except Exception as e:
            print(f'Run failedi', e)
            wandb.finish()

