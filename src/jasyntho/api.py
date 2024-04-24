# -*- coding: utf-8 -*-

"""Synthesis extraction API."""

import asyncio
import os
import pickle
from functools import partial
from typing import Optional

import dsp
import dspy
from dotenv import load_dotenv
from pydantic import BaseModel, model_validator

from jasyntho.doc_extract import SynthTree
from jasyntho.extract import Extractor
from jasyntho.utils import set_llm


class SynthesisExtract(BaseModel):
    """Synthesis of a substance."""

    inst_model: str = "gpt-4-0613"
    dspy_model_1: str = "gpt-4-0613"
    dspy_model_2: str = "gpt-4-0613"
    llm: Optional[dsp.LM] = None
    synthex: Optional[BaseModel] = None

    class Config:
        """Model configuration."""

        arbitrary_types_allowed = True

    def __call__(self, file_path: str, logger=None):
        """Call the appropriate method."""

        if self.inst_model.startswith("gpt"):
            print("Using async version")
            return asyncio.run(self.__async_call__(file_path, logger=logger))
        else:
            print("Using sync version")
            return self.__sync_call__(file_path, logger=logger)

    def __sync_call__(self, paper_src: str, logger=None):
        """Return the synthesis (sync version)."""
        tree = SynthTree.from_dir(paper_src, logger)
        tree.select_syntheses()
        tree.rxn_extract = self.synthex
        tree.raw_prods = tree.extract_rss()
        tree = self.after_prod_pipeline(tree)
        return tree

    async def __async_call__(self, paper_src: str, logger=None):
        """Return the synthesis (sync version)."""
        tree = SynthTree.from_dir(paper_src, logger)
        tree.select_syntheses()
        tree.rxn_extract = self.synthex
        tree.raw_prods = await tree.async_extract_rss()
        # tree = self.after_prod_pipeline(tree)
        return tree

    def after_prod_pipeline(self, tree: SynthTree):
        """Run the pipeline after products are extracted."""

        tree.products = [p for p in tree.raw_prods if not p.isempty()]

        reach_sgs = tree.partition()
        print(f"Number of RSGs: {len([r for r in reach_sgs if len(r) > 1])}")

        print("Extending full graph...")
        new_connects = tree.extended_connections()
        tree.reach_subgraphs = tree.partition(new_connects)
        print(f"New Number of RSGs: {len(tree.reach_subgraphs)}")

        print("Gathering smiles...")
        set_llm(self.dspy_model_2)
        tree.gather_smiles()
        json_format = tree.export()  # gets a json for each disjoint tree
        # TODO maybe save
        print(json_format.keys())

        return tree

    @model_validator(mode="after")
    def init_llm_synthex(self):
        """Set the llm and synthesis extractor."""

        load_dotenv()
        if self.llm is None:
            self.llm = set_llm(llm_dspy=self.dspy_model_1)
        if self.synthex is None:
            self.synthex = Extractor("rxn_setup", model=self.inst_model)
        return self
