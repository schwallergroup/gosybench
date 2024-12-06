"""Calculate metrics for an extracted tree."""

import json
import os
from typing import Any

import networkx as nx
from pydantic import BaseModel

from gosybench.basetypes import STree
from gosybench.logger import setup_logger

from .utils import SmilesPathFinder

logger = setup_logger(__package__)


class TreeMetrics(BaseModel):
    """Calculate descriptive metrics for an extracted tree."""

    smiles_path_solver: Any = SmilesPathFinder()

    def __call__(self, tree, directory="."):
        """Run all metrics."""
        gd = self.graph_describe(tree)
        rxns = self.total_reactions(tree)
        max_source = self.max_seq_smiles(tree)

        tjson = tree.export()
        with open(os.path.join(directory, "tree.json"), "w") as f:
            json.dump(tjson, f, indent=4)

        # self.draw_tree(tree, max_source["source_max_len"], directory)
        return dict(**gd, **rxns, **max_source)

    def graph_describe(self, tree: STree):
        """Calculate properties of the extracted graph."""

        logger.debug("Calculating graph properties.")

        G = tree.graph
        if len(G.nodes) == 0:
            return dict(
                nnodes=0,
                nedges=0,
                nproducts=0,
                nrgs_initial=0,
                max_node_seq=0,
                paths_longer_than_5=0,
            )

        logger.debug(f"Number of nodes: {len(G.nodes)}")
        logger.debug(f"Number of edges: {len(G.edges)}")
        logger.debug(f"Number of products: {len(tree.products)}")

        tree_components = tree.get_components()
        nrgs = len([r for r in tree_components if len(r) > 1])
        logger.debug(f"Number of components: {nrgs}")

        # Number of nodes with smiles
        nodes_w_attr = [
            G.nodes[n] for n in G.nodes if "attr" in tree.graph.nodes[n]
        ]
        logger.debug(
            f"Number of nodes with smiles: {len([n for n in nodes_w_attr if 'smiles' in n['attr']])}"
        )

        # Count max node in-degree
        max_in_degree = max([G.in_degree(n) for n in G.nodes])

        # Longest sequence of nodes
        try:
            max_node_seq = max(
                [
                    nx.dag_longest_path_length(p)
                    for p in tree_components.values()
                ]
            )
            logger.debug(f"Longest sequence of nodes: {max_node_seq}")
        except:
            max_node_seq = "--"
            logger.debug("Error calculating longest sequence.")

        # Count how many sequences are longer than 5
        count_5 = 0
        for k, v in tree_components.items():
            try:
                if nx.dag_longest_path_length(v) > 5:
                    count_5 += 1
            except:
                pass

        return dict(
            nnodes=len(G.nodes),
            nedges=len(G.edges),
            nproducts=len(tree.products),
            nrgs_initial=nrgs,
            max_node_seq=max_node_seq,
            paths_longer_than_5=count_5,
            max_in_degree=max_in_degree,
        )

    def total_reactions(self, tree: STree):
        """Calculate the total number of reactions in the tree."""
        logger.debug("Calculating total number of reactions with SMILES.")

        count = 0
        G = tree.graph
        for u, v in G.edges:
            if "attr" in G.nodes[u] and "attr" in G.nodes[v]:
                if G.nodes[u]["attr"].get("smiles") and G.nodes[v]["attr"].get(
                    "smiles"
                ):
                    logger.debug(f"\tReaction: {v} -> {u}")
                    count += 1
        logger.debug(f"Number of reactions recovered (smiles): {count}")
        return dict(total_single_reactions=count)

    def max_seq_smiles(self, tree: STree):
        """Find the top-3 longest paths in the tree such that all nodes have smiles."""

        result = self.smiles_path_solver.max_seq_smiles(self.stree)
        return result
