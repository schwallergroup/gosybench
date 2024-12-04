# For each paper, evaluate all the methods

import asyncio
import os

import networkx as nx

from gosybench.basetypes import STree
from gosybench.evaluate import GOSyBench
from gosybench.logger import setup_logger
from gosybench.metrics import GraphEval, TreeMetrics

logger = setup_logger(__package__)

if __name__ == "__main__":
    gosybench = GOSyBench(
        project="GOSyBench-eval",
        # describe=TreeMetrics(),
        describe=None,
        metrics=GraphEval(),
    )

    def le_base_method(path, name):
        """Simply load a precomputed graph."""
        logger.debug(f"Loading graph {path}")
        pfile = os.path.join(path, f"{name}")
        try:
            tree = STree.from_pickle(pfile)
            return tree
        except Exception as e:
            logger.error(f"Error loading {pfile}: {e}")
            return STree(tree=[], graph=nx.DiGraph())

    from functools import partial

    llms = ["gpt35"]  # "gpt4t",
    vis = ["vision", "text"]
    si_selects = ["", "select"]
    from itertools import product

    for l, v, s in product(llms, vis, si_selects):
        le_method = partial(
            le_base_method, name=f"extracted_graph_{l}_{v}_{s}.pickle"
        )
        le_method.__name__ = f"le_{l}_{v}_{s}"

        gosybench.evaluate(le_method)


# #         asyncio.run(main(path))


# # for paper in papers:

# #     for model in models:
# #         for method in methods:
# #             for si_select in si_selects:
# #                 asyncio.run(extractg(paper, model, method, si_select))
