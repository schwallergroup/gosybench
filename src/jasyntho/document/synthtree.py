"""
Define class SynthTree.

tree of SynthNodes that represent the chemical synthesis described in pdf doc.
"""

import asyncio
import json
import logging
import os
import re
from itertools import chain
from typing import Dict, List, Optional, Literal

import fitz  # type: ignore
import networkx as nx  # type: ignore
from colorama import Fore  # type: ignore

import wandb
from jasyntho.extract import ExtractReaction, Product
from jasyntho.extract.extended import LabConnection
from jasyntho.utils import RetrieveName, name_to_smiles

from .base import ResearchDoc
from .si_select import SISplitter
from .synthpar import SynthParagraph
from ..extract.substances import Product
from .parsing import VisionParser

# Silence retry validator warnings
logging.getLogger("instructor").setLevel(logging.CRITICAL)


class SynthTree(ResearchDoc):
    """Extend SISynthesis to represent reaction tree."""

    products: List[Product] = []
    full_g: nx.DiGraph = nx.DiGraph()
    reach_subgraphs: Dict[str, nx.DiGraph] = {}
    rxn_extract: Optional[ExtractReaction] = None
    paragraphs: List[SynthParagraph] = []
    raw_prods: List[Product] = []
    v: bool = True

    def gather_smiles(self):
        """Gather all smiles from the products."""

        G = self.full_g

        iupac = RetrieveName()

        def get_iupac(subs, context):
            try:
                return iupac(subs, context).name
            except Exception as e:
                return []

        def _size_reach_sg(G, node):
            """Calc size of each reachable subgraph."""
            rn = set(nx.bfs_tree(G, node))
            return len(rn)

        for k, g in G.nodes.items():
            l = _size_reach_sg(G, k)
            if l > 1:
                if "attr" not in g.keys():
                    return None

                name = g["attr"]["substance_name"]
                labl = g["attr"]["reference_key"]
                smi = name_to_smiles(name, labl)
                if smi is None:
                    # Try to get iupac name
                    retrieved_names = get_iupac(k, context=g["attr"]["text"])
                    print(f"key {k}. Got iupac name: {retrieved_names}")
                    for n in retrieved_names:
                        smi = name_to_smiles(n, labl)
                        if smi:
                            # Assign iupac and smiles attributes to node
                            g["attr"]["iupac"] = n
                            g["attr"]["smiles"] = smi
                            break
                if smi is not None:
                    g["attr"]["smiles"] = smi

        self.full_g = G
        # TODO try this

    def extended_connections(self):
        """Return the extended connections for a given query."""
        dts = self.partition()
        lab_connect = LabConnection(self)

        new_connects = {}
        for k, g in dts.items():
            if len(g) > 1:
                print(f"Processing reachable subgraph from source node {k}")
                new_connects[k] = lab_connect(k)

        self.reach_subgraphs = self.partition(new_connects)
        return new_connects  # in case we want to use it later

    def partition(self, new_connects: Optional[dict] = None):
        """Merge and find all reachable subgraphs in paper.
        If dict of new connects is given, rewire the graph with new connections.
        """
        prods = self.unique_keys(self.products)
        self.full_g = self.get_full_graph(prods)

        if new_connects is not None:
            self.full_g = self._rewire(self.full_g, new_connects)

        reach_subgraph = SynthTree.get_reach_subgraphs(self.full_g)
        return reach_subgraph

    def _rewire(self, full_graph, new_connects):
        """Rewire the graph with new connections."""
        # add new edges
        for k, res in new_connects.items():
            if res is not None:
                prod_step = res["step 2"]
                if prod_step is not None:
                    prod = prod_step.product.reference_key
                    if prod in full_graph.nodes:
                        if k != prod:
                            full_graph.add_edge(prod, k)
        return full_graph

    @classmethod
    def unique_keys(cls, trees):
        """Return a list of trees with unique IDs.

        For now simply keep a unique one. the first found
        """
        ftrees = {}
        for t in trees:
            if t.reference_key not in ftrees.keys():
                ftrees[t.reference_key] = t
        return list(ftrees.values())

    def get_full_graph(
        self,
        product_list: List[Product],
        children_types: List[str] = ["reactant", "reagent", "catalyst"],
    ):
        """Build a graph using input disconnected nodes."""
        # Directed graph
        Gd = nx.DiGraph()

        # Add each node
        for p in product_list:
            # Add node with properties
            if p.reference_key is not None:
                Gd.add_node(
                    p.reference_key, attr=p.model_dump()  # type: ignore
                )
            else:
                print(f"\t- Error adding node: {p.note}")
            for c in p.children:
                if c.role_in_reaction in children_types:
                    Gd.add_edge(
                        p.reference_key,
                        c.reference_key,
                        attr={"type": "lab reaction"},
                    )
        return Gd

    @classmethod
    def get_reach_subgraphs(cls, Gd: nx.DiGraph) -> Dict[str, nx.DiGraph]:
        """
        Get a list of reachable subgraph from source nodes.

        Find all nodes with indegree==0 (heads) and find subgraph of reachable
        nodes.
        """
        # Get list of heads
        heads = [n for n, indeg in Gd.in_degree() if indeg == 0]

        for h in Gd.nodes:
            if h in heads:
                Gd.nodes[h]["is_head"] = True
            else:
                Gd.nodes[h]["is_head"] = False

        # Extract subgraphs reachable from each head node.
        def extract_subgraph(graph, start_node):
            """Use BFS to find all nodes reachable from start_node."""
            reachable_nodes = set(nx.bfs_tree(graph, start_node))
            return graph.subgraph(reachable_nodes).copy()

        # Store the subgraphs in a list
        subgraphs = {
            node: extract_subgraph(Gd, node)
            for node in Gd
            if Gd.nodes[node]["is_head"]
        }
        return subgraphs

    # Exporting
    def export(self):
        """Export the SynthTree's reachable subgraph from source nodes into JSON."""

        json = {}
        # For each reachable subgraph from source node, serialize it into JSON
        for k, g in self.reach_subgraphs.items():
            smiles = g.nodes[k]["attr"].get("smiles") or k
            json[k] = {
                "smiles": smiles,
                "type": "mol",
                "in_stock": False,
                "children": self.json_serialize(g, key=k),
            }
        return json

    def json_serialize(self, G, key="10"):
        """Serialize a single reachable subgraph from source node into JSON."""
        # TODO finish this -> convert_to_smiles, etc. Add this somewhere else so that this function is simply format translation

        json = {}
        successors = G.successors(key)
        slist = []
        for s in successors:
            props = G.nodes[s]
            if len(list(G.successors(s))) > 0:
                # Get properties of the node
                if "attr" not in props.keys():
                    continue
                name = props["attr"]["substance_name"]
                if "smiles" in props["attr"].keys():
                    smiles = props["attr"]["smiles"]
                else:
                    smiles = name

                # Format json
                slist.append(
                    {
                        "smiles": smiles,
                        "name": name,
                        "type": "mol",
                        "in_stock": False,
                        "children": self.json_serialize(G, key=s),
                    }
                )
            else:
                smiles = s
                slist.append(
                    {
                        "smiles": s,
                        "name": s,
                        "type": "mol",
                        "in_stock": False,
                    }
                )

        final_json = [{"smiles": "", "type": "reaction", "children": slist}]
        return final_json

    def select_syntheses(self) -> None:
        """Select the part of the SI where syntheses are described."""
        si_split = SISplitter()

        si_split.signal_threshold = 0.35
        si_split.window_size = 150
        if self.v:
            si_split.plot = True

        doc = self.from_dir(self.doc_src)
        relevant_si = si_split.select_relevant(doc)
        relev_si_src = os.path.join(self.doc_src, "si_syntheses.pdf")
        relevant_si.save(relev_si_src)

    def extract_rss(self) -> list:
        """Extract reaction setups for each paragraph in the doc."""
        relev_si_src = os.path.join(self.doc_src, "si_syntheses.pdf")
        self.paragraphs = self._get_paragraphs(relev_si_src)

        raw_prodlist = [p.extract(self.rxn_extract) for p in self.paragraphs]
        self.raw_prods = list(chain(*raw_prodlist))  # type: ignore

        self._log_products()
        self._report_process(self.raw_prods)
        products = [p for p in self.raw_prods if not p.isempty()]
        return products

    async def async_extract_rss(self, mode: Literal['text', 'vision']='text') -> list:
        """Extract reaction setups for each paragraph in the doc."""
        relev_si_src = os.path.join(self.doc_src, "si_syntheses.pdf")
        self.paragraphs = await self._get_paragraphs(relev_si_src, mode=mode)

        raw_prodlist = await asyncio.gather(
            *[p.async_extract(self.rxn_extract) for p in self.paragraphs]
        )
        self.raw_prods = list(chain(*raw_prodlist))  # type: ignore

        self._log_products()
        self._report_process(self.raw_prods)
        products = [p for p in self.raw_prods if not p.isempty()]
        return products

    def _log_products(self) -> None:
        """Log the products extracted from the paragraphs."""

        if self.logger:

            def jdump(p):
                return str(
                    json.dumps([c.model_dump() for c in p.children], indent=2)
                )

            table = [
                [p.text, jdump(p), f"{p.reference_key} -- {p.substance_name}"]
                for i, p in enumerate(self.raw_prods)
            ]

            table_wnb = wandb.Table(  # type: ignore
                data=table, columns=["text", "children", "ref_key -- name"]
            )
            self.logger.log({"products": table_wnb})

    def _report_process(self, raw_prods) -> None:
        """Print a report of results of prgr processing."""
        # if not self.v:
        #    return None

        correct = 0
        empty = 0
        notes = []
        for p in raw_prods:
            if p.isempty():
                empty += 1
                notes.append(p.note)
            else:
                correct += 1

        def printm(message):
            """Print report message."""
            print(Fore.LIGHTYELLOW_EX + message + Fore.RESET)

        printm(f"Total paragraphs: {len(self.paragraphs)}")
        printm(f"Processed paragraphs: {correct}")
        printm(f"Found {empty} empty paragraphs.")
        for n in set(notes):
            printm(f"\t{n}: {notes.count(n)}")

    async def _get_paragraphs(self, doc_src: str, mode: Literal['text', 'vision']='text', api_key: Optional[str]=None) -> List[SynthParagraph]:
        """
        Create list of paragraphs from document.

        Input
            doc_src: address of the pdf document.
        """
        if mode=='text':
            fitz_si_syn = fitz.open(doc_src)
            end = fitz_si_syn.page_count

            parags_pages = self._get_pars_per_page(fitz_si_syn, 0, end)
            return self._clean_up_pars(parags_pages)
        if mode=='vision':
            parser = VisionParser(ptype='vision', api_key=api_key)
            return await parser.vision_parse(doc_src, batch_size=5, model='gpt-4o', prgr_sep='##---##')



    def _clean_up_pars(self, pars):
        """Merge and filter out paragraphs."""
        all_paragraphs = []
        new_paragraph = ""

        for par in pars:
            if par[0] == "bold":
                if new_paragraph != "" and not new_paragraph.isspace():
                    all_paragraphs.append(SynthParagraph(new_paragraph))
                new_paragraph = ""
            new_paragraph += par[1]

        return all_paragraphs

    def _get_pars_per_page(self, doc, start, end):
        """Get all paragraphs in this page.

        This is one of these functions you simply don't touch.
        """
        all_paragraphs = []

        # iterate over pages of document
        for i in range(start, end):
            # make a dictionary
            json_data = doc[i].get_text("json")
            json_page = json.loads(json_data)
            page_blocks = json_page["blocks"]

            page_paragraphs = []
            new_paragraph = ""
            bold_txt = ""
            start_bold = False

            for j in range(len(page_blocks)):
                line = page_blocks[j]

                if "lines" in list(line.keys()):
                    for n in line["lines"]:
                        text_boxes = n["spans"]

                        for k in range(len(text_boxes)):
                            font = text_boxes[k]["font"]
                            text = text_boxes[k]["text"].replace("\n", "")
                            # to check if it is a superscript
                            flags = int(text_boxes[k]["flags"])

                            if (
                                not re.search(r"S\d+", text)
                                or (
                                    re.search(r"S\d+", text)
                                    and ("Bold" in font or "bold" in font)
                                )
                                or re.search("[T|t]able", text)
                                or re.search("[F|f]igure", text)
                            ):
                                if flags & 2**0:
                                    text = " " + text

                                if k == (len(text_boxes) - 1) and j == (
                                    len(page_blocks) - 1
                                ):
                                    new_paragraph += text
                                    if start_bold:
                                        page_paragraphs.append(
                                            ["bold", new_paragraph]
                                        )
                                    else:
                                        page_paragraphs.append(
                                            ["plain", new_paragraph]
                                        )
                                    new_paragraph = ""
                                else:
                                    if "Bold" in font or "bold" in font:
                                        bold_txt += text
                                    else:
                                        if len(bold_txt) > 5:
                                            if start_bold:
                                                page_paragraphs.append(
                                                    ["bold", new_paragraph]
                                                )
                                            else:
                                                page_paragraphs.append(
                                                    ["plain", new_paragraph]
                                                )

                                            start_bold = True
                                            new_paragraph = ""
                                            new_paragraph += bold_txt
                                            bold_txt = ""
                                        else:
                                            new_paragraph += bold_txt
                                            bold_txt = ""

                                        if new_paragraph == "":
                                            start_bold = False

                                        new_paragraph += text

            all_paragraphs.extend(page_paragraphs)

        return all_paragraphs
