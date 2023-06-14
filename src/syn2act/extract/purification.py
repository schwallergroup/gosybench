"""
Purification extraction schema built by Kor API
"""

from kor.extraction import create_extraction_chain
from kor.nodes import Object, Text, Number

from .utils import *
from segment.gpt import llm

chromatography = Object(

    id = 'chromatography',
    description = ' chromatography is a laboratory technique for the separation of a mixture into its components.',

    attributes =[
        Text(
            id = 'name',
            description = 'the name of the method'
        ),
        Text(
            id = 'solvent',
            description = (
            'the solvent used in this purification step'
            ''
            )
        )
    ],
    
    examples =[
        (
            "tert-Butanol (2.0 mL, 21.1 mmol) was added to a solution of chlorosulfonyl-isocyanate (1.8 mL, 21.1 mmol) in \
            CH2Cl2 (40 mL).  The reaction mixture was stirred at ambient temperature for 0.5 hours and then treated with a \
            solution of 3-aminopyridine (2.00 g, 21.1 mmol) and triethylamine (4.4 mL, 31.6 mmol) in CH2C12 (20 mL) via canula.\
            The reaction mixture was stirred at ambient temperature for an additional 1.5 hours and then filtered through \
            a 0.25 inch silica gel plug. The solvent was removed under reduced pressure and the residue was purified by \
            flash chromatography on silica gel (elution with EtOAc) to provide 1.17 g of the title compound as a white solid.\
            MS (ESI+) m/z 274 (M+H)+.", 

            [
                {
                    "name": "flash chromatography",
                    "solvent": "silica gel (elution with EtOAc)",
                },
                
            ],
        )
    ],
    many=True,

)

crystallization = Object(

    id = 'crystallization',
    description = ' crystallization is a procedure for purifying an impure compound in a solvent.',

    attributes =[
        Text(
            id = 'name',
            description = 'the name of the method'
        ),
        Text(
            id = 'solvent',
            description = (
            'the solvent used in this purification step'
            ''
            )
        )
    ],
    
    examples =[
        (
            "To a MeOH (3 mL) solution of 4 Å powdered molecular sieves (0.11 g) under argon is added \
            3-amino6,7-dimethoxy-quinoline hydrochloride (0.17 g, 0.68 mmol) and NaOMe (0.039 g, 0.71 mmol). The reaction \
            mixture is stirred at room temperature for 30 min., and cyclohexanone (0.074 mL, 0.71 mmol), \
            then pyridine.borane (0.072 mL, 0.071 mmol) are added portionwise. The mixture is stirred for 4.5 h, \
            then 5N HCl (1.4 mL, 6.8 mmol) is added portionwise. The reaction mixture is stirred 45 min., \
            then made strongly basic with 5N NaOH. The mix is partitioned between EtOAC and H2O, and the aqueous layer is \
            washed with EtOAc (2×). The combined organic layers are washed with brine, (1×), dried (MgSO4), \
            chromatographed (50% EtOAc/hexanes), and recrystallized from EtOAc/hexanes to obtain 0.112 g light-yellow solid \
            in 57% yield (m.p. 164-165). Anal. calcd for C17H22N2O2: C, 71.30; H, 7.74; N, 9.78. Found: C, 71.45; H, 7.49; N, 9.80.", 

            [
                {
                    "name": "recrystallized",
                    "solvent": "EtOAc/hexanes",
                },
                
            ],
        )
    ],
    many=True,

)

purification_schema = Object(
    id = 'properties',
    description = 'purification in a chemical reaction',
    attributes=[
        chromatography,
        crystallization,
        reaction,
        product
    ],
    many=True,
)

chain_purification = create_extraction_chain(llm, purification_schema, encoder_or_encoder_class='json')