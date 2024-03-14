"""Gather knowledge about substances from the extended document (paper+SI)"""

import json
from typing import Any, Dict, List

import dspy
import instructor
from dsp.utils import deduplicate
from openai import OpenAI
from pydantic import BaseModel, Field

from jasyntho.doc_extract.synthtree import SynthTree

from .instructor import ExSubstances


class DirectSubs(dspy.Signature):
    """Answer a question about substance."""

    context = dspy.InputField(
        desc="May contain relevant facts about the substance."
    )
    substance = dspy.InputField(desc="The substance to ask about.")
    question = dspy.InputField()
    answer = dspy.OutputField(desc="A detailed answer to the question.")


class Gather1Subs(dspy.Module):
    """Retrieve info for one substance."""

    def __init__(self, doc: SynthTree):
        """Initialize the module."""
        super().__init__()

        self.doc = doc
        self.get_context_summary = dspy.ChainOfThought(DirectSubs)
        self.get_substances = ExSubstances.from_context

        # Cache to store answers for substances
        self.lib: dict = {}
        self.role_questions: List[str] = [
            "What is the role of this substance in the paper?",
        ]

    def forward(self, substance):
        """Retrieve information about a substance."""
        context = self.retrieve(doc=self.doc.paper, query=substance)

        lm_ctxt = []
        for q in self.role_questions:
            if f"{substance}: {q}" in self.lib:
                lm_ctxt.append(self.lib[f"{substance}: {q}"])
                continue

            ctxt_sum = self.get_context_summary(
                context=context, question=q, substance=substance
            )
            subs_ctx = self.get_substances(ctxt_sum.answer).substances

            ans = {
                "context": ctxt_sum.answer,
                "question": f"{substance}: {q}",
                "substances": [s.reference_key for s in subs_ctx],
            }
            self.lib[f"{substance}: {q}"] = ans
            lm_ctxt.append(ans)

        # HERE

        return lm_ctxt

    def retrieve(self, doc, query):
        """Retrieve the context for a substance."""
        ctxt = self.doc.acquire_context(doc=doc, query=query)
        return "\n\n".join(ctxt)


class SContext(dspy.Signature):
    """Summarize the provided context. Clarify the role of `substance`."""

    context = dspy.InputField(
        desc="Contains distilled information about the relations between `substance` and other substances in a paper."
    )
    substance = dspy.InputField(desc="Focus on this substance.")
    answer = dspy.OutputField(desc="A detailed answer to the question.")


class SubstanceContext(dspy.Module):
    """Gather context for a substance. Then answer what is the role of `substance`."""

    def __init__(self, doc: SynthTree):
        """Initialize the module."""
        super().__init__()
        self.doc = doc
        self.context: List[Dict[str, Any]] = []
        self.substance_context = Gather1Subs(self.doc)
        self.generate_answer = dspy.ChainOfThought(SContext)
        self.sset: set = set()

    def forward(self, substance: str, depth: int = 2):
        """Gather context with a tree search of depth `depth`, starting from `substance`.
        Then answer what is the role of `substance`."""
        self.gather_deep_context(substance, depth)
        fctxt = self.format_context()
        print(f"Final context: {fctxt}")

        return self.generate_answer(context=fctxt, substance=substance)

    def gather_deep_context(self, substance, depth):
        """Recursively build list of substances connected to `substance` at `depth`."""
        if depth == 0:
            return self.sset
        else:
            new_subs = self.connected_substances(substance)
            self.sset.update(new_subs)
            print(f"Depth {depth}: {substance} -> {new_subs}")
            for s in new_subs:
                self.gather_deep_context(s, depth - 1)

    def format_context(self):
        """Format the context for the model."""
        ctxt = [f"{c['context']}" for c in self.context]
        fstr = "\n\n".join(deduplicate(ctxt))
        return fstr

    def connected_substances(self, substance):
        """Return the substances connected to the `substance` in the `context`."""

        # TODO: pass 2 substances: the source and the query.
        # e.g. role of 8 regarding 29?

        ctxt = self.substance_context(substance)
        subs = set()
        for c in ctxt:
            self.context.append(c)  # Gather context
            subs.update(c["substances"])
        return subs
