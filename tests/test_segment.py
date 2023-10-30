"""Test suite for the segment module"""

import os

import pytest
from dotenv import load_dotenv

from syn2act.segment import SegFlanT5, SegGPT

load_dotenv()


@pytest.fixture
def uspto_example():
    """Example of a synthesis paragraph from USPTO"""

    example = "To a rapidly stirred solution of saturated aqueous ammonium hydroxide (50 mL) and ice in a 0 deg. C. bath was added 2,4-dichloro-5-nitropyrimidine (6.0 g, 31 mmol) in portions. The resulting yellow foamy mixture was allowed to stir for 30 min, at which point the precipitate was isolated by filtration. The solid was rinsed several times with ice-cold water and once with ice cold ethanol to give a peach-colored solid. The crude solid was purified by adsorption onto 18 g silica gel, followed by silica gel chromatography, eluting with 0-20% MeOH/dichloromethane to give 2-chloro-5-nitropyrimidin-4-amine as an off-white solid. MS (ES+): 175 (M+H)+; Calc. for C4H3ClN4O2=174.55."
    return example


@pytest.mark.skip(reason="Takes forever")
def test_segmentor_oai(uspto_example):
    """Test OpenAI models."""

    oai_key = os.getenv("OPENAI_API_KEY")

    gpt4segm = SegGPT("gpt-4", oai_key)
    out_gpt4 = gpt4segm(uspto_example)
    assert isinstance(out_gpt4, list)
    assert list(out_gpt4[0][0].keys())[0] == "text segment"

    gpt35segm = SegGPT("gpt-3.5-turbo-16k", oai_key)
    out_gpt35 = gpt35segm(uspto_example)
    assert isinstance(out_gpt35[0], list)
    print(gpt35segm)
    assert list(out_gpt35[0][0].keys())[0] == "text segment"


@pytest.mark.skip(reason="Takes forever")
def test_segmentor_flant5(uspto_example):
    """Test fine-tuned Flan-T5 model."""

    t5segm = SegFlanT5()
    out_segm = t5segm(uspto_example)
    assert isinstance(out_segm, list)
    assert list(out_segm[0][0].keys())[0] == "text segment"
