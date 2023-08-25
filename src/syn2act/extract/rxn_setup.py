""" 
Reaction set_up extraction schema built by Kor API
"""

from kor.extraction import create_extraction_chain
from kor.nodes import Number, Object, Text

from syn2act.segment.gpt import llm_gpt4

from .utils import catalyst, product, reaction, solvent

reactant = Object(
    # 'id' defines what will appear in the output.
    id="reactants",
    # Natural language description about the object, helping LLM understand what info to collect
    description="objects reacting in reaction set-up stage in a chemical procedure",
    # Fields to capture fro m a piece of text about the object
    attributes=[
        Text(id="name", description="The name of the reactant"),
        Text(id="reference_num", description="Number code used to reference the reactant"),
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
        (
            "To a stirred solution of alkyne 17 3 (3.00 g, 8.86 mmol, 1.0 equiv) in CH2Cl2 (10 mL) at 25 °C was added Co2(CO)8 (3.63 g, 10.6 mmol, 1.2 equiv) in one portion. After 20 min, a solution of oleﬁn 16 4 (3.90 g, 17.7 mmol, 2.0 equiv) in CH2Cl2 (8 mL) was added. The reaction mixture was cooled to 0 °C, and BF3∙Et2O (2.19 mL, 17.7 mmol, 2.0 equiv) was added dropwise.",
            [
                {
                    "name": "alkyne",
                    "reference_num": "17",
                    "mass": "3.00 g",
                    "moles": "8.86 mmol",
                },
                {
                    "name": "Co2(CO)8",
                    "mass": "3.63 g",
                    "moles": "10.6 mmol",
                },
                {
                    "name": "oleﬁn",
                    "reference_num": "16",
                    "mass": "3.90 g",
                    "moles": "17.7 mmol",
                },
                {"name": "BF3∙Et2O", "volume": "2.19 mL", "moles": "17.7 mmol"},
            ],
        ),
    ],
    many=True,
)

set_up_schema = Object(
    id="set_up_properties",
    description="set-up step in a chemical reaction",
    attributes=[reactant, solvent, catalyst, product, reaction],
    many=True,
)

chain_set_up = create_extraction_chain(llm_gpt4, set_up_schema, encoder_or_encoder_class="json")
chain_reactants = create_extraction_chain(llm_gpt4, reactant, encoder_or_encoder_class="json")
