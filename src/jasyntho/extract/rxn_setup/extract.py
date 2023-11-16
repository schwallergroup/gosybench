"""Data extraction from reaction setup text segments"""

import ast
import os
import re
from typing import List, Tuple, Union

import instructor  # type: ignore
from chemdataextractor import Document  # type: ignore
from chemdataextractor.doc import Heading  # type: ignore
from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from openai import OpenAI  # type: ignore
from pydantic import ValidationError

from .prompts import propextr_tpl
from .typing import SubstanceList

load_dotenv()


class ReactionSetup:
    """Extraction of structured data from reaction-setup snippet."""

    def __init__(self, api_key=None):
        """Initialize LLMChain for data extraction with GPT-4."""
        load_dotenv()
        openai_key = api_key or os.environ.get("OPENAI_API_KEY")

        llm = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            openai_api_key=openai_key,
            temperature=0.0,
            max_tokens=512,
            request_timeout=60,  # wait for max 1 min
        )

        self.llm = 'gpt-3.5-turbo'
        self.client = instructor.patch(OpenAI())
        self.prod_prop_chain = LLMChain(prompt=propextr_tpl, llm=llm)

    def __call__(self, text: str) -> Union[dict, list]:
        """Execute the extraction pipeline for a single paragraph."""
        try:
            parag, prods_md = self._products_metadata(text)
            prods_child = self._extract_reacts(parag)

            # Finally complete prods_md with prods_child
            prod_list = []
            for prod_key, prod_d in prods_md.items():
                if prods_child["status"] == "success":
                    prod_d["children"] = prods_child["data"]
                elif len(prods_md.keys()) > 0:
                    prod_d["children"] = []
                prod_list.append(prod_d)

            return prod_list
        except ValidationError:
            return []

    def _products_metadata(self, text: str) -> Tuple[str, dict]:
        """Extract metadata for all products described in paragraph.

        Input:
            text : str
                full text of paragr, containing prod name, id, rxn, etc.
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
        header, content = self._split_paragraph(text)
        products = self._extract_prods_header(header)
        segments = self._filter_sgmnt(content)

        prods_inp = str([p["labels"] for p in products])
        prod_props = self._get_prod_data(prods_inp, segments)
        merged_data = self._merge_prod_data(products, prod_props)
        return content, merged_data

    def _extract_reacts(self, prg: str) -> dict:
        """Extract the substances in a reaction."""
        # TODO: this is only a proxy to getting reaction setup.
        prg = prg[:500]

        subs = self.client.chat.completions.create(
            model=self.llm,
            response_model=SubstanceList,
            messages=[
                {"role": "user", "content": prg},
            ],
            temperature=0.2,
            max_retries=2,
        )

        # Wrap into dict with error status
        try:
            subs = self.__clean_synth_dict(subs)
            return {"status": "success", "data": subs}
        except ValidationError:
            return {"status": "failure", "data": None}
        return subs

    def __clean_synth_dict(self, slist: SubstanceList) -> List[dict]:
        """Clean extracted json of paragraph children."""
        # Add keys if None
        for s in slist.substances:
            if s.reference_key is None:
                s.reference_key = s.substance_name

        # keep only 'reactant' and 'solvent'
        new_subs = SubstanceList()
        for h in slist.substances:
            if h.role in ["reactant", "solvent"]:
                new_subs.substances.append(h)

        # Keep only unique keys
        uniq_d = {d.reference_key: d for d in reversed(new_subs.substances)}
        subs = [s.model_dump() for s in uniq_d.values()]  # type: ignore
        return subs

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
        """Split paragraph into header and content."""
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
        """Extract product name and label from header using CDE."""
        prg = Document(Heading(head))
        return prg.records.serialize()

    def _filter_sgmnt(self, prg):
        """Get relevant excerpts from paragraph.

        Return concat excerpts that may contain
        analytical data from products
        """
        segments = ""
        for i, m in enumerate(re.finditer(r"yield|\%", prg)):
            s = m.span()
            segments += f"{i+1}. {prg[s[0]-60:s[1]+60]}\n"
        return segments

    def _get_prod_data(self, products, segments):
        """Get analytical data for product.

        TODO: mod with instructor
        """
        response = self.prod_prop_chain.run(products=products, segments=segments)
        try:
            prod_props = ast.literal_eval(response)
        except SyntaxError:
            prod_props = []
        return prod_props
