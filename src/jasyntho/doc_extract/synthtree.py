"""
Define class SynthTree.

tree of SynthNodes that represent the chemical synthesis described in pdf doc.
"""

from typing import List, Optional

import networkx as nx  # type: ignore

from jasyntho.extract import Product

from .synthdoc import SynthDocument


class SynthTree(SynthDocument):
    """Extend SynthDocument to represent reaction tree."""

    def __init__(
        self,
        doc_src: str,
        api_key: Optional[str] = None,
        model: str = "gpt-4-0314",
        startp: int = 0,
        endp: Optional[int] = None,
    ) -> None:
        """Initialize a SynthTree object."""
        super(SynthTree, self).__init__(
            doc_src, api_key, model, startp, endp
        )  # TODO: select startp and endp automatically from doc_src

    def disjoint_trees(self):
        """Merge and find all disjoint trees in paper."""
        prods = self.unique_keys(self.products)
        full_g = self.get_full_graph(prods)
        list_disj = SynthTree.get_list_disjoint(full_g)
        return list_disj

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
        subgraphs = [
            extract_subgraph(Gd, node)
            for node in Gd
            if Gd.nodes[node]["is_head"]
        ]
        return subgraphs
