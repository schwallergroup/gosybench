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
