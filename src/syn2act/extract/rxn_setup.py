"""
Reaction set_up extraction schema built by Kor API
"""

from kor.extraction import create_extraction_chain
from kor.nodes import Number, Object, Text

from syn2act.segment.gpt import llm

from .utils import *

reactant = Object(
    # 'id' defines what will appear in the output.
    id="reactants",
    # Natural language description about the object, helping LLM understand what info to collect
    description="objects reacting in reaction set-up stage in a chemical procedure",
    # Fields to capture fro m a piece of text about the object
    attributes=[
        Text(id="name", description="The name of the reactant"),
        Text(id="mass", description="The mass of the reactant"),
        Text(id="moles", description="The moles of the reactant"),
        Text(id="volume", description="The volume of the reactant"),
        Text(id="concentration", description="The concentration of the reactant"),
    ],
    # Example help tell the LLM what is needed
    examples=[
        (
            "Tert-butyl (2S,4S)-2-[5-(2-{(2S,4S)-1-[N-(methoxycarbonyl)-L-valyl]-4-methylpyrrolidin-2-yl}-1,11-dihydroisochromeno[4',3':6,7]naphtho[1,2-d]imidazol-9-yl)-1H-imidazol-2-yl]-4-(methoxymethyl)pyrrolidine-1-carboxylate (166 mg, 0.21 mmol) was dissolved in DCM (4 mL), MeOH (1 mL) and HCl (4 M in dioxane, 1 mL) was added. The reaction mixture was stirred for 2 h and then concentrated under reduced pressure. The crude residue was treated with (R)-2-(methoxycarbonylamino)-2-phenylacetic acid (44 mg, 0.21 mmol), COMU (100 mg, 0.21 mmol) and DMF (5 mL), then DIPEA (0.18 mL, 1.05 mmol) was added dropwise. After 1 h, the mixture was diluted with 10% MeOH/EtOAc and washed successively with saturated aqueous NaHCO3 and brine. The organics were dried over MgSO4, filtered and concentrated under reduced pressure. The crude residue was purified by HPLC to afford methyl {(1R)-2-[(2S,4S)-2-(5-{2-[(2S,4S)-1-{(2S)-2-[(methoxycarbonyl)amino]-3-methylbutanoyl}-4-methylpyrrolidin-2-yl]-1,11-dihydroisochromeno[4',3': 6,7]naphtho[1,2-d]imidazol-9-yl}-1H-imidazol-2-yl)-4-(methoxymethyl)pyrrolidin-1-yl]-2-oxo-1-phenylethyl}carbamate (71 mg, 38%).",
            [
                {
                    "name": "Tert-butyl (2S,4S)-2-[5-(2-{(2S,4S)-1-[N-(methoxycarbonyl)-L-valyl]-4-methylpyrrolidin-2-yl}-1,11-dihydroisochromeno[4',3':6,7]naphtho[1,2-d]imidazol-9-yl)-1H-imidazol-2-yl]-4-(methoxymethyl)pyrrolidine-1-carboxylate",
                    "mass": "166 mg",
                    "moles": "0.21 mmol",
                },
                {
                    "name": "(R)-2-(methoxycarbonylamino)-2-phenylacetic acid",
                    "mass": "44 mg",
                    "moles": "0.21 mmol",
                },
                {"name": "COMU", "mass": "100 mg", "moles": "0.21 mmol"},
                {"name": "DIPEA", "volume": "0.18 mL", "moles": "1.05 mmol"},
            ],
        ),
        (
            "PL 137,526 describes the hydrogenation of p-tert-butylphenol to form p-tert-butylcyclohexanol using a nickel catalyst. ",
            [{"name": "p-tert-butylphenol"}],
        ),
    ],
    many=True,
)

object_schema = Object(
    id="properties",
    description="object in a chemical reaction",
    attributes=[reactant, solvent, catalyst, product, reaction],
    many=True,
)

chain_object = create_extraction_chain(llm, object_schema, encoder_or_encoder_class="json")
