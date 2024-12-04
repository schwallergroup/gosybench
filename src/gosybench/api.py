# -*- coding: utf-8 -*-

"""API for GOSyBench."""

import networkx as nx
from gosybench.basetypes import STree
from gosybench.evaluate import GOSyBench
from gosybench.metrics import GraphEval


def test_method(x: str) -> STree:
    """Test method."""
    g = nx.DiGraph()
    g.add_edge("a", "b")
    return STree(graph=g)


if __name__ == "__main__":
    gosybench = GOSyBench(
        project="GOSyBench",
        describe=None,
        metrics=GraphEval(),
    )

    # Evaluate
    gosybench.evaluate(test_method)
