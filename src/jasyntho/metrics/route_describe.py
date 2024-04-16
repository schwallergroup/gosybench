"""Calculate metrics for an extracted tree."""

import networkx as nx
from colorama import Fore
from pydantic import BaseModel
from rxn_tree_vis.reaction.reactiontree import ReactionTree

from jasyntho import SynthTree


class TreeMetrics(BaseModel):

    def __call__(self, tree):
        """Run all metrics."""
        gd = self.graph_describe(tree)
        rxns = self.total_reactions(tree)
        max_source = self.max_seq_smiles(tree)

        self.draw_tree(tree, max_source["source_max_len"], "max")
        return dict(**gd, **rxns, **max_source)

    def graph_describe(self, tree: SynthTree):
        """Calculate properties of the extracted graph."""

        G = tree.full_g

        print(Fore.LIGHTRED_EX, f"\nNumber of nodes: {len(G.nodes)}")
        print(Fore.LIGHTRED_EX, f"Number of edges: {len(G.edges)}")
        print(Fore.LIGHTRED_EX, f"Number of products: {len(tree.products)}")

        rgs_init = len(tree.reach_subgraphs)
        print(Fore.LIGHTRED_EX, f"Number of RSGs: {rgs_init}\n")

        # Number of nodes with smiles
        nodes_w_attr = [
            G.nodes[n] for n in G.nodes if "attr" in tree.full_g.nodes[n]
        ]
        print(
            Fore.LIGHTCYAN_EX,
            f"Number of nodes with smiles: {len([n for n in nodes_w_attr if 'smiles' in n['attr']])}",
        )
        # Longest sequence of nodes
        max_node_seq = max(
            [
                nx.dag_longest_path_length(p)
                for p in tree.reach_subgraphs.values()
            ]
        )
        print(
            Fore.LIGHTCYAN_EX, f"Longest sequence of nodes: {max_node_seq}\n"
        )

        return dict(rgs_init=rgs_init, max_node_seq=max_node_seq)

    def total_reactions(self, tree: SynthTree):
        """Calculate the total number of reactions in the tree."""
        count = 0
        G = tree.full_g
        for u, v in G.edges:
            if "attr" in G.nodes[u] and "attr" in G.nodes[v]:
                if G.nodes[u]["attr"].get("smiles") and G.nodes[v]["attr"].get(
                    "smiles"
                ):
                    print(Fore.LIGHTWHITE_EX, f"\tReaction: {u} -> {v}")
                    count += 1
        print(
            Fore.LIGHTWHITE_EX,
            f"Number of reactions recovered (smiles): {count}",
        )
        return dict(total_reactions=count)

    def max_seq_smiles(self, tree: SynthTree):
        """Find the longest path in the tree such that all nodes have smiles."""
        ml = 0
        ml_path = []
        source = ""

        for k, g in tree.reach_subgraphs.items():
            if len(g) > 1:
                ml_path_tmp = self._max_length_smiles_one_path(g, k)
                if len(ml_path_tmp) > ml:
                    ml_path = ml_path_tmp
                    ml = len(ml_path_tmp)
                    source = k
        print(
            Fore.LIGHTYELLOW_EX,
            f"Maximum path length with smiles: {ml_path}, length: {ml}. Source: {source}\n\n",
        )
        return dict(max_len_path=ml_path, max_len=ml, source_max_len=source)

    def _max_length_smiles_one_path(self, G, source):
        """Find the longest path in a RSG such that all nodes have smiles."""

        max_length = 0
        max_path = []
        for end_node in G.nodes:
            for path in nx.all_simple_paths(G, source=source, target=end_node):
                if all(["attr" in G.nodes[n].keys() for n in path]):
                    if all(
                        [
                            G.nodes[n]["attr"].get("smiles") is not None
                            for n in path
                        ]
                    ):
                        if len(path) > max_length:
                            max_length = len(path)
                            max_path = path
        return max_path

    def draw_tree(self, tree: SynthTree, max_source, model=""):
        """Draw a tree (RSG)."""

        # Make image of the longest path
        if max_source != "":
            json = tree.export()

            t = ReactionTree.from_dict(json[max_source])
            im = t.to_image()
            im.save(f"img_max_{model}.png")
            print(
                f"RSG with max SMILES sequence stored at img_max_{model}.png"
            )
