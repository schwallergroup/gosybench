"""Definition of kor schemas for data extraction."""

from kor.nodes import Number, Object, Text

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

set_up_schema = Object(
    id="set_up_schema",
    description="Summary of a set-up step in a chemical procedure",
    attributes=[product, set_up_step],
    examples=[
        (
            "'Methyl (14S)-2-O-acetyl-8,12-anhydro-3,4,6,7,10,13-hexadeoxy-3,7-dimethyl-9-O-(triethylsilyl)-D-lyxo-D-manno-tetradecodialdo-14,11-furanosid-5-ulose (32b): A solution of benzyl ether 39b (2.30 g, 3.88 mmol, 1.0 equiv) and Pd/C (30 wt% Pd/C, 20% loading of 39b, 460 mg) in THF (50 mL) was stirred under a hydrogen atmosphere (1 bar) at 23 °C for 1.5 h. The resulting mixture was ﬁltered through a pad of Celite and the ﬁltrate was concentrated under reduced pressure to give the crude alcohol which was used for the next step without further puriﬁcation. To a stirred solution of the above alcohol in CH2Cl2 (50 mL) were added NaHCO3 (2.28 g, 27.2 mmol, 7.0 equiv) and Dess–Martin periodinane (4.11 g, 9.70 mmol, 2.5 equiv). The resulting mixture was allowed to warm to 23 °C and stirred for 1 h before it was quenched by the addition of sat. aq. NaHCO3 solution (30 mL) and sat. aq. Na2S2O3 solution (50 mL). The layers were separated, and the aqueous layer was extracted with CH2Cl2 (3 × 50 mL). The organic layer was washed with brine (50 mL), dried over Na2SO4, ﬁltered, and concentrated under reduced pressure. Flash column chromatography (SiO2, hexanes/EtOAc 10:1, v/v  →  1:1, v/v) aﬀorded fragment A’ (32b; 1.26 g, 2.52 mmol, 65% yield for the two steps) as a colorless oil. 32b: Rf = 0.50 (SiO2, hexanes/EtOAc 2:1, v/v); [α]D23 = +19.5 (c = 0.62, EtOAc); ",
            [
                {
                    "products": [
                        {
                            "name": "Methyl (14S)-2-O-acetyl-8,12-anhydro-3,4,6,7,10,13-hexadeoxy-3,7-dimethyl-9-O-(triethylsilyl)-D-lyxo-D-manno-tetradecodialdo-14,11-furanosid-5-ulose",
                            "reference_num": "32b",
                            "mass": "1.26 g",
                            "yield": "65%",
                        }
                    ],
                    "steps": [
                        {
                            "type": "set-up",
                            "text": "A solution of benzyl ether 39b (2.30 g, 3.88 mmol, 1.0 equiv) and Pd/C (30 wt% Pd/C, 20% loading of 39b, 460 mg) in THF (50 mL) was stirred under a hydrogen atmosphere (1 bar) at 23 °C for 1.5 h. The resulting mixture was ﬁltered through a pad of Celite and the ﬁltrate was concentrated under reduced pressure to give the crude alcohol which was used for the next step without further puriﬁcation. To a stirred solution of the above alcohol in CH2Cl2 (50 mL) were added NaHCO3 (2.28 g, 27.2 mmol, 7.0 equiv) and Dess–Martin periodinane (4.11 g, 9.70 mmol, 2.5 equiv). The resulting mixture was allowed to warm to 23 °C and stirred for 1 h before it was quenched by the addition of sat. aq. NaHCO3 solution (30 mL) and sat. aq. Na2S2O3 solution (50 mL). The layers were separated, and the aqueous layer was extracted with CH2Cl2 (3 × 50 mL). The organic layer was washed with brine (50 mL), dried over Na2SO4, ﬁltered, and concentrated under reduced pressure.",
                        }
                    ],
                }
            ],
        )
    ],
    many=True,
)
