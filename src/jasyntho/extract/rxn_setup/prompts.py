"""Define prompt templates for LLM extraction chains."""

from langchain.prompts import ChatPromptTemplate
from langchain.prompts import HumanMessagePromptTemplate, \
    SystemMessagePromptTemplate


sys_msg = SystemMessagePromptTemplate.from_template(
    "You are a data extractor. "
    "Your priority is to produce data in the requested format."
)

# Prompts for first step: extract identity of products
prop_ptpl = (
    "You get excerpts of a synthesis procedure of products {products}. \n"
    "Your task is to report the properties {properties} as a dictionary "
    '{{"product_label":{{"property_name": "property_value"}} }}\n'
    "Make sure to output something for all products {products}. "
    'Give data in the format "value units"'
    "Input: \n{segments}\n\n"
    "Output:"
)

prop_extr_ptpl = ChatPromptTemplate.from_messages(
    [
        sys_msg,
        HumanMessagePromptTemplate.from_template(prop_ptpl),
    ]
)


# Prompts for second step: extract children of products
synth_ptpl = (
    "Your priority is to provide a correct and parsable output.\n"
    "I give you a paragraph describing the synthesis of a product. "
    "Your task is to extract the reactants used and properties.\n"
    "Give the output in a dictionary with the format "
    "[{{'reference_key', 'substance_name', 'role'}}]. "
    "'role' must be one of ['reactant', 'solvent', 'work-up']\n"
    "'workup' is reserved for any substances that are used "
    "in following steps after the reaction.\n"
    "'reference_key' is a key to another substance the paragraph describes. "
    "Examples can be: S1, 22, 14a. If not given, use the same as 'name'.\n"
    ""
    "Input: \n{paragraph}\n\n"
    "Output: "
)

child_extr_ptpl = ChatPromptTemplate.from_messages(
    [
        sys_msg,
        HumanMessagePromptTemplate.from_template(synth_ptpl),
    ]
)
