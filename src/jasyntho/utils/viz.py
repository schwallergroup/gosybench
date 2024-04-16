"""Visualization utils."""

from typing import Dict
import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout

def plot_graph(G: nx.DiGraph):
    """Plot a graph."""
    fig = plt.figure(figsize=(10, 7))
    pos = graphviz_layout(G, prog="dot")
    nx.draw(G, pos, with_labels=True, arrows=True)
    fig.show()

def plot_graphs(dt: Dict[str, nx.DiGraph]):
    """Plot a dictionary of graphs."""

    for g in dt.values():
        if len(g) > 1:
            plot_graph(g)