"""Segment a synthethic procedure paragraph into semantically distinct pieces using Language Models. This facilitates subsequent parsing"""

import json
import os
import re
from time import time
from typing import List, Optional

from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI

from .llms import *
from .llms.prompts import human_example


class Segmentor:
    """
    Segment a synthesis paragraph semantically.
    Initializes pretrained LLMs for segmentation.
    """

    def __init__(self, llm: str, api_key: Optional[str] = None) -> None:
        """
        Input
        _____
        llm : str
            reference to the LLM used for segmentation.
            One of 'gpt4', 'gpt35', 'claude', 'flant5'
        """
        self.llm = self._init_llm(llm, api_key)

    def syn2segment(self, paragraph: str) -> List[dict]:
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

        segmented_paragraph = self.llm.run({"example": human_example, "paragraph": paragraph})

        json_out = self._parse_llm_segm(segmented_paragraph)
        json_out.pop()
        return json_out

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
        return output

    def _init_llm(self, llm: str, api_key: Optional[str] = None) -> LLMChain:
        """
        Initialize a model for segmentation.
        Input
        _____
        llm : str
            LLM to use for segmentation.
        """
        if api_key is None:
            pass
        else:
            if llm == "gpt4":
                return gpt4_segment(api_key)
            elif llm == "gpt35":
                return gpt35_segment(api_key)
            elif llm == "claude":
                return claude_segment(api_key)
            elif llm == "flant5":
                return flant5_segment()

        return None
