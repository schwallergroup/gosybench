"""Define prompt templates for LLM extraction chains."""

from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)

sys_msg = SystemMessagePromptTemplate.from_template(
    "You are a data extractor. Your priority is to produce data in the " "requested format."
)

# Prompts for first step: extract identity of products
prop_stpl = (
    "You get excerpts of a synthesis procedure of products {products}. \n"
    "Your task is to report the properties {properties} as a dictionary "
    '{{"product_label":{{"property_name": "property_value"}} }}\n'
    "Make sure to output something for all products {products}. "
    'Give data in the format "value units"'
    "Input: \n{segments}\n\n"
    "Output:"
)
properties = str(["mass", "yield", "moles"])

prop_extr_ptpl = ChatPromptTemplate.from_messages(
    [
        sys_msg,
        HumanMessagePromptTemplate.from_template(prop_stpl),
    ],
)

propextr_tpl = prop_extr_ptpl.partial(properties=properties)


# Prompts for second step: extract children of products
synth_stpl = (
    "Your task is to extract data from a provided paragraph and format it "
    "into a JSON dictionary. You should identify the reactants used and their "
    "properties.\n"
    "Format the output as a list of dictionaries, each with the keys: "
    "'reference_key', 'substance_name', and 'role'. \n"
    "The 'role' can be one of ['reactant', 'solvent', 'work-up'], where "
    "'work-up' is for substances used in steps after the main reaction. The "
    "'reference_key' is an identifier for another substance described in the "
    "paragraph, like 22, S1, 14a, etc. If a reference key isn't given, use "
    "the substance's name as the key. Ensure all values are strings and the "
    "output is valid JSON. \n"
    "Example Input: {example_in}\n"
    "Example Output: {example_out}\n\n"
    "Input: {paragraph}\n"
    "Output: "
)

example_in = """To a stirred solution of bromide 14 (0.10 g, 0.27 mmol, 1.0
equiv) in toluene (20 mL) was added n-Bu3SnH (0.11 mL, 0.41 mmol, 1.5 equiv)
followed by AIBN (4.5 mg, 0.027 mmol, 0.1 equiv) in one portion, and the
resulting mixture was heated to 90 °C. After 0.5 h, the reaction mixture was
allowed to cool to 23 °C and the solvent was removed under reduced pressure."""

example_out = [
    {"reference_key": "14", "substance_name": "bromide 14", "role": "reactant"},
    {"reference_key": "toluene", "substance_name": "toluene", "role": "solvent"},
    {"reference_key": "n-Bu3SnH", "substance_name": "n-Bu3SnH", "role": "reactant"},
    {"reference_key": "AIBN", "substance_name": "AIBN", "role": "reactant"},
]

child_extr_ptpl = ChatPromptTemplate.from_messages(
    [
        sys_msg,
        HumanMessagePromptTemplate.from_template(synth_stpl),
    ]
)

childextr_tpl = child_extr_ptpl.partial(example_in=example_in, example_out=str(example_out))
