"""Data extraction from reaction setup text segments"""

import ast
import os
import re
from typing import Union

from chemdataextractor import Document
from chemdataextractor.doc import Heading
from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI

from .prompts import child_extr_ptpl, prop_extr_ptpl


class ReactionSetup:
    """Extraction of structured data from reaction-setup snippet."""

    def __init__(self, api_key=None):
        """Initialize LLMChain for data extraction with GPT-4"""

        load_dotenv()
        openai_key = api_key or os.environ.get("OPENAI_API_KEY")

        self.props_prod = ["mass", "yield", "moles"]
        self.llm = ChatOpenAI(
            openai_api_key=openai_key,
            temperature=0.1,
            max_tokens=512,
            request_timeout=60,  # wait for max 1 min
        )
        self.prod_prop_chain = LLMChain(prompt=prop_extr_ptpl, llm=self.llm)
        self.child_prop_chain = LLMChain(prompt=child_extr_ptpl, llm=self.llm)

    def __call__(self, text: str) -> Union[dict, list]:
        """Execute the extraction pipeline for a single paragraph."""
        header, parag = self._split_paragraph(text)
        prods_md = self._products_metadata(header, parag)
        if len(prods_md) != 0:
            prods_md["procedure"] = text
        else:
            return []

        prods_child = self._reformat_extend(parag)

        # Finally complete prods_md with prods_child
        prod_list = []
        for prod_key, prod_d in prods_md.items():
            print(prod_key)
            if prods_child["status"] == "success":
                prod_d["children"] = prods_child["data"]
            elif len(prods_md.keys()) > 0:
                prod_d["children"] = []
            prod_list.append(prod_d)

        return prod_list

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
                            'substance_name': '...',
                            'reference_key': '...',
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

    def _reformat_extend(self, prg: str) -> dict:
        """Expand details of reaction set-up step for each product
        obtained in first step.
        For each product, return a dict:
            {'reference_key', 'compound_name', 'reagents'}
        """

        # Preprocess paragraph
        prg = prg[:200]  # Simply take 200 first chars: rxn setup

        out_llm = self.child_prop_chain.run(prg)
        try:
            dt = ast.literal_eval(out_llm)
            print(dt)
            # Reformat data {'S1': {'name': ...}}
            # dt_pp = {'reference_key': r['reference_key']: 'name': r['name']} for r in dt}
            data = {"status": "success", "data": dt}
        except SyntaxError:
            data = {"status": "failure", "data": out_llm}

        return data

    def _merge_prod_data(self, products, prod_props):
        """Merge property and product ID dictionaries."""
        f_data = {}
        for p in products:
            lbl = p["labels"][0]
            try:
                names = p["names"]  # assume 'names' exists
            except KeyError:
                names = lbl

            f_data[lbl] = {"substance_name": names, "reference_key": lbl}
            f_data[lbl].update(prod_props[lbl])
        return f_data

    def _split_paragraph(self, text: str) -> tuple:
        """
        Split paragraph into header and content.
        """
        try:
            # Find occurence of (ID), where ID is product identifier:
            # any combination of letters and numbers
            match = re.search(r"\([A-Za-z\d]+\)\:", text)
            sp = match.span()  # type: ignore

            header = text[: sp[1]]
            parag = text[sp[1] :]
        except AttributeError:
            header = ""
            parag = text
        return header, parag

    def _extract_prods_header(self, head):
        """Extract product name and label from header using CDE"""
        prg = Document(Heading(head))
        return prg.records.serialize()

    def _filter_sgmnt(self, prg):
        """Get relevant excerpts from paragraph that may contain
        analytical data from products"""

        segments = ""
        for i, m in enumerate(re.finditer(r"yield|\%", prg)):
            s = m.span()
            segments += f"{i+1}. {prg[s[0]-60:s[1]+60]}\n"
        return segments

    def _prod_data_llm(self, products, segments):
        """Get analytical data for product using LLMs."""
        response = self.prod_prop_chain.run(
            products=products, properties=self.props_prod, segments=segments
        )
        try:
            prod_props = ast.literal_eval(response)
        except SyntaxError:
            prod_props = []
        return prod_props
