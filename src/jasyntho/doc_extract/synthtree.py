"""
Define class SynthTree.

tree of SynthNodes that represent the chemical synthesis described in pdf doc.
"""

from typing import Dict, List, Optional

import networkx as nx  # type: ignore

from jasyntho.extract import Extractor, Product
from jasyntho.extract.extended import LabConnection
from jasyntho.utils import RetrieveName, name_to_smiles

from .synthdoc import SISynthesis


class SynthTree(SISynthesis):
    """Extend SISynthesis to represent reaction tree."""

    products: List[Product] = []
    full_g: nx.DiGraph = nx.DiGraph()
    reach_subgraphs: Dict[str, nx.DiGraph] = {}

    def gather_smiles(self):
        """Gather all smiles from the products."""

        G = self.full_g
        iupac = RetrieveName(self)

        def _size_reach_sg(G, node):
            """Calc size of each reachable subgraph."""
            rn = set(nx.bfs_tree(G, node))
            return len(rn)

        for k, g in G.nodes.items():
            l = _size_reach_sg(G, k)
            if l > 1:
                if "attr" not in g.keys():
                    return None

                name = g["attr"]["substance_name"]
                labl = g["attr"]["reference_key"]
                smi = name_to_smiles(name, labl)
                if smi is None:
                    # Try to get iupac name
                    retrieved_names = iupac(k, context=g["attr"]["text"])
                    print(f"key {k}. Got iupac name: {retrieved_names}")
                    for n in retrieved_names:
                        smi = name_to_smiles(n, labl)
                        if smi:
                            # Assign iupac and smiles attributes to node
                            g["attr"]["iupac"] = n
                            g["attr"]["smiles"] = smi
                            break
                if smi is not None:
                    g["attr"]["smiles"] = smi

        self.full_g = G
        # TODO try this

    def extended_connections(self):
        """Return the extended connections for a given query."""
        dts = self.get_reachable_subgraphs()
        lab_connect = LabConnection(self)

        new_connects = {}
        for k, g in dts.items():
            if len(g) > 1:
                print(f"Processing reachable subgraph from source node {k}")
                new_connects[k] = lab_connect(k)

        self.reach_subgraphs = self.get_reachable_subgraphs(new_connects)
        return new_connects  # in case we want to use it later

    def get_reachable_subgraphs(self, new_connects: Optional[dict] = None):
        """Merge and find all reachable subgraphs in paper.
        If dict of new connects is given, rewire the graph with new connections.
        """
        prods = self.unique_keys(self.products)
        self.full_g = self.get_full_graph(prods)

        if new_connects is not None:
            self.full_g = self._rewire(self.full_g, new_connects)

        reach_subgraph = SynthTree.get_reach_subgraph(self.full_g)
        return reach_subgraph

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
    def get_reach_subgraph(cls, Gd: nx.DiGraph) -> Dict[str, nx.DiGraph]:
        """
        Get a list of reachable subgraph from source nodes.

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

    # Exporting
    def export(self):
        """Export the SynthTree's reachable subgraph from source nodes into JSON."""

        json = {}
        # For each reachable subgraph from source node, serialize it into JSON
        for k, g in self.reach_subgraphs.items():
            smiles = g.nodes[k]["attr"].get("smiles") or k
            json[k] = {
                "smiles": smiles,
                "type": "mol",
                "in_stock": False,
                "children": self.json_serialize(g, key=k),
            }
        return json

    def json_serialize(self, G, key="10"):
        """Serialize a single reachable subgraph from source node into JSON."""
        # TODO finish this -> convert_to_smiles, etc. Add this somewhere else so that this function is simply format translation

        json = {}
        successors = G.successors(key)
        slist = []
        for s in successors:
            props = G.nodes[s]
            if len(list(G.successors(s))) > 0:
                # Get properties of the node
                name = props["attr"]["substance_name"]
                if "smiles" in props["attr"].keys():
                    smiles = props["attr"]["smiles"]
                else:
                    smiles = name

                # Format json
                slist.append(
                    {
                        "smiles": smiles,
                        "name": name,
                        "type": "mol",
                        "in_stock": False,
                        "children": self.json_serialize(G, key=s),
                    }
                )
            else:
                smiles = s
                slist.append(
                    {
                        "smiles": s,
                        "name": s,
                        "type": "mol",
                        "in_stock": False,
                    }
                )

        final_json = [{"smiles": "", "type": "reaction", "children": slist}]
        return final_json
