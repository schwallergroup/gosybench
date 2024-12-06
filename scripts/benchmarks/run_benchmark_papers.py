"""Run all benchmarks on multiple models."""

import asyncio
import os
import pickle

import wandb
from gosybench import TreeMetrics
from jasyntho import SynthTree
from jasyntho.extract import ExtractReaction

# For an input paper, run extraction using various methods, log each


async def extractg(
    path, model="gpt-3.5-turbo", method="text", si_select=False
):

    wandb.init(
        project="graphex-benchmark",
        config=dict(
            paper=path.split("/")[-1],
            product_model=model,
            parsing_method=method,
            si_select=si_select,
        ),
    )

    metrics = TreeMetrics()

    try:
        tree = SynthTree.from_dir(path)
        tree.rxn_extract = ExtractReaction(llm=model)

        tree.raw_prods = await tree.async_extract_rss(
            mode=method, si_select=si_select
        )
        tree.products = [p for p in tree.raw_prods if not p.isempty()]
        tree.full_g = tree.get_full_graph(tree.products)
        tree.reach_subgraphs = tree.get_reach_subgraphs(tree.full_g)

        if model == "gpt-3.5-turbo":
            k = "gpt35"
        elif model == "gpt-4-turbo":
            k = "gpt4t"
        elif model == "gpt-4":
            k = "gpt4"
        elif model == "gpt-4o":
            k = "gpt4o"

        if si_select:
            si = "select"
        else:
            si = ""

        with open(
            os.path.join(path, f"extracted_graph_{k}_{method}_{si}.pickle"),
            "wb",
        ) as f:
            pickle.dump(tree.full_g, f)

        # Calc descriptors for extracted graph
        m = metrics(tree)
        print(f"CELA {m}")
        wandb.summary.update(dict(**m, success=True))
    except Exception as e:
        print(e)
        wandb.summary.update({"success": False})
    wandb.finish()

    # return tree.full_g


async def main(path):
    for method in ["vision", "text"]:
        for model in ["gpt-3.5-turbo", "gpt-4-turbo"]:
            for si_select in [True, False]:
                og = await extractg(
                    path, model=model, method=method, si_select=si_select
                )

                # if model == "gpt-3.5-turbo":
                #     k = "gpt35"
                # elif model == "gpt-4-turbo":
                #     k = "gpt4t"
                # elif model == "gpt-4":
                #     k = "gpt4"
                # elif model == "gpt-4o":
                #     k = "gpt4o"

                # if si_select:
                #     si = "_select"
                # else:
                #     si = ""
                # with open(os.path.join(path, f'extracted_graph_{k}_{method}{si}.pickle'), 'rb') as f:
                #     og = pickle.load(f)
                #     print(k, method, si)


if __name__ == "__main__":

    papers = [
        "jacs.0c00363",
        # "ja074300t",
        # "jacs.0c00308",
        # "jacs.0c02143",
        # "jacs.0c02513",
        # "jacs.1c01356",
        # "jacs.1c00293",
        # "jacs.3c01991",
        # "jacs.3c07019",
        # "jacs.8b00148",
        # "jacs.7b13260",
        # "jacs.7b09929",
        # "jacs.7b00807",
        # "jacs.9b12546",
        # "jacs.9b09699",
        # "jacs.9b05013",
        # "jacs.8b13029",
        # "jacs.8b06755",
        # "jacs.8b03015",
        # "jacs.7b11299",
        # "jacs.7b08749",
        # "jacs.7b07724",
        # "jacs.7b06055",
        # "jacs.7b01454",
        # "jacs.6b07846",
        # "jacs.2c13889",
        # "jacs.2c12529",
        # "jacs.2c06934",
        # "jacs.0c10122",
    ]
    for p in papers:
        root_gosybench = "src/gosybench/data/papers/"
        path = os.path.join(root_gosybench, p)
        asyncio.run(main(path))
