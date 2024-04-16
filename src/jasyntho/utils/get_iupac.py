"""Retrieve IUPAC names for substances."""

import re
from typing import List, Optional

import dspy
import networkx as nx
import requests
from pydantic import BaseModel


class SubsIUPAC(dspy.Signature):
    """Retrieve name of a substance."""

    context: str = dspy.InputField(
        desc="Description of the synthesis of substance."
    )
    substance: str = dspy.InputField(desc="The substance to ask about.")

    name: List[str] = dspy.OutputField(
        desc="The context describes the synthesis of substance. What are the names used to refer to substance?"
    )


class RetrieveName(dspy.Module):
    """Retrieve systematic name of a substance."""

    def __init__(self, doc: BaseModel):
        super().__init__()

        self.doc = doc
        self.name = dspy.TypedChainOfThought(SubsIUPAC)
        self.retrieve = doc.acquire_context

    def forward(self, substance: str, context: str):
        """Get the name of the substance."""

        try:
            name = self.name(context=context, substance=substance)
            return name.name
        except ValueError:
            return []

