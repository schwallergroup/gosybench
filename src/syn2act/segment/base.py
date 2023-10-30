"""Segment a synthethic procedure paragraph into semantically distinct pieces using Language Models. This facilitates subsequent parsing"""

import json
import os
import re
from time import time
from typing import List, Optional, Union

from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI


class Segmentor:
    """
    Segment a synthesis paragraph semantically.
    Initializes pretrained LLMs for segmentation.
    """

    def __init__(self) -> None:
        """Base class for segmentation of synthetic paragraphs."""
        pass

    def __call__(self, inputs: Union[List, str]) -> List[List]:
        """
        Segment a synthesis paragraph semantically into sequences of
        'reaction set-up', 'workup', 'purification', 'analysis'

        Input
        _____
            paragraph: a string containing synthesis paragraph text

        Output
        ______
            JSON object with ['segment', 'class', 'order'] properties for each segment.
        """

        segm_paragrs = self._run(inputs)
        json_out = [self._parse_llm_segm(p) for p in segm_paragrs]

        return json_out

    def _run(self, inputs: Union[List, str]) -> Union[List, str]:
        """Execute the LLM segmentation"""
        return []

    def _parse_llm_segm(self, llm_output: str) -> List[dict]:
        """
        Parse the output of an LLM for paragraph segmentation into a JSON object.

        Input
        _____
            llm_segm: the (string) output of a segmentation LLM.

        Output
        ______
            JSON object with ['segment', 'class', 'order'] properties for each segment.
        """
        valid_entries = ["text segment", "text class", "explanation", "step order"]

        output = []
        segments = re.split(
            "Step end #", llm_output
        )  # split the paragraph text into segments by step

        for segment in range(len(segments)):
            dict_temp = {}
            sentences = re.split(
                "\n", segments[segment]
            )  # split text segment, text class, explanation and step order

            for j in range(0, len(sentences)):
                item = sentences[j].split(": ")  # split label and its content
                try:
                    if item[0] in valid_entries:  # continue if the label does not exist
                        # save index and value in the dictionary
                        dict_temp[item[0]] = item[1]
                    else:
                        continue
                except:
                    if item[0] == "":  # continue if the label does not exist
                        continue

                    else:
                        dict_temp[item[0]] = item[1]  # save index and value in the dictionary

            output.append(dict_temp)  # save the dictionary into the list

        output.pop()
        return output
