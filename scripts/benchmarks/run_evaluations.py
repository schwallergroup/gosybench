

# For each paper, evaluate all the methods 

import os
import asyncio
from gosybench.evaluate import GOSyBench
from gosybench.metrics import GraphEval, TreeMetrics
from gosybench.logger import setup_logger
from gosybench.basetypes import STree

logger = setup_logger(__package__)

if __name__ == "__main__":
    gosybench = GOSyBench(
        project="GOSyBench",
        # describe=TreeMetrics(),
        describe=None,
        metrics=GraphEval(),
    )

    def le_base_method(path, name):
        """Simply load a precomputed graph."""
        name = "extracted_graph_gpt35_vision_.pickle"
        logger.debug(f"Loading graph {path}")
        pfile = os.path.join(path, f"{name}")
        tree = STree.from_pickle(pfile)
        # Preprocess graph
        G = tree.graph
        for n in G.nodes:
            if "attr" not in G.nodes[n]:
                G.nodes[n]["attr"] = {}
            G.nodes[n]["attr"]["name"] = n
        tree.graph=G
        return tree

    from functools import partial

    llms = ["gpt4t", "gpt4"]
    vis = ["vision", "text"]
    si_selects = ["", "select"]
    from itertools import product
    for l,v,s in product(llms, vis, si_selects):
        le_method = partial(le_base_method, name=f"extracted_graph_{l}_{v}_{s}.pickle")

        gosybench.evaluate(le_method)


# #         asyncio.run(main(path))


# # for paper in papers:

# #     for model in models:
# #         for method in methods:
# #             for si_select in si_selects:
# #                 asyncio.run(extractg(paper, model, method, si_select))
    