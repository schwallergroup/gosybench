"""
Define class SynthTree.

tree of SynthNodes that represent the chemical synthesis described in pdf doc.
"""

from typing import List, Optional

import networkx as nx  # type: ignore

from jasyntho.extract import Extractor, Product
from jasyntho.extract.extended import LabConnection

from .synthdoc import SISynthesis


class SynthTree(SISynthesis):
    """Extend SISynthesis to represent reaction tree."""

    products: List[Product] = []
    full_g: nx.DiGraph = nx.DiGraph()
    list_disjoint: List[nx.DiGraph] = []

    def extended_connections(self):
        """Return the extended connections for a given query."""
        dts = self.disjoint_trees()
        lab_connect = LabConnection(self)

        new_connects = {}
        for k, g in dts.items():
            if len(g) > 1:
                print(f"Processing disjoint tree {k}")
                new_connects[k] = lab_connect(k)

        self.list_disjoint = self.disjoint_trees(new_connects)
        return new_connects  # in case we want to use it later

    def disjoint_trees(self, new_connects: Optional[dict] = None):
        """Merge and find all disjoint trees in paper.
        If dict of new connects is given, rewire the graph with new connections.
        """
        prods = self.unique_keys(self.products)
        full_g = self.get_full_graph(prods)

        if new_connects is not None:
            full_g = self._rewire(full_g, new_connects)

        list_disjoint = SynthTree.get_list_disjoint(full_g)
        return list_disjoint

    def _rewire(self, full_graph, new_connects):
        """Rewire the graph with new connections."""
        # add new edges
        for k, res in new_connects.items():
            if res is not None:
                prod_step = res["step 2"]
                if prod_step is not None:
                    prod = prod_step.product.reference_key
                    if prod in full_graph.nodes:
                        if k != prod:
                            full_graph.add_edge(prod, k)
        return full_graph

    @classmethod
    def unique_keys(cls, trees):
        """Return a list of trees with unique IDs.

        For now simply keep a unique one. the first found
        """
        ftrees = {}
        for t in trees:
            if t.reference_key not in ftrees.keys():
                ftrees[t.reference_key] = t
        return list(ftrees.values())

    def get_full_graph(
        self,
        product_list: List[Product],
        children_types: List[str] = ["reactant", "reagent", "catalyst"],
    ):
        """Build a graph using input disconnected nodes."""
        # Directed graph
        Gd = nx.DiGraph()

        # Add each node
        for p in product_list:
            # Add node with properties
            if p.reference_key is not None:
                Gd.add_node(
                    p.reference_key, attr=p.model_dump()  # type: ignore
                )
            else:
                print(f"\t- Error adding node: {p.note}")
            for c in p.children:
                if c.role_in_reaction in children_types:
                    Gd.add_edge(
                        p.reference_key,
                        c.reference_key,
                        attr={"type": "lab reaction"},
                    )
        return Gd

    @classmethod
    def get_list_disjoint(cls, Gd: nx.DiGraph):
        """
        Get a list of disjoint trees.

        Find all nodes with indegree==0 (heads) and find subgraph of reachable
        nodes.
        """
        # Get list of heads
        heads = [n for n, indeg in Gd.in_degree() if indeg == 0]

        for h in Gd.nodes:
            if h in heads:
                Gd.nodes[h]["is_head"] = True
            else:
                Gd.nodes[h]["is_head"] = False

        # Extract subgraphs reachable from each head node.
        def extract_subgraph(graph, start_node):
            """Use BFS to find all nodes reachable from start_node."""
            reachable_nodes = set(nx.bfs_tree(graph, start_node))
            return graph.subgraph(reachable_nodes).copy()

        # Store the subgraphs in a list
        subgraphs = {
            node: extract_subgraph(Gd, node)
            for node in Gd
            if Gd.nodes[node]["is_head"]
        }
        return subgraphs
