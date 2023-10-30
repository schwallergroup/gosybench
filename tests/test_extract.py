"""Test suite for the extract module"""

import os

import pytest
from dotenv import load_dotenv

from jasyntho.extract import Extractor

load_dotenv()


@pytest.fixture
def segmented_example():
    """Example of a synthesis paragraph from USPTO"""
    example = [
        {
            "text segment": "2-chloro-5-nitropyrimidin-4-amine (1): To a rapidly stirred solution of saturated aqueous ammonium hydroxide (50 mL) and ice in a 0 deg. C. bath was added 2,4-dichloro-5-nitropyrimidine (6.0 g, 31 mmol) in portions.",
            "text class": "reaction set-up",
            "explanation": "this is the reaction set-up step because it describes the preparation of the reaction mixture, including the solvent (saturated aqueous ammonium hydroxide), the temperature (0 deg. C.), and the addition of the reactant (2,4-dichloro-5-nitropyrimidine) in portions.",
            "step order": "1",
        },
        {
            "text segment": "'The resulting yellow foamy mixture was allowed to stir for 30 min, at which point the precipitate was isolated by filtration.'",
            "text class": "work-up",
            "explanation": "this is the work-up step because it describes the process of isolating the precipitate from the reaction mixture by filtration.",
            "step order": "2",
        },
        {
            "text segment": "'The solid was rinsed several times with ice-cold water and once with ice cold ethanol to give a peach-colored solid.'",
            "text class": "work-up",
            "explanation": "this is the work-up step because it describes the process of rinsing the solid with ice-cold water and ethanol to remove impurities and obtain a purified solid product.",
            "step order": "3",
        },
        {
            "text segment": "'The crude solid was purified by adsorption onto 18 g silica gel, followed by silica gel chromatography, eluting with 0-20% MeOH/dichloromethane to give 2-chloro-5-nitropyrimidin-4-amine as an off-white solid.'",
            "text class": "purification",
            "explanation": "this is the purification step because it describes the process of purifying the crude solid by adsorption onto silica gel and subsequent chromatography using a mixture of MeOH and dichloromethane as the eluent.",
            "step order": "4",
        },
        {
            "text segment": "'MS (ES+)",
            "text class": "analysis",
            "explanation": "this is the analysis step because it provides the mass spectrometry data (MS) and the calculated molecular formula for the compound.",
            "step order": "5",
        },
    ]

    return example


@pytest.fixture
def uspto_example():
    """Example of a synthesis paragraph from USPTO"""
    example = "2-chloro-5-nitropyrimidin-4-amine (1): To a rapidly stirred solution of saturated aqueous ammonium hydroxide (50 mL) and ice in a 0 deg. C. bath was added 2,4-dichloro-5-nitropyrimidine (6.0 g, 31 mmol) in portions. The resulting yellow foamy mixture was allowed to stir for 30 min, at which point the precipitate was isolated by filtration. The solid was rinsed several times with ice-cold water and once with ice cold ethanol to give a peach-colored solid. The crude solid was purified by adsorption onto 18 g silica gel, followed by silica gel chromatography, eluting with 0-20% MeOH/dichloromethane to give 2-chloro-5-nitropyrimidin-4-amine as an off-white solid. MS (ES+): 175 (M+H)+; Calc. for C4H3ClN4O2=174.55."
    return example


@pytest.mark.skip(reason="Takes forever")
def test_extract_full(uspto_example):
    """Test extraction pipeline on rxn_setup.
    Ximena designed the pipeline for this use."""

    oai_key = os.getenv("OPENAI_API_KEY")

    extractor = Extractor("rxn_setup", oai_key)
    result = extractor(uspto_example)

    assert "compound_name" in result
    assert "reagents" in result
    assert "reference_num" in result


@pytest.mark.skip(reason="Takes forever")
def test_extract_rxn_setup(segmented_example):
    """Test extraction pipeline on rxn_setup.
    Current pipeline not designed to handle segmented inputs.
    """

    oai_key = os.getenv("OPENAI_API_KEY")

    extractor = Extractor("rxn_setup", oai_key)
    result = extractor(segmented_example[0]["text segment"])

    assert "compound_name" in result
