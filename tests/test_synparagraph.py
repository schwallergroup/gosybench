"""Test suite for the SynthParagraph class"""

import os

import ast
import json
import pytest
from dotenv import load_dotenv
from jasyntho.extract import Extractor

# from jasyntho.doc_extract.synthpar import SynthParagraph

load_dotenv()


with open('tests/synth_child_io/sample.json') as fh:
    data = json.load(fh)
    child_synth_io = [(d['input'], str(d['output'])) for d in data]


def get_children(prg):
    """Execute children extractor chain"""

    oai_key = os.getenv("OPENAI_API_KEY")
    extractor = Extractor("rxn_setup", oai_key).extractor
    out_llm = extractor.child_prop_chain(prg[:400])['text']
    out = ast.literal_eval(out_llm)
    return out


@pytest.mark.parametrize("inp, expect", child_synth_io)
def test_child_extr_chain(inp, expect):
    """Test children extraction chain from paragraphs."""

    exp = ast.literal_eval(expect)
    out = get_children(inp)
    assert out[0]['reference_key'] == exp[0]['reference_key']


#@pytest.fixture
#def uspto_example():
#    """Example of a synthesis paragraph from USPTO"""
#    example = "2-chloro-5-nitropyrimidin-4-amine (1): To a rapidly stirred solution of saturated aqueous ammonium hydroxide (50 mL) and ice in a 0 deg. C. bath was added 2,4-dichloro-5-nitropyrimidine (6.0 g, 31 mmol) in portions. The resulting yellow foamy mixture was allowed to stir for 30 min, at which point the precipitate was isolated by filtration. The solid was rinsed several times with ice-cold water and once with ice cold ethanol to give a peach-colored solid. The crude solid was purified by adsorption onto 18 g silica gel, followed by silica gel chromatography, eluting with 0-20% MeOH/dichloromethane to give 2-chloro-5-nitropyrimidin-4-amine as an off-white solid. MS (ES+): 175 (M+H)+; Calc. for C4H3ClN4O2=174.55."
#    return example
#
#
#def test_synthparagraph(uspto_example):
#    """Create SynthParagraph object."""
#
#    sp = SynthParagraph(uspto_example)
#    assert sp.text == uspto_example
#
#
#
#@pytest.mark.skip(reason="Takes forever")
#def test_extract_paragraph(uspto_example):
#    """Create SynthParagraph object."""
#
#    oai_key = os.getenv("OPENAI_API_KEY")
#    extractor = Extractor("rxn_setup", oai_key)
#
#    sp = SynthParagraph(uspto_example)
#    extract = sp.extract(extractor)[0]
#
#    assert "compound_name" in extract
#    assert "reagents" in extract
#    assert "reference_num" in extract
#
#
#@pytest.mark.skip(reason="not yet implemented")
#def test_extract_rxn_setup(segmented_example):
#    """Test extraction pipeline on rxn_setup.
#    Current pipeline not designed to handle segmented inputs.
#    """
#
#    oai_key = os.getenv("OPENAI_API_KEY")
#
#    extractor = Extractor("rxn_setup", oai_key)
#    result = extractor(segmented_example[0]["text segment"])
#
#    assert "compound_name" in result
