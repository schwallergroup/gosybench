"""Base types for the GoSyBench package."""

import os
import pickle
from typing import List, Optional

import networkx as nx
from pydantic import BaseModel, Field


class Substance(BaseModel):
    """Substance base class."""

    reference_key: Optional[str] = Field(
        description=(
            "Identifier for a substance described in text. "
            "combination of letters and numbers, like "
            "'S1', '14', '22a', or more complex like 'C8-epi-20' etc."
        )
    )
    substance_name: Optional[str] = Field(
        description="Name of the substance.",
    )


class Product(Substance):
    """Substance with children and properties.

    Args:
        reference_key: Identifier for a substance described in text.
        substance_name: Name of the substance.
        children: List of substances that are children of this substance.
    """

    role_in_reaction: str = "main product"
    children: List[Substance] | None = None


class STree(BaseModel):
    """Minimal representation of a synthetic tree."""

    class Config:
        arbitrary_types_allowed = True

    products: List[Product] = []
    graph: nx.DiGraph = nx.DiGraph()

    @classmethod
    def from_pickle(cls, path: str):

        with open(path, "rb") as f:
            graph = pickle.load(f)

            products = []
            for node in graph.nodes:
                children = []
                for child in graph.successors(node):
                    children.append(
                        Product(
                            reference_key=child,
                            substance_name=graph.nodes[child].get("name"),
                        )
                    )
                products.append(
                    Product(
                        reference_key=node,
                        substance_name=graph.nodes[node].get("name"),
                        children=children,
                    )
                )
            return cls(products=products, graph=graph)

    def export(self):
        """Export the STree's reachable subgraph from source nodes into JSON."""

        json = {}
        for k, g in self.get_components().items():
            try:
                smiles = g.nodes[k]["attr"].get("smiles") or k
                json[k] = {
                    "smiles": smiles,
                    "type": "mol",
                    "in_stock": False,
                    "children": self.json_serialize(g, key=k),
                }
            except:
                continue
        return json

    def json_serialize(self, G, key="10"):
        """Serialize a single reachable subgraph from source node into JSON."""
        # TODO finish this -> convert_to_smiles, etc. Add this somewhere else so that this function is simply format translation

        successors = G.successors(key)
        slist = []
        for s in successors:
            props = G.nodes[s]
            if len(list(G.successors(s))) > 0:
                # Get properties of the node
                if "attr" not in props.keys():
                    continue
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

    def get_components(self):
        G = self.graph
        indegs = G.in_degree()
        components = {}
        for n in G.nodes:
            if indegs[n] == 0:
                desc = nx.descendants(G, n)
                components[n] = G.subgraph(desc | {n})
        return components