"""
Analysis extraction schema built by Kor API
"""

from kor.extraction import create_extraction_chain
from kor.nodes import Object, Text, Number

from .utils import *
from segment.gpt import llm


nmr_data = Object(

    id = 'nmr_data',
    description = 'nmr analytical data',

    attributes =[
        Text(
            id = 'value',
            description = 'the exact value of NMR data'
        ),
        Text(
            id = 'range',
            description = 'the range of the value of NMR data'
        ),
        Text(
            id = 'multiplicity',
            description = (
            'the value telling how many hydrogen atoms are immediately next door to the hydrogens producing that peak'
            '"s" stands for "singlet", "d" stands for "doublet", "t" stands for "triplet", "q" stands for quartet, and "m" stands for "multiplet"'
            )
        ),
        Text(
            id = 'protons',
            description = 'the location of the proton'
        ),
        Text(
            id = 'j_constant',
            description = 'the coupling constant (aka J constant) of splitting, which is the spacing between the peaks when two protons couple to each other'
        ),
        Text(
            id = 'group',
            description = 'the group specified in the text '
        ),
    ],
    examples =[
        (
            "1H NMR (CD3OD): 8.462 (s, 1H), 8.029-7.471 (m, 7H), \
            7.394-7.343 (m, 5H), 5.410 (d, 2H, J=6.8 Hz), 5.300 (m, 1H), 5.233 (m, 2H), 4.341 (m, 1H), 4.236 (d, 1H, J=7.2 Hz), \
            3.603 (s, 3H), 3.551 (s, 3H), 3.522-3.241 (m, 8H), 2.650 (m, 1H), 2.550 (m, 2H), 1.977-1.926 (m, 4H), 1.221 (d, 3H, J=3.2 Hz), \
            0.897-0.779 (dd, 6H, J=19.2, 6.8 Hz).",
            [
                {
                "value": "8.462",
                "multiplicity": "s",
                "protons": "1H"
                },
                {
                "range": "8.029-7.471",
                "multiplicity": "m",
                "protons": "7H"
                },
                {
                "range": "7.394-7.343",
                "multiplicity": "m",
                "protons": "5H"
                },
                {
                "value": "5.410",
                "multiplicity": "d",
                "protons": "2H",
                "j_constant": "6.8 Hz"
                },
                {
                "value": "5.300",
                "multiplicity": "m",
                "protons": "1H"
                },
                {
                "value": "5.233",
                "multiplicity": "m",
                "protons": "2H"
                },
                {
                "value": "4.341",
                "multiplicity": "m",
                "protons": "1H"
                },
                {
                "value": "4.236",
                "multiplicity": "d",
                "protons": "1H",
                "j_constant": "7.2 Hz"
                },
                {
                "value": "3.603",
                "multiplicity": "s",
                "protons": "3H"
                },
                {
                "value": "3.551",
                "multiplicity": "s",
                "protons": "3H"
                },
                {
                "range": "3.522-3.241",
                "multiplicity": "m",
                "protons": "8H"
                },
                {
                "value": "2.650",
                "multiplicity": "m",
                "protons": "1H"
                },
                {
                "value": "2.550",
                "multiplicity": "m",
                "protons": "2H"
                },
                {
                "range": "1.977-1.926",
                "multiplicity": "m",
                "protons": "4H"
                },
                {
                "value": "1.221",
                "multiplicity": "d",
                "protons": "3H",
                "J": "3.2 Hz"
                },
                {
                "range": "0.897-0.779",
                "multiplicity": "dd",
                "protons": "6H",
                "j_constant": ["19.2 Hz", "6.8 Hz"]
                }
            ],
        )
    ],
    many=True,
)

nmr = Object(

    id = 'nmr',
    description = 'nuclear magnetic resonance method determining the content and purity of a sample ',

    attributes =[
        Text(
            id = 'name',
            description = 'the name of the method'
        ),
        Text(
            id = 'solvent',
            description = 'the solvent in which the NMR is undergone'
        ),
        nmr_data
    ],

    examples =[
        (
            "1H-NMR (DMSO-d6) δ: 12.6 (brs, 1H, CO2H), 8.04 (br s, 3H, NH3−), 6.10 (dt, J=5.6, 2.0, 2.0 Hz, 1H, vinyl), \
            5.85 (dt, J=5.3, 2.3, 2.3 Hz, 1H, vinyl), 4.19 (br s, w½=20 Hz, 1H, allytic H), 3.61 (m, w½=22 Hz, 1H, altylic H), \
            2.53 (quintet, J=5.3 Hz (overlapping with DMSO peak), ½CH2), 2.39 (s, 3H), CH3SO3H), \
            1.93 (dt, J=6.7, 6.7, 13.7 Hz, 1H, ½CH2); [α]20589-83.8°, [α]20578-87.4°, [α]20546-101.2°, [α]20436-186.7°, \
            [α]20365-316.2° (c=1.42, methanol); CI-MS (CH4): 128(M+1); EI-MS; 127(M).",

            [
                {
                    "name": "1H-NMR",
                    "solvent": "DMSO-d6",
                    "nmr_data": [
                        {
                        "value": "12.6",
                        "multiplicity": "brs",
                        "protons": "1H",
                        "group": "CO2H"
                        },

                        {
                        "value": "8.04",
                        "multiplicity": "brs",
                        "protons": "3H",
                        "group": "NH3−"
                        },

                        {
                        "value": "6.10",
                        "multiplicity": "dt",
                        "protons": "1H",
                        "j_constant": ["5.6 Hz", "2.0 Hz", "2.0 Hz"],
                        "group": "vinyl"
                        },

                        {
                        "value": "5.85",
                        "multiplicity": "dt",
                        "protons": "1H",
                        "j_constant": ["5.3 Hz", "2.3 Hz", "2.3 Hz"],
                        "group": "vinyl"
                        },

                        {
                        "value": "4.19",
                        "multiplicity": "brs",
                        "protons": "1H",
                        "group": "allytic H"
                        },

                        {
                        "value": "3.61",
                        "multiplicity": "m",
                        "protons": "1H",
                        "group": "allytic H"
                        },

                        {
                        "value": "2.53",
                        "multiplicity": "quintet",
                        "j_constant": "5.3 Hz (overlapping with DMSO peak)",
                        "group": "½CH2"
                        },

                        {
                        "value": "2.39",
                        "multiplicity": "s",
                        "protons": "3H",
                        "group": "CH3SO3H"
                        },

                        {
                        "value": "1.93",
                        "multiplicity": "dt",
                        "protons": "1H",
                        "j_constant": ["6.7 Hz", "6.7 Hz", "13.7 Hz"],
                        "group": "½CH2"
                        }
                    ]
                },
            ],
        ),
    ],
    many=True,
)

ms = Object(

    id = 'ms',
    description = 'mass spectrometry method analyzing the mass-to-charge ratio of one or more molecules present in a sample.',

    attributes =[
        Text(
            id = 'name',
            description = 'the name of the method'
        ),
        Text(
            id = 'type',
            description = (
            'the type of the mass spectrometry method used in this analytical step'
            '"CI" stands for "chemical ionization", "EI" stands for "electron ionization", "HR" stands for "high resolution"'
            '"CE" stands for "capillary electrophoresis", "LC" stands for "liquid chromatography", "ICP" stands for "Inductively coupled plasma"'
            '"ESI" stands for electrospray ionization, "ES+/ESI+" stands for positive electrospray ionisation'
            )
        ),
        Text(
            id = 'reagent_gas',
            description = 'the reagent gas of the method; it can be "hydrogen (H2)", "methane (CH4)", "isobutane (iso-C4H10)" and "ammonia (NH3)"'
        ),
        Text(
            id = 'value',
            description = 'the mass-to-charge (m/e, m/z) ratio'
        )
    ],

    examples =[
        (
            "Dry the organic layer over (Na2SO4), filter, evaporate the filtrate in vacuo and purify by vacuum distillation \
            to give 2-methyl-2-phenyl-propionic acid, N-methoxy-N-methylamide (18.0 g, 95%); bp 91-103° C./5 mm Hg. \
            MS (CI, CH4) m/e 208 (M++1, 100), 119. ",

            [
                {
                    "name": "MS",
                    "type": "CI",
                    "reagent_gas": "CH4",
                    "value": ["208 (M++1, 100)", "119"]
                },
            ],
        ),
        (
            "The residue was purified by preparative HPLC (gradient, 10-90% acetonitrile/water+0.1% trifluoroacetic acid, \
            15 min run) to furnish the title compound. MS (ES+) m/e 475 [M+H]+, 493",
            [
                {
                    "name": "MS",
                    "type": "ES+",
                    "value": ["475 [M+H]+", "493"]
                },
            ],
        )
    ],
    many=True,

)

bp_data = Object(

    id = 'bp_data',
    description = 'the boiling point of the product',

    attributes =[
        Text(
            id = 'boiling_point',
            description = 'the boiling point of the product'
        ),
        Text(
            id = 'pressure',
            description = 'the pressure under which the boiling point is measured'
        ),
    ],

    examples =[
        (
            "Dissolve 2-methyl-2-phenyl-propionic acid (15.0 g, 91.2 mmol) in toluene (80 mL) and add,\
            by dropwise addition over 5 minutes, thionyl chloride (15 mL, 206 mmol). Stir at room temperature \
            overnight, add additional thionyl chloride (3 mL, 41.1 mmol) and heat to reflux for 1 hour. Remove \
            excess thionyl chloride by azeotropic distillation with toluene (40 mL). Add toluene (20 mL) to the \
            reaction mixture along with a solution of potassium carbonate (28.0 g, 203 mmol) in water (40 mL). \
            Add, by dropwise addition, a solution of N,O-dimethylhydroxylamine hydrochloride (8.9 g, 91.2 mmol) \
            in water (20 mL) without cooling and stir for 2 hours. Add tert-butylmethyl ether (75 mL) following \
            by slow addition of aqueous HCl (2N, 75 mL) with vigorous stirring. Separate the organic layer and wash \
            with aqueous HCl (2N, 75 mL), saturated sodium hydrogen carbonate (25 mL) and brine (50 mL). Dry the \
            organic layer over (Na2SO4), filter, evaporate the filtrate in vacuo and purify by vacuum distillation \
            to give 2-methyl-2-phenyl-propionic acid, N-methoxy-N-methylamide (18.0 g, 95%); bp 91-103° C./5 mm Hg. \
            MS (CI, CH4) m/e 208 (M++1, 100), 119. ",

            [
                {
                    "boiling point": "91-103° C.",
                    "pressure": "5 mm Hg"
                },
            ],
        )
    ],
    many=True,
)

mp_data = Object(

    id = 'mp_data',
    description = 'the melting point of the product',

    attributes =[
        Text(
            id = 'melting_point',
            description = 'the melting point of the product'
        ),
    ],

    examples =[
        (
            " suspension of 4-chlorobiphenyl (9.43 g, 0.0500 mol), succinic anhydride (5.50 g, 0.0550 mol), and \
            anhydrous aluminum chloride (14.8 g, 0.111 mol) in nitrobenzene (25 mL) at 5° C. under nitrogen was \
            stirred 4 hours, then allowed to warm to room temperature. After 3 days, the mixture was heated at 95° C. \
            to 120° C. for 1 hour, cooled to 5° C., and quenched with a mixture of ice (15 g), water (8 mL), and \
            concentrated hydrochloric acid (HCl) solution (8 mL). Additional water (150 mL) was added, followed by ethyl \
            acetate. The ethyl acetate layer was washed with 0.2 M HCl and extracted with saturated aqueous sodium \
            bicarbonate solution. The bicarbonate layer was rotary evaporated briefly to remove residual ethyl acetate, \
            then acidified by the dropwise addition of concentrated HCl solution. The resulting tan precipitate was filtered \
            off, washed with 0.2 M HCl, and air dried. The solids were dissolved in hot toluene/acetone, and the solution was \
            decolorized with activated carbon, and filtered hot through celite. The filtrate was concentrated, and the resulting\
            crystals were filtered, washed, and dried in vacuo to give 1.96 g of 4-(4′-chloro-biphenyl-4-yl)-4-oxo-butyric acid \
            as pale yellow plates; mp 184-185° C.  ",
            [
                {
                    "melting point": "184-185° C."
                },
            ],
        )
    ],
    many=True,
)

nd30 = Object(

    id = 'nd30',
    description = 'the refractive index of the compound under analytics',

    attributes =[
        Text(
            id = 'nd30',
            description = 'the refractive index of the compound under analytics'
        ),
    ],

    examples =[
        (
            "A mixture containing 12.5 ml. of 2-bromoethanol, 12.9 ml. of ethane sulfonyl chloride and 100 ml. of ether was formed. Then, 14 ml. of triethylamine was added dropwise \
            over a 55 minute period at 5°-10°C. and stirred for 1 hour. The mixture was allowed to come to room temperature and stirred for an additional 15 minutes. \
            To the mixture was added 100 ml. of water, the ether layer was separated, dried over magnesium sulfate and evaporated to yield 17.6 grams of a yellow oil. \
            nD30 1.4760. ",

            [
                {
                    "nD30": "1.4760"
                },
            ],
        )
    ],
    many=True,
)

analysis_schema = Object(
    id = 'properties',
    description = 'analysis in the chemical step',
    attributes=[
        nmr,
        ms,
        bp_data,
        mp_data,
        product,
        nd30
    ],
    many=True,
)

chain_analysis = create_extraction_chain(llm, analysis_schema, encoder_or_encoder_class='json')
