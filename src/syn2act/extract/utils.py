"""
utiliy schema built by Kor API which are multiply used in many schemas
"""

from kor.extraction import create_extraction_chain
from kor.nodes import Number, Object, Text

from syn2act.segment.gpt import llm_gpt4

solvent = Object(
    id="solvents",
    description="objects dissolving solutes, such as reactants and catalysts, in reaction set-up stage in a chemical procedure",
    attributes=[
        Text(id="name", description="The name of the solvent"),
        Text(id="mass", description="The mass of the solvent"),
        Text(id="moles", description="The moles of the solvent"),
        Text(id="volume", description="The volume of the solvent"),
        Text(id="concentration", description="The concentration of the solvent"),
    ],
    examples=[
        (
            "Tert-butyl (2S,4S)-2-[5-(2-{(2S,4S)-1-[N-(methoxycarbonyl)-L-valyl]-4-methylpyrrolidin-2-yl}-1,11-dihydroisochromeno[4',3':6,7]naphtho[1,2-d]imidazol-9-yl)-1H-imidazol-2-yl]-4-(methoxymethyl)pyrrolidine-1-carboxylate (166 mg, 0.21 mmol) \
            was dissolved in DCM (4 mL), MeOH (1 mL) and HCl (4 M in dioxane, 1 mL) was added. \
            The reaction mixture was stirred for 2 h and then concentrated under reduced pressure. \
            The crude residue was treated with (R)-2-(methoxycarbonylamino)-2-phenylacetic acid (44 mg, 0.21 mmol), COMU (100 mg, 0.21 mmol) and DMF (5 mL), then DIPEA (0.18 mL, 1.05 mmol) was added dropwise. \
            After 1 h, the mixture was diluted with 10% MeOH/EtOAc and washed successively with saturated aqueous NaHCO3 and brine. The organics were dried over MgSO4, \
            filtered and concentrated under reduced pressure. The crude residue was purified by HPLC to afford \
            methyl {(1R)-2-[(2S,4S)-2-(5-{2-[(2S,4S)-1-{(2S)-2-[(methoxycarbonyl)amino]-3-methylbutanoyl}-4-methylpyrrolidin-2-yl]-1,11-dihydroisochromeno[4',3': 6,7]naphtho[1,2-d]imidazol-9-yl}-1H-imidazol-2-yl)-4-(methoxymethyl)pyrrolidin-1-yl]-2-oxo-1-phenylethyl}carbamate (71 mg, 38%).",
            [
                {"name": "DCM", "volume": "4 mL"},
                {"name": "MeOH", "volume": "1 mL"},
                {"name": "HCl (in dioxane)", "volume": "1 mL", "concentration": "4M"},
                {"name": "DMF", "volume": "5 mL"},
            ],
        )
    ],
    many=True,
)

catalyst = Object(
    id="catalysts",
    description=(
        "substances that increase the rate of a chemical reaction without itself undergoing any permanent chemical change."
        "substances appearing in reaction set-up stage in a chemical procedure."
    ),
    attributes=[
        Text(id="name", description="The name of the catalyst"),
        Text(id="mass", description="The mass of the catalyst"),
        Text(id="moles", description="The moles of the catalyst"),
        Text(id="volume", description="The volume of the catalyst"),
        Text(id="concentration", description="The concentration of the catalyst"),
    ],
    examples=[
        (
            "To a suspension of (2,2-Dimethyl-5-oxo-[1,3]dioxolan-4-ylidene)-acetic acid, Compound III-A, (4.5 g, 26.2 mmol) in benzene (30 mL) was added oxalyl chloride (15 mL) \
            and the resulting mixture was heated at reflux for 1 h. The mixture was cooled to room temp. and concentrated. \
            The residue was dissolved in methylene chloride (30 mL) and cooled to 0° C. To this was added a suspension of \
            (3,4-dichloro-benzyl)-methyl-amine hydrochloride salt (5.0 g, 22.1 mmol) in methylene chloride (30 mL) and pyridine (18 mL). \
            The resulting mixture was stirred at room temp for 18 h then diluted with 1N HCl. The aqueous phase was saturated with sodium \
            chloride and extracted with methylene chloride (3 times). The organic layers were combined, dried (Na2SO4), and concentrated. \
            The brown oil was purified over silica gel eluting with ethyl acetate/hexane (1:1) to give the title compound as a pale yellow \
            oil that solidified to a white solid upon standing (6.2 g, 82% yield). 1H NMR (300 MHz, DMSO) δ: 7.44-7.10 (m, 3H), 6.16 (s, 0.66H), \
            6.08 (s, 0.33H), 4.59 (s, 1.33H), 4.53 (s, 0.67H), 3.02 (s, 2H), 2.97 (s, 1H), 1.74 (s, 4H), 1.69 (s, 2H).",
            [
                {"Name": "pyridine", "Volume": "18 mL"},
            ],
        ),
        (
            "PL 137,526 describes the hydrogenation of p-tert-butylphenol to form p-tert-butylcyclohexanol using a nickel catalyst. ",
            [{"name": "nickel"}],
        ),
    ],
    many=True,
)

product = Object(
    id="products",
    description="substance present at the end of a chemical reaction",
    attributes=[
        Text(id="name", description="The name of the product"),
        Text(
            id="reference_num",
            description="Number code used to reference the product. Common to be in parenthesis",
        ),
        Text(id="mass", description="The mass of the product"),
        Text(id="yield", description="The yield of the product"),
    ],
    examples=[
        (
            "3,7:6,10-Dianhydro-12-O-[tert-butyl(diphenyl)silyl]-2,5,8,11-tetradeoxy-8-methyl-L-arabino-L-galacto-dodecofuranose (42): \
            To a stirred solution of S4 (mixture of tautomers, 148mg, 0.540mmol, 1.0 equiv) in CH2Cl2 (5 mL) at 0 °C were added imidazole \
            and TBDPSCl. The resulting mixture was allowed to warm to 23°C and \
            stirred for 3h before it was quenched by the addition of sat. aq. NaHCO3 solution (10mL). Flash column chromatography (SiO2, hexanes/EtOAc 10:1, v/v → 1:1, v/v) of the \
            residue afforded 42/43 (mixture of tautomers, 255 mg, 0.497 mmol, 92% yield) as a colorless oil.",
            [
                {
                    "name": "3,7:6,10-Dianhydro-12-O-[tert-butyl(diphenyl)silyl]-2,5,8,11-tetradeoxy-8-methyl-L-arabino-L-galacto-dodecofuranose (42)",
                    "reference_num": "42",
                    "mass": "255 mg",
                    "yield": "92%",
                }
            ],
        ),
        (
            "Tert-butyl (2S,4S)-2-[5-(2-{(2S,4S)-1-[N-(methoxycarbonyl)-L-valyl]-4-methylpyrrolidin-2-yl}-1,11-dihydroisochromeno[4',3':6,7]naphtho[1,2-d]imidazol-9-yl)-1H-imidazol-2-yl]-4-(methoxymethyl)pyrrolidine-1-carboxylate (166 mg, 0.21 mmol) \
            was dissolved in DCM (4 mL), MeOH (1 mL) and HCl (4 M in dioxane, 1 mL) was added. \
            The crude residue was treated with (R)-2-(methoxycarbonylamino)-2-phenylacetic acid (44 mg, 0.21 mmol), COMU (100 mg, 0.21 mmol) and DMF (5 mL). \
            After 1 h, the mixture was diluted with 10% MeOH/EtOAc and washed successively with saturated aqueous NaHCO3 and brine.\
            The crude residue was purified by HPLC to afford \
            methyl {(1R)-2-[(2S,4S)-2-(5-{2-[(2S,4S)-1-{(2S)-2-[(methoxycarbonyl)amino]-3-methylbutanoyl}-4-methylpyrrolidin-2-yl]-1,11-dihydroisochromeno[4',3': 6,7]naphtho[1,2-d]imidazol-9-yl}-1H-imidazol-2-yl)-4-(methoxymethyl)pyrrolidin-1-yl]-2-oxo-1-phenylethyl}carbamate (C16-epi-47) (71 mg, 38%).",
            [
                {
                    "name": "methyl {(1R)-2-[(2S,4S)-2-(5-{2-[(2S,4S)-1-{(2S)-2-[(methoxycarbonyl)amino]-3-methylbutanoyl}-4-methylpyrrolidin-2-yl]-1,11-dihydroisochromeno[4',3': 6,7]naphtho[1,2-d]imidazol-9-yl}-1H-imidazol-2-yl)-4-(methoxymethyl)pyrrolidin-1-yl]-2-oxo-1-phenylethyl}carbamate",
                    "reference_num": "C16-epi-47",
                    "mass": "71 mg",
                    "yield": "38%",
                },
            ],
        ),
        (
            "PL 137,526 describes the hydrogenation of p-tert-butylphenol to form p-tert-butylcyclohexanol using a nickel catalyst. ",
            [{"name": "p-tert-butylcyclohexanol"}],
        ),
    ],
    many=True,
)

reaction = Object(
    # 'id' defines what will appear in the output.
    id="reaction",
    # Natural language description about the object, helping LLM understand what info to collect
    description="the reaction taking place during the reaction setup",
    # Fields to capture fro m a piece of text about the object
    attributes=[
        Text(id="action", description="The action that the experimentalist took"),
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
            "Heat at 35° C. for 24 hours.",
            [
                {
                    "description": "Heat at 35° C. for 24 hours.",
                    "action": "Heat",
                    "time": "24 hours",
                    "temperature": "35° C",
                },
            ],
        ),
        (
            "The reaction mixture was stirred at ambient temperature for 0.5 hours and then treated \
            with a solution of 3-aminopyridine (2.00 g, 21.1 mmol) and triethylamine (4.4 mL, 31.6 mmol) \
            in CH2C12 (20 mL) via canula. The reaction mixture was stirred at ambient temperature for an additional 1.5 hours",
            [
                {
                    "description": "The reaction mixture was stirred at ambient temperature for 0.5 hours and then treated with a solution of 3-aminopyridine (2.00 g, 21.1 mmol) and triethylamine (4.4 mL, 31.6 mmol) in CH2C12 (20 mL) via canula.",
                    "action": "stirred",
                    "time": "0.5 hours",
                    "temperature": "ambient temperature",
                },
                {
                    "description": "The reaction mixture was stirred at ambient temperature for 0.5 hours and then treated with a solution of 3-aminopyridine (2.00 g, 21.1 mmol) and triethylamine (4.4 mL, 31.6 mmol) in CH2C12 (20 mL) via canula.",
                    "action": "treated",
                    "time": "0.5 hours",
                    "temperature": "ambient temperature",
                    "solvents": [
                        {"name": "3-aminopyridine", "mass": "2.00 g", "moles": "21.1 mmol"},
                        {"name": "triethylamine", "volume": "4.4 mL", "moles": "31.6 mmol"},
                        {"name": "CH2C12", "volume": "20 mL"},
                    ],
                },
                {
                    "description": "The reaction mixture was stirred at ambient temperature for an additional 1.5 hours",
                    "action": "stirred",
                    "time": "1.5 hours",
                    "temperature": "ambient temperature",
                },
            ],
        ),
    ],
    many=True,
)

synthesis_step = Object(
    id="steps",
    description="Full step in a chemical procedure",
    attributes=[
        Text(
            id="type",
            description="""Describes what the step entails. The step can vary in length from some words to multiple sentences. It belongs to one of four types:
            - 'set-up': the preparation of a chemical synthesis procedure, where reactants, solvents, and catalysts are specified. Specific conditions in which the reaction is initiated, such as temperature, pressure, atmosphere, are indicated. Chemical treatments may come along to stop the reaction, such as the portionwise addition of acid, base, water or liquid.
            - 'work-up': the process of isolating the desired product from the reaction mixture after the chemical reaction has taken place. It always comes after the completion of reaction-set up in order to separate products from unreacted starting materials, byproducts, and other impurities. Common techniques in work-up includes quenching, extraction, washing, phase separation, evaporation and filtration. Some key words of work-up steps in sentence include 'adding acid (ex. HCL, H2SO4) or base (ex. NaOH) into reaction mixture/residue', 'cooling the mixture to ambient temperature or below 0 degree celsius', 'solvents being removed/filtered/concentrated by rotary evaporation', 'diluting the solution or forming two layers to do extraction'.
            - 'purification': Purification is the process of removing impurities and unwanted byproducts from the desired product to obtain a pure compound. It sometimes comes after the work-up step to obtain a high-quality product with the desired properties. Common purification techniques include crystallization, recrystallization, chromatography, and distillation. 
            - 'analysis': Analysis refers to the characterization and evaluation of the synthesized product to confirm its identity, purity, and properties. This step involves the use of various analytical techniques to determine the product's structure, composition, and physical properties. Common analytical methods include melting point determination, nuclear magnetic resonance (NMR) spectroscopy, infrared spectroscopy (IR), mass spectrometry (MS), Ultraviolet-visible (UV-Vis) spectroscopy, and X-ray crystallography. They often include lists of numbers representing the results of the techniques mentioned.""",
        ),
        Text(id="text", description="Text corresponding to the step."),
        Number(
            id="number",
            description="Number of the current step. The step_num of the current step is always one more than that of the previous step. Numbering starts at 1",
        ),
    ],
    examples=[
        (
            "Methyl {(1R)-2-[(2S,4S)-2-(5-{2-[(2S,4S)-1-{(2S)-2-[(methoxycarbonyl)amino]-3-methylbutanoyl}-4-methylpyrrolidin-2-yl]-1,11-dihydroisochromeno[4',3':6,7]naphtho[1,2-d]imidazol-9-yl}-1H-imidazol-2-yl)-4-(methoxymethyl)pyrrolidin-1-yl]-2-oxo-1-phenylethyl}carbamate: Tert-butyl (2S,4S)-2-[5-(2-{(2S,4S)-1-[N-(methoxycarbonyl)-L-valyl]-4-methylpyrrolidin-2-yl}-1,11-dihydroisochromeno[4',3':6,7]naphtho[1,2-d]imidazol-9-yl)-1H-imidazol-2-yl]-4-(methoxymethyl)pyrrolidine-1-carboxylate (166 mg, 0.21 mmol) was dissolved in DCM (4 mL), MeOH (1 mL) and HCl (4 M in dioxane, 1 mL) was added. The reaction mixture was stirred for 2 h and then concentrated under reduced pressure. The crude residue was treated with (R)-2-(methoxycarbonylamino)-2-phenylacetic acid (44 mg, 0.21 mmol), COMU (100 mg, 0.21 mmol) and DMF (5 mL), then DIPEA (0.18 mL, 1.05 mmol) was added dropwise. After 1 h, the mixture was diluted with 10% MeOH/EtOAc and washed successively with saturated aqueous NaHCO3 and brine. The organics were dried over MgSO4, filtered and concentrated under reduced pressure. The crude residue was purified by HPLC to afford title compound (71 mg, 38%). LCMS-ESI+: calculated for C49H54N8O8: 882.41; observed [M+1]+: 884.34. 1H NMR (CD3OD): 8.462 (s, 1H), 8.029-7.471 (m, 7H), 7.394-7.343 (m, 5H), 5.410 (d, 2H, J=6.8 Hz), 5.300 (m, 1H), 5.233 (m, 2H), 4.341 (m, 1H), 4.236 (d, 1H, J=7.2 Hz), 3.603 (s, 3H), 3.551 (s, 3H), 3.522-3.241 (m, 8H), 2.650 (m, 1H), 2.550 (m, 2H), 1.977-1.926 (m, 4H), 1.221 (d, 3H, J=3.2 Hz), 0.897-0.779 (dd, 6H, J=19.2, 6.8 Hz)",
            [
                {
                    "type": "set-up",
                    "text": "Tert-butyl (2S,4S)-2-[5-(2-{(2S,4S)-1-[N-(methoxycarbonyl)-L-valyl]-4-methylpyrrolidin-2-yl}-1,11-dihydroisochromeno[4',3':6,7]naphtho[1,2-d]imidazol-9-yl)-1H-imidazol-2-yl]-4-(methoxymethyl)pyrrolidine-1-carboxylate (166 mg, 0.21 mmol) was dissolved in DCM (4 mL), MeOH (1 mL) and HCl (4 M in dioxane, 1 mL) was added. The reaction mixture was stirred for 2 h and then concentrated under reduced pressure. The crude residue was treated with (R)-2-(methoxycarbonylamino)-2-phenylacetic acid (44 mg, 0.21 mmol), COMU (100 mg, 0.21 mmol) and DMF (5 mL), then DIPEA (0.18 mL, 1.05 mmol) was added dropwise.",
                    "number": 1,
                },
                {
                    "type": "work-up",
                    "text": "After 10 hours, the mixture was diluted with 10% MeOH/EtOAc and washed successively with saturated aqueous NaHCO3 and brine. The organics were dried over MgSO4, filtered and concentrated under reduced pressure.",
                    "number": 2,
                },
                {
                    "type": "purification",
                    "text": "The crude residue was purified by HPLC to afford title compound (71 mg, 38%).",
                    "number": 3,
                },
                {
                    "type": "analysis",
                    "text": "LCMS-ESI+: calculated for C49H54N8O8: 882.41; observed [M+1]+: 884.34. 1H NMR (CD3OD): 8.462 (s, 1H), 8.029-7.471 (m, 7H), 7.394-7.343 (m, 5H), 5.410 (d, 2H, J=6.8 Hz), 5.300 (m, 1H), 5.233 (m, 2H), 4.341 (m, 1H), 4.236 (d, 1H, J=7.2 Hz), 3.603 (s, 3H), 3.551 (s, 3H), 3.522-3.241 (m, 8H), 2.650 (m, 1H), 2.550 (m, 2H), 1.977-1.926 (m, 4H), 1.221 (d, 3H, J=3.2 Hz), 0.897-0.779 (dd, 6H, J=19.2, 6.8 Hz).",
                    "number": 4,
                },
            ],
        )
    ],
    many=True,
)

set_up_step = Object(
    id="steps",
    description="Set-up step in a chemical procedure",
    attributes=[
        Text(
            id="type",
            description="""A step can vary in length from some words to multiple sentences and it belongs to one of four types:
            - 'set-up': the preparation of a chemical synthesis procedure, where reactants, solvents, and catalysts are specified. Specific conditions in which the reaction is initiated, such as temperature, pressure, atmosphere, are indicated. Chemical treatments may come along to stop the reaction, such as the portionwise addition of acid, base, water or liquid.
            - 'work-up': the process of isolating the desired product from the reaction mixture after the chemical reaction has taken place.
            - 'purification': removing impurities and unwanted byproducts from the desired product to obtain a pure compound.
            - 'analysis': characterization and evaluation of the synthesized product to confirm its identity, purity, and properties.
            You should only extract steps that fall in the 'set-up' category and ignore the rest.
            """,
        ),
        Text(id="text", description="Text corresponding to the step."),
    ],
    examples=[
        (
            "Methyl {(1R)-2-[(2S,4S)-2-(5-{2-[(2S,4S)-1-{(2S)-2-[(methoxycarbonyl)amino]-3-methylbutanoyl}-4-methylpyrrolidin-2-yl]-1,11-dihydroisochromeno[4',3':6,7]naphtho[1,2-d]imidazol-9-yl}-1H-imidazol-2-yl)-4-(methoxymethyl)pyrrolidin-1-yl]-2-oxo-1-phenylethyl}carbamate: Tert-butyl (2S,4S)-2-[5-(2-{(2S,4S)-1-[N-(methoxycarbonyl)-L-valyl]-4-methylpyrrolidin-2-yl}-1,11-dihydroisochromeno[4',3':6,7]naphtho[1,2-d]imidazol-9-yl)-1H-imidazol-2-yl]-4-(methoxymethyl)pyrrolidine-1-carboxylate (166 mg, 0.21 mmol) was dissolved in DCM (4 mL), MeOH (1 mL) and HCl (4 M in dioxane, 1 mL) was added. The reaction mixture was stirred for 2 h and then concentrated under reduced pressure. The crude residue was treated with (R)-2-(methoxycarbonylamino)-2-phenylacetic acid (44 mg, 0.21 mmol), COMU (100 mg, 0.21 mmol) and DMF (5 mL), then DIPEA (0.18 mL, 1.05 mmol) was added dropwise. After 1 h, the mixture was diluted with 10% MeOH/EtOAc and washed successively with saturated aqueous NaHCO3 and brine. The organics were dried over MgSO4, filtered and concentrated under reduced pressure. The crude residue was purified by HPLC to afford title compound (71 mg, 38%). LCMS-ESI+: calculated for C49H54N8O8: 882.41; observed [M+1]+: 884.34. 1H NMR (CD3OD): 8.462 (s, 1H), 8.029-7.471 (m, 7H), 7.394-7.343 (m, 5H), 5.410 (d, 2H, J=6.8 Hz), 5.300 (m, 1H), 5.233 (m, 2H), 4.341 (m, 1H), 4.236 (d, 1H, J=7.2 Hz), 3.603 (s, 3H), 3.551 (s, 3H), 3.522-3.241 (m, 8H), 2.650 (m, 1H), 2.550 (m, 2H), 1.977-1.926 (m, 4H), 1.221 (d, 3H, J=3.2 Hz), 0.897-0.779 (dd, 6H, J=19.2, 6.8 Hz)",
            [
                {
                    "type": "set-up",
                    "text": "Tert-butyl (2S,4S)-2-[5-(2-{(2S,4S)-1-[N-(methoxycarbonyl)-L-valyl]-4-methylpyrrolidin-2-yl}-1,11-dihydroisochromeno[4',3':6,7]naphtho[1,2-d]imidazol-9-yl)-1H-imidazol-2-yl]-4-(methoxymethyl)pyrrolidine-1-carboxylate (166 mg, 0.21 mmol) was dissolved in DCM (4 mL), MeOH (1 mL) and HCl (4 M in dioxane, 1 mL) was added. The reaction mixture was stirred for 2 h and then concentrated under reduced pressure. The crude residue was treated with (R)-2-(methoxycarbonylamino)-2-phenylacetic acid (44 mg, 0.21 mmol), COMU (100 mg, 0.21 mmol) and DMF (5 mL), then DIPEA (0.18 mL, 1.05 mmol) was added dropwise.",
                },
            ],
        )
    ],
    many=True,
)


reaction_schema = Object(
    id="rxn_schema",
    description="Complete summary of a chemical procedure divided into steps",
    attributes=[product, synthesis_step],
    examples=[
        (
            "3,7:6,10-Dianhydro-12-O-[tert-butyl(diphenyl)silyl]-2,5,8,11-tetradeoxy-8-methyl-L-arabino-L- galacto-dodecofuranose (42): To a stirred solution of S4 (148mg, 0.540mmol) in CH2Cl2 (5 mL) at 0 °C were added imidazole (73.5 mg, 1.08 mmol) and TBDPSCl (178mg, 0.648mmol). The resulting mixture was allowed to warm to 23°C and stirred for 3h before it was quenched by the addition of sat. aq. NaHCO3 solution (10mL). The layers were separated, and the aqueous layer was extracted with CH2Cl2 (3×30mL). The combined organic layers were washed with brine (15mL), dried over Na2SO4, filtered, and concentrated under reduced pressure. Flash column chromatography (SiO2, hexanes/EtOAc 10:1, v/v → 1:1, v/v) of the residue afforded 42/43 (mixture of tautomers, 255 mg, 0.497 mmol, 92% yield) as a colorless oil. Rf = 0.40 (SiO2, hexanes/EtOAc 5:1, v/v); FT-IR (film) νmax = 3293, 2931, 2859, 1495, 1454, 1361, 1091, 735 cm−1; 1H NMR (mixture of isomers, 600 MHz, CDCl3) δ = 7.36–7.33 (m, 4 H), 7.31–7.26 (m, 1 H), 4.51 (s, 2 H), 4.26 (dt, J = 6.2, 2.8 Hz, 0.53 H), 4.16 (dt, J = 6.2, 3.1 Hz, 0.45 H)",
            [
                {
                    "products": [
                        {
                            "name": "3,7:6,10-Dianhydro-12-O-[tert-butyl(diphenyl)silyl]-2,5,8,11-tetradeoxy-8-methyl-L-arabino-L-galacto-dodecofuranose (42)",
                            "reference_num": "42",
                            "mass": "255 mg",
                            "yield": "92%",
                        }
                    ],
                    "steps": [
                        {
                            "type": "set-up",
                            "text": "To a stirred solution of S4 (148mg, 0.540mmol) in CH2Cl2 (5 mL) at 0 °C were added imidazole (73.5 mg, 1.08 mmol) and TBDPSCl (178mg, 0.648mmol). The resulting mixture was allowed to warm to 23°C and stirred for 3h before it was quenched by the addition of sat. aq. NaHCO3 solution (10mL).",
                            "number": 1,
                        },
                        {
                            "type": "work-up",
                            "text": "The layers were separated, and the aqueous layer was extracted with CH2Cl2 (3×30mL). The combined organic layers were washed with brine (15mL), dried over Na2SO4, filtered, and concentrated under reduced pressure.",
                            "number": 2,
                        },
                        {
                            "type": "purification",
                            "text": "Flash column chromatography (SiO2, hexanes/EtOAc 10:1, v/v → 1:1, v/v) of the residue afforded 42/43 (mixture of tautomers, 255 mg, 0.497 mmol, 92% yield) as a colorless oil.",
                            "number": 3,
                        },
                        {
                            "type": "analysis",
                            "text": " Rf = 0.40 (SiO2, hexanes/EtOAc 5:1, v/v); FT-IR (film) νmax = 3293, 2931, 2859, 1495, 1454, 1361, 1091, 735 cm−1; 1H NMR (mixture of isomers, 600 MHz, CDCl3) δ = 7.36–7.33 (m, 4 H), 7.31–7.26 (m, 1 H), 4.51 (s, 2 H), 4.26 (dt, J = 6.2, 2.8 Hz, 0.53 H), 4.16 (dt, J = 6.2, 3.1 Hz, 0.45 H)",
                            "number": 4,
                        },
                    ],
                }
            ],
        )
    ],
    many=True,
)


chain_reaction_schema = create_extraction_chain(
    llm_gpt4, reaction_schema, encoder_or_encoder_class="json"
)
