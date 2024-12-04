"""Load precomputed graphs for each method, and evaluate it."""

import os
from functools import partial
from itertools import product

import networkx as nx

from gosybench.basetypes import STree
from gosybench.evaluate import GOSyBench
from gosybench.logger import setup_logger
from gosybench.metrics import GraphEval

logger = setup_logger(__package__)


def main():
    gosybench = GOSyBench(
        project="GOSyBench-eval",
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

    llms = ["gpt35", "gpt4t"]
    vis = ["vision", "text"]
    si_selects = ["", "select"]

    for l, v, s in product(llms, vis, si_selects):
        le_method = partial(
            le_base_method, name=f"extracted_graph_{l}_{v}_{s}.pickle"
        )
        le_method.__name__ = f"le_{l}_{v}_{s}"
        gosybench.evaluate(le_method)


if __name__ == "__main__":
    main()
