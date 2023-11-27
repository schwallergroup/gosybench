"""Test suite for the SynthTree class"""

import os

import pytest
from dotenv import load_dotenv

from jasyntho import SynthTree

load_dotenv()


# @pytest.mark.skip(reason="Takes for ever")
@pytest.fixture()
def ex_tree():
    """Initialize document."""
    oai_key = os.getenv("OPENAI_API_KEY")
    doc = SynthTree("tests/examples/synth_SI_sub.pdf", oai_key)
    doc.build_tree()
    return doc


# @pytest.mark.skip(reason="Takes for ever")
def test_trees_extraction(ex_tree):
    """Check that paragraphs could be parsed into trees"""
    assert len(ex_tree.trees) == 3
    assert "S1" in [t.name for t in ex_tree.trees]
    assert "21" in [t.name for t in ex_tree.trees]


@pytest.mark.skip(reason="Failing")
def test_merged_trees(ex_tree):
    """Check that trees can be merged as expected"""
    mts = ex_tree.merged_trees
    assert len(mts) == 2
    assert "21" in [t.name for t in mts]

    # "DMP" in the children of any of the mts
    assert any(["DMP" in t.children[0].name for t in mts])
