import os
import json
import click
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

def run(inst_model, dspy_model, paper):

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

    except Exception as e:
        print(f"Error processing {paper}: {e}")
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
        plink = os.path.join('notebooks/data/', p)
        run(inst_model=llm, dspy_model=llm, paper=plink)


if __name__ == "__main__":
    main()
