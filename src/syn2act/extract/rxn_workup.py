"""
work_up extraction schema built by Kor API
"""

from kor.extraction import create_extraction_chain
from kor.nodes import Number, Object, Text

from syn2act.segment.gpt import llm_gpt4

from .utils import catalyst, product, solvent

work_up = Object(
    # 'id' defines what will appear in the output.
    id="procedures",
    # Natural language description about the object, helping LLM understand what info to collect
    description="objects reacting in reaction set-up stage in a chemical procedure",
    # Fields to capture fro m a piece of text about the object
    attributes=[
        Text(
            id="action",
            description="The action that the experimentalist took. Choose one of the following: [heat, cold, stir, treat, wash, dilute, unknown]",
        ),
        Text(id="temperature", description="The working temperature of the reaction"),
        Text(id="time", description="The working time of the reaction"),
        Text(id="pressure", description="The pressure under which the reaction is undergone"),
        Text(id="equipment", description="The equipment the experimentalist used in the step"),
        Text(id="description", description="The text describing the step"),
        solvent,
        catalyst,
    ],
    # Example help tell the LLM what is needed
    examples=[
        (
            "The reaction mixture was stirred for 2 h and then concentrated under reduced pressure. \
            The crude residue was treated with (R)-2-(methoxycarbonylamino)-2-phenylacetic acid (44 mg, 0.21 mmol), \
            COMU (100 mg, 0.21 mmol) and DMF (5 mL), then DIPEA (0.18 mL, 1.05 mmol) was added dropwise. \
            After 1 h, the mixture was diluted with 10% MeOH/EtOAc and washed successively with saturated aqueous \
            NaHCO3 and brine. The organics were dried over MgSO4, filtered and concentrated under reduced pressure.",
            [
                {
                    "description": "The reaction mixture was stirred for 2 h and then concentrated under reduced pressure.",
                    "action": "stirred",
                    "time": "2 h",
                },
                {
                    "description": "The reaction mixture was stirred for 2 h and then concentrated under reduced pressure.",
                    "action": "concentrated",
                    "pressure": "reduced pressure",
                },
                {
                    "description": "The crude residue was treated with (R)-2-(methoxycarbonylamino)-2-phenylacetic acid (44 mg, 0.21 mmol), COMU (100 mg, 0.21 mmol) and DMF (5 mL), then DIPEA (0.18 mL, 1.05 mmol) was added dropwise.",
                    "action": "treated",
                    "solvents": [
                        {
                            "name": "(R)-2-(methoxycarbonylamino)-2-phenylacetic acid",
                            "mass": "44 mg",
                            "moles": "0.21 mmol",
                        },
                    ],
                },
                {
                    "description": "The crude residue was treated with (R)-2-(methoxycarbonylamino)-2-phenylacetic acid (44 mg, 0.21 mmol), COMU (100 mg, 0.21 mmol) and DMF (5 mL), then DIPEA (0.18 mL, 1.05 mmol) was added dropwise.",
                    "action": "treated",
                    "solvents": [
                        {"name": "COMU", "mass": "100 mg", "moles": "0.21 mmol"},
                    ],
                },
                {
                    "description": "The crude residue was treated with (R)-2-(methoxycarbonylamino)-2-phenylacetic acid (44 mg, 0.21 mmol), COMU (100 mg, 0.21 mmol) and DMF (5 mL), then DIPEA (0.18 mL, 1.05 mmol) was added dropwise.",
                    "action": "treated",
                    "solvents": [
                        {"name": "DMF", "volume": "5 mL"},
                    ],
                },
                {
                    "description": "The crude residue was treated with (R)-2-(methoxycarbonylamino)-2-phenylacetic acid (44 mg, 0.21 mmol), COMU (100 mg, 0.21 mmol) and DMF (5 mL), then DIPEA (0.18 mL, 1.05 mmol) was added dropwise.",
                    "action": "added dropwise",
                    "solvents": [
                        {"name": "DIPEA", "volume": "0.18 mL", "moles": "1.05 mmol"},
                    ],
                },
                {
                    "description": "After 1 h, the mixture was diluted with 10% MeOH/EtOAc and washed successively with saturated aqueous NaHCO3 and brine.",
                    "time": "1 h",
                    "action": "diluted",
                    "solvents": [
                        {"name": "MeOH/EtOAc", "concentration": "10%"},
                    ],
                },
                {
                    "description": "After 1 h, the mixture was diluted with 10% MeOH/EtOAc and washed successively with saturated aqueous NaHCO3 and brine.",
                    "action": "washed successively",
                    "solvents": [
                        {"name": "aqueous NaHCO3 and brine", "concentration": "saturated"},
                    ],
                },
                {
                    "description": "The organics were dried over MgSO4, filtered and concentrated under reduced pressure.",
                    "action": "dried",
                    "solvents": [
                        {"name": "MgSO4"},
                    ],
                },
                {
                    "description": "The organics were dried over MgSO4, filtered and concentrated under reduced pressure.",
                    "action": "filtered",
                },
                {
                    "description": "The organics were dried over MgSO4, filtered and concentrated under reduced pressure.",
                    "action": "concentrated",
                    "pressure": "reduced pressure",
                },
            ],
        )
    ],
    many=True,
)

work_up_schema = Object(
    id="work_up_properties",
    description="work-up in a chemical reaction",
    attributes=[work_up, product],
    many=True,
)

chain_work_up = create_extraction_chain(llm, work_up_schema, encoder_or_encoder_class="json")
