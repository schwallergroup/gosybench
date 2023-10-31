"""Data extraction from reaction setup text segments"""

import json
import os
import re
import ast
from dotenv import load_dotenv
from langchain import PromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from chemdataextractor import Document
from chemdataextractor.doc import Heading
from .prompts import prop_extr_ptpl, examples_tree_chain, tree_extract_prompt


class ReactionSetup:
    """Extraction of structured data from reaction-setup snippet."""

    def __init__(self, api_key=None):
        """Initialize LLMChain for data extraction with GPT-4"""

        load_dotenv()
        openai_key = api_key or os.environ.get("OPENAI_API_KEY")

        self.props_prod = ['mass', 'yield', 'moles']
        llm = ChatOpenAI(openai_api_key=openai_key)
        self.prod_prop_chain = LLMChain(prompt=prop_extr_ptpl, llm=llm)

        self.llm = ChatOpenAI(
            model_name="gpt-4",
            temperature=0.1,
            max_tokens=2048,
            request_timeout=3000,
            openai_api_key=openai_key,
        )

    def __call__(self, text: str) -> dict:
        """Execute the extraction pipeline for a single paragraph."""
        header, parag = self._split_paragraph(text)
        prods_md = self._products_metadata(header, parag)
        return prods_md
        full_out = self._reformat_expand(prods_md)
        return full_out

    def _products_metadata(self, heading: str, content: str) -> dict:
        """Extract metadata for all products described in paragraph.

        Input:
            heading : str
                heading of paragr, containing the product names and labels
            content : str
                content of paragr, containing the reaction set-up and analysis
        Output:
            dict: list of products with metadata + reaction set-up
                follows schema:
                {
                    'prod_label':
                        {
                            'prod_name': '...',
                            'prod_ref': '...',
                            'mass': '...',
                            'yield': '...',
                            'moles': '...',
                        }
                }
        """
        products = self._extract_prods_header(heading)
        segments = self._filter_sgmnt(content)

        prods_inp = str([p["labels"] for p in products])
        prod_props = self._prod_data_llm(prods_inp, segments)
        merged_data = self._merge_prod_data(products, prod_props)
        return merged_data

    def _split_paragraph(self, text: str) -> tuple:
        try:
            # Find occurence of (ID), where ID is product identifier:
            # any combination of letters and numbers
            match = re.search(
                r'\([A-Za-z\d]+\)\:',
                text
            ).span()  # type: ignore

            header = text[:match[1]]
            parag = text[match[1]:]
        except AttributeError:
            header = ""
            parag = text
        return header, parag

    def _extract_prods_header(self, head):
        prg = Document(Heading(head))
        return prg.records.serialize()

    def _filter_sgmnt(self, prg):
        segments = ""
        for i, m in enumerate(re.finditer(r'yield|\%', prg)):
            s = m.span()
            segments += f"{i+1}. {prg[s[0]-60:s[1]+60]}\n"
        return segments

    def _prod_data_llm(self, products, segments):
        response = self.prod_prop_chain.run(
            products=products, properties=self.props_prod, segments=segments
        )
        prod_props = ast.literal_eval(response)
        return prod_props

    def _merge_prod_data(self, products, prod_props):
        f_data = {}
        for p in products:
            lbl = p['labels'][0]
            try:
                names = p['names']  # assume 'names' exists
            except KeyError:
                names = lbl

            f_data[lbl] = {
                "prod_name": names,
                "prod_ref": lbl,
                **prod_props[lbl]
            }
        return f_data

    def _reformat_expand(self, prods_md: dict) -> dict:
        """Expand details of reaction set-up step for each product
        obtained in first step.
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
