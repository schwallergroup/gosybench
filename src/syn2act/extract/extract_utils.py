"""
extract info from segmented text
"""

from .analysis import chain_analysis
from .purification import chain_purification
from .rxn_setup import chain_set_up
from .rxn_workup import chain_work_up
from .utils import chain_reaction_schema, chain_set_up_schema


def get_set_up_summary(text: str):
    """
    Extracts the product list and the set-up step from a chemical synthesis description paragraph.
    Outputs them as a JSON using LLMs

    Args:
        text (str): synthesis paragraph

    Returns:
        dict: dictionary following schema
        {
            'set_up_schema: [
                {
                    'products':
                        [
                            {
                                name,
                                reference_num,
                                mass,
                                yield
                            }

                        ],
                    'steps': [
                        {
                            type: set_up,
                            text
                        }
                    ]
                }
            ]
        }
    """
    set_up_schema = chain_set_up_schema.predict_and_parse(text=text)["data"]

    if "set_up_schema" not in set_up_schema.keys():
        return {}

    for rxn in set_up_schema["set_up_schema"]:
        if "products" not in rxn.keys():
            rxn["products"] = []

        if "steps" not in rxn.keys():
            rxn["steps"] = []

    return set_up_schema


def paragraph2json(text: str):
    """
    Convert a synthesis description paragraph into a JSON using LLMs
    """

    # Get steps and products from paragraph
    synthesis_dict = chain_reaction_schema.predict_and_parse(text=text)["data"]

    if "rxn_schema" not in synthesis_dict.keys():
        return {}

    for rxn in synthesis_dict["rxn_schema"]:
        if "products" not in rxn.keys():
            rxn["products"] = []

        if "steps" not in rxn.keys():
            rxn["steps"] = []

        steps_list = rxn["steps"]

        # Iterate over steps and depending on the type, call appropriate extraction chain for details
        for step in steps_list:
            step_details = ""
            match step["type"]:
                case "set-up":
                    step_details = chain_set_up.predict_and_parse(text=step["text"])["data"]
                case "work-up":
                    step_details = chain_work_up.predict_and_parse(text=step["text"])["data"]
                case "purification":
                    step_details = chain_purification.predict_and_parse(text=step["text"])["data"]
                case "analysis":
                    step_details = chain_analysis.predict_and_parse(text=step["text"])["data"]

            step["details"] = step_details

    return synthesis_dict
