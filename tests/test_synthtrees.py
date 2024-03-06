"""Test suite for the SynthTree class"""

import os

import pytest
from dotenv import load_dotenv

from jasyntho import SynthTree
from jasyntho.extract import Extractor

load_dotenv()


# @pytest.mark.skip(reason="Takes for ever")
@pytest.fixture()
def ex_tree():
    """Initialize document."""
    oai_key = os.getenv("OPENAI_API_KEY")
    rxn_extract = Extractor("rxn_setup", oai_key, model="gpt-4")

    doc = SynthTree.from_dir(
        "tests/examples",
    )
    doc.rxn_extract = rxn_extract

    doc.products = doc.extract_rss()
    doc.extract_rss()
    return doc


# @pytest.mark.skip(reason="Takes for ever")
def test_trees_extraction(ex_tree):
    """Check that paragraphs could be parsed into trees"""
    assert "S1" in [t.reference_key for t in ex_tree.products]
    assert "21" in [t.reference_key for t in ex_tree.products]


# @pytest.mark.skip(reason="Failing")
def test_merged_trees(ex_tree):
    """Check that trees can be merged as expected"""
    mts = ex_tree.merged_trees
    assert len(mts) == 2
    assert "21" in [t.name for t in mts]

    # "DMP" in the children of any of the mts
    assert any(["DMP" in t.children[0].name for t in mts])
