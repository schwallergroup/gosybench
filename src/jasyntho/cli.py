# -*- coding: utf-8 -*-

"""Command line interface for :mod:`jasyntho`."""


import logging

import click

from colorama import Fore
from .api import SynthesisExtract

__all__ = [
    "main",
]

logger = logging.getLogger(__name__)


@click.command()
@click.option(
    "--model",
    default="gpt-3.5-turbo",
    type=click.Choice(["gpt-3.5-turbo", "gpt-4-turbo", "gpt-4-0613", "claude-opus-20240229", "mistral-small-latest", "mistral-large-latest"]),
    help="LLM to use for synthesis extraction.",
)
def main(model):
    """main"""

    synthex = SynthesisExtract(model=model)
    tree = synthex("notebooks/data/1c10539")

    
    import networkx as nx
    print(Fore.LIGHTRED_EX, f"\nNumber of nodes: {len(tree.full_g.nodes)}")
    print(Fore.LIGHTRED_EX, f"Number of edges: {len(tree.full_g.edges)}")
    print(Fore.LIGHTRED_EX, f"Number of products: {len(tree.products)}")
    print(Fore.LIGHTRED_EX, f"Number of RSGs: {len(tree.reach_subgraphs)}\n")
    # Number of nodes with smiles
    nodes_w_attr = [tree.full_g.nodes[n] for n in tree.full_g.nodes if 'attr' in tree.full_g.nodes[n]]
    print(Fore.LIGHTCYAN_EX, f"Number of nodes with smiles: {len([n for n in nodes_w_attr if 'smiles' in n['attr']])}")
    # Longest sequence of nodes
    print(Fore.LIGHTCYAN_EX, f"Longest sequence of nodes: {max([nx.dag_longest_path_length(p) for p in tree.reach_subgraphs.values()])}\n")

    # Longest sequence of nodes with smiles
    def max_length_smiles_one_path(G, source):
        max_length = 0
        max_path = []
        for end_node in G.nodes:
            for path in nx.all_simple_paths(G, source=source, target=end_node):
                if all(['attr' in G.nodes[n].keys() for n in path]):
                    if all([G.nodes[n]['attr'].get('smiles') is not None for n in path]):
                        if len(path) > max_length:
                            max_length = len(path)
                            max_path = path
        return max_path

    def max_seq_smiles(tree):
        ml = 0
        ml_path = []
        source = ''

        for k, g in tree.reach_subgraphs.items():
            if len(g)>1:
                ml_path_tmp = max_length_smiles_one_path(g, k)
                if len(ml_path_tmp) > ml:
                    ml_path = ml_path_tmp
                    ml = len(ml_path_tmp)
                    source = k
        print(Fore.LIGHTYELLOW_EX, f"Maximum path length with smiles: {ml_path}, length: {ml}. Source: {source}\n\n")
        return ml_path, source

    path, max_source = max_seq_smiles(tree)

    # Make image of the longest path
    if max_source != '':
        from rxn_tree_vis.reaction.reactiontree import ReactionTree
        json = tree.export()

        t = ReactionTree.from_dict(json[max_source])
        im = t.to_image()
        im.save(f"img_max_{model}.png")
        print(f"RSG with max SMILES sequence stored at img_max_{model}.png")


    # Number of total reactions recovered (smiles)
    count = 0
    G = tree.full_g
    for u, v in G.edges:
        if 'attr' in G.nodes[u] and 'attr' in G.nodes[v]:
            if G.nodes[u]['attr'].get('smiles') and G.nodes[v]['attr'].get('smiles'):
                print(Fore.LIGHTWHITE_EX, f"\tReaction: {u} -> {v}")
                count += 1
    print(Fore.LIGHTWHITE_EX, f"Number of reactions recovered (smiles): {count}")




if __name__ == "__main__":
    main()
