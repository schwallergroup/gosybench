"""Data extraction from reaction setup text segments"""

import json
import os
from typing import List, Optional

from dotenv import load_dotenv
from kor.extraction import create_extraction_chain
from langchain import PromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI

from .kor_schemas import *
from .prompts import *


class ReactionSetup:
    """Extraction of structured data from reaction-setup snippet."""

    def __init__(self, api_key=None):
        """Initialize LLMChain for data extraction with GPT-4"""

        load_dotenv()
        openai_key = api_key or os.environ.get("OPENAI_API_KEY")

        self.llm = ChatOpenAI(
            model_name="gpt-4",
            temperature=0.1,
            max_tokens=2048,
            request_timeout=3000,
            openai_api_key=openai_key,
        )

    def __call__(self, text: str):
        """Execute the extraction pipeline for a single paragraph."""

        prods_md = self._products_metadata(text)
        full_out = self._reformat_expand(prods_md)
        return full_out

    def _products_metadata(self, text: str) -> dict:
        """Extract metadata for all products described in paragraph.

        Extracts the product list and the set-up step from a chemical synthesis description paragraph.

        Input:
            text : str
                synthesis paragraph
        Output:
            dict: list of products with metadata + reaction set-up
                follows schema:
                    {
                        'products':[{'name', 'reference_num', 'mass', 'yield'}],
                        'steps': [{'type': 'set-up', 'text': '...'}]
                    ]
        """

        chain_set_up_schema = create_extraction_chain(
            self.llm, set_up_schema, encoder_or_encoder_class="json"
        )
        schem_result = chain_set_up_schema.predict_and_parse(text=text)["data"]

        if "set_up_schema" not in schem_result.keys():
            return {}

        for rxn in schem_result["set_up_schema"]:
            if "products" not in rxn.keys():
                rxn["products"] = []

            if "steps" not in rxn.keys():
                rxn["steps"] = []

        return schem_result

    def _reformat_expand(self, prods_md: dict) -> dict:
        """Expand details of reaction set-up step for each product obtained in first step.
        For each product, return a dict:
            {'reference_num', 'compound_name', 'reagents'}
        """

        tree_extract_template = PromptTemplate.from_template(
            template=tree_extract_prompt, template_format="jinja2"
        )

        tree_chain = LLMChain(prompt=tree_extract_template, llm=self.llm)

        llm_out = tree_chain.predict(examples=examples_tree_chain, user_input=str(prods_md))

        return json.loads(llm_out)

    ################## comments


#        # Obtain the schema of the set-up step from the text
#
#        # AB: So they first extract a schema from full paragraph, and then process this object again?
#
#        # Seems like this step:
#        # - gets info about product (name, ref num, mass, yield...)
#        # - extracts the rxn set-up. Is simply a pair "type", "text". "type" is instructed to always be "set-up".
#        # In the examples there is none where multiple set-ups are shown, so no reason to think this case is handled.
#        schema = self._get_paragraph_schema(text)
#        schema_string = str(schema)
#
#        # Convert the schema into an appropriate tree-like dictionary using LLM
#        # AB: Inputs prev object. Outputs recursive sequence of ["ref num", "comp name", "reagents"], where "reagents" is a list of objects of with the same structure.
#        # Some inconsistencies in the examples.
#        json_tree = self.tree_chain.predict(examples=examples_tree_chain, user_input=schema_string)
#        return json.loads(json_tree)
#
