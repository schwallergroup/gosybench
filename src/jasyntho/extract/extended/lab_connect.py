"""Module to extract experimental connections between substances."""

from typing import List

import dspy
from pydantic import BaseModel, Field

from .signatures import ExperimentalConnection, SynthConnection


# TODO it will probs be necessary to find synonyms, find the uses of the byproducts
class LabConnection(dspy.Module):
    """Find experimental connections between substances."""

    def __init__(self, doc: BaseModel):
        super().__init__()

        self.doc = doc
        self.connect = dspy.TypedPredictor(ExperimentalConnection)
        self.retrieve = doc.acquire_context
        self.synth_conn = dspy.TypedPredictor(SynthConnection)

    def forward(self, substance: str):
        """Get summ of substance context, then find if it is a reactant. If so, find the product."""

        ec = self.get_summarize_context(substance)
        if ec.is_reactant:
            try:
                sc = self.synth_conn(
                    context=ec.reaction_description, substance=substance
                )
                return {"step 1": ec, "step 2": sc}
            except:
                return {"step 1": ec, "step 2": None}
        else:
            return None

    def get_summarize_context(self, substance: str):
        """Get and summarize the context to answer if substance leads to a product."""

        # TODO Find a way of filtering irrelevant context, specially for non-specific queries (e.g. "A", "10", etc)
        context = self.retrieve(substance, self.doc.paper)
        if len(context) == 0:
            context = self.retrieve(substance, self.doc.si)

        token_limit = 16000
        token_ratio = 0.7
        cc = int(token_limit / token_ratio)
        ctxt_str = "\n\n".join(context)[:cc]

        exp_connect = self.connect(
            context=ctxt_str,
            substance=substance,
        )
        return exp_connect
