"""Test suite for the SynthTree class"""

import os

import pytest
from dotenv import load_dotenv

from syn2act import SynthTree

load_dotenv()


# @pytest.fixture()
@pytest.mark.skip(reason="Takes for ever")
def ex_tree():
    """Initialize document."""
    oai_key = os.getenv("OPENAI_API_KEY")
    doc = SynthTree("tests/examples/synth_SI_sub.pdf", oai_key)
    return doc


@pytest.mark.skip(reason="Takes for ever")
def test_trees_extraction(ex_tree):
    """Check that paragraphs could be parsed into trees"""
    assert len(ex_tree.trees) == 2
    assert ex_tree.trees[0].name == "S1"


@pytest.mark.skip(reason="Takes for ever")
def test_merged_trees(ex_tree):
    """Check that trees can be merged as expected"""
    mts = ex_tree.merged_trees
    assert len(mts) == 1
    assert mts[0].name == "21"
    assert mts[0].children[0].name == "DMP"
