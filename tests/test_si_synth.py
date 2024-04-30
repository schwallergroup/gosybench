"""Test suite for the SISynthesis class"""

import os

import pytest
from dotenv import load_dotenv

from jasyntho import SynthTree
from jasyntho.extract import Extractor

load_dotenv()


@pytest.fixture()
def ex_document():
    """Initialize document."""
    doc = SynthTree.from_dir("tests/examples/")
    doc.paragraphs = doc._get_paragraphs(doc.doc_src + "/si_0.pdf")
    return doc


def test_parse_doc(ex_document):
    """Check that paragraphs could be parsed"""
    assert len(ex_document.paragraphs) == 3


def test_cut_parags(ex_document):
    """Use subset of paragraphs"""
    ex_document.paragraphs = ex_document.paragraphs[:3]
    assert len(ex_document.paragraphs) == 3


@pytest.mark.skip(reason="Failing")
def test_extract(ex_document):
    """Check we can extract reaction setup"""
    ex_document.paragraphs = ex_document.paragraphs[6:7]

    oai_key = os.getenv("OPENAI_API_KEY")
    rxn_extract = Extractor("rxn_setup", oai_key, model="gpt-3.5-turbo")
    ex_document.rxn_extract = rxn_extract

    ex_document.extract_rss()

    assert isinstance(ex_document.rxn_setups, list)
    assert len(ex_document.rxn_setups) == 1
    assert "compound_name" in ex_document.rxn_setups[0].keys()
    assert (
        ex_document.rxnsetups[0]["compound_name"]
        == "(2R,4R,6S)-6-[3-(Benzyloxy)propyl]-2-(2-{[tert-butyl(diphenyl)silyl]oxy}ethyl)-4-methyldihydro-2H-pyran-3(4H)-one"
    )
