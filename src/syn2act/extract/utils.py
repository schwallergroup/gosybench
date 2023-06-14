"""
utiliy schema built by Kor API which are multiply used in many schemas
"""

from kor.nodes import Number, Object, Text

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
        Text(id="mass", description="The mass of the product"),
        Text(id="yield", description="The yield of the product"),
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
                {
                    "name": "methyl {(1R)-2-[(2S,4S)-2-(5-{2-[(2S,4S)-1-{(2S)-2-[(methoxycarbonyl)amino]-3-methylbutanoyl}-4-methylpyrrolidin-2-yl]-1,11-dihydroisochromeno[4',3': 6,7]naphtho[1,2-d]imidazol-9-yl}-1H-imidazol-2-yl)-4-(methoxymethyl)pyrrolidin-1-yl]-2-oxo-1-phenylethyl}carbamate",
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
