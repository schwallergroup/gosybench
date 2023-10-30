"""Test suite for the par2tree.document module"""

import os

import pytest
from dotenv import load_dotenv

from syn2act.doc_extract import SynthDocument

load_dotenv()


@pytest.fixture()
def ex_document():
    """Initialize document."""

    oai_key = os.getenv("OPENAI_API_KEY")
    doc = SynthDocument("tests/examples/synth_SI.pdf", oai_key)
    return doc


def test_parse_doc(ex_document):
    """Check that paragraphs could be parsed"""
    assert len(ex_document.paragraphs) == 73


def test_cut_parags(ex_document):
    """Use subset of paragraphs"""
    ex_document.paragraphs = ex_document.paragraphs[:3]
    assert len(ex_document.paragraphs) == 3


@pytest.mark.skip(reason="Takes for ever")
def test_extract(ex_document):
    """Check we can extract reaction setup"""
    ex_document.paragraphs = ex_document.paragraphs[6:7]
    ex_document.extract_rss()

    assert isinstance(ex_document.rxn_setups, list)
    assert len(ex_document.rxn_setups) == 1
    assert "compound_name" in ex_document.rxn_setups[0].keys()
    assert (
        ex_document.rxnsetups[0]["compound_name"]
        == "(2R,4R,6S)-6-[3-(Benzyloxy)propyl]-2-(2-{[tert-butyl(diphenyl)silyl]oxy}ethyl)-4-methyldihydro-2H-pyran-3(4H)-one"
    )
