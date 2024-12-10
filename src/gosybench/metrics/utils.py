"""Optimized solver to find the longest path in a tree with SMILES."""

from typing import Dict, Union

import networkx as nx

from gosybench.basetypes import STree
from gosybench.logger import setup_logger

logger = setup_logger(__package__)


class SmilesPathFinder:
    """Optimized solver to find the longest path in a tree with SMILES."""

    def __init__(self):
        self.top_paths = []

    def has_smiles(self, g: nx.DiGraph, node):
        """Check if a node has a SMILES attribute."""
        return "attr" in g.nodes[node] and "smiles" in g.nodes[node]["attr"]

    def is_subpath(self, path, longer_paths):
        """Check if a path is a subpath of any of the longer paths."""
        path_set = set(path)
        return any(
            path_set.issubset(set(longer_path)) for longer_path in longer_paths
        )

    def dfs_longest_path(self, g: nx.DiGraph, node, path=None):
        """Depth-first search to find the longest path in a tree."""
        if path is None:
            path = []

        if not self.has_smiles(g, node):
            return

        path = path + [node]

        is_leaf = True
        for neighbor in g.successors(node):
            if neighbor not in path and self.has_smiles(g, neighbor):
                is_leaf = False
                self.dfs_longest_path(g, neighbor, path)

        if is_leaf and not self.is_subpath(
            path, [p for p, _ in self.top_paths]
        ):
            self.top_paths.append((path, len(path)))
            self.top_paths.sort(key=lambda x: x[1], reverse=True)
            if len(self.top_paths) > 3:
                self.top_paths.pop()

    def max_seq_smiles(self, tree: STree):
        """Find the longest path in a tree with SMILES."""
        logger.debug("Calculating maximum path length with SMILES.")

        tree_components = tree.get_components()

        all_paths = []
        results: Dict[str, Union[str, int]] = {}
        for k, g in tree_components.items():
            self.top_paths = []  # Reset for each component
            if len(g) > 1:
                self.dfs_longest_path(g, k)
                all_paths += [(p, l, k) for p, l in self.top_paths]

        # Add placeholders
        for i in range(3):
            results[f"long_path_{i}_len"] = 0
            results[f"long_path_{i}_src"] = "None"

        # Sort by length
        all_paths.sort(key=lambda x: x[1], reverse=True)
        for i, (path, length, source) in enumerate(all_paths):
            if i == 3:
                break
            smi_path = [tree.graph.nodes[n]["attr"]["smiles"] for n in path]
            logger.debug(f"Longest path {i}: {smi_path}")
            results[f"long_path_{i}_len"] = length
            results[f"long_path_{i}_src"] = source

        return results
