"""Segment a synthethic procedure paragraph into semantically distinct pieces using Language Models. This facilitates subsequent parsing"""

import json
import os
import re
from time import time
from typing import List

from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI

from .llms import *
from .llms.prompts import human_example


class Segmentor:
    """
    Segment a synthesis paragraph semantically.
    Initializes pretrained LLMs for segmentation.

    Attributes
    __________
    """

    def __init__(self, llm: str) -> None:
        """
        Input
        _____
        llm : str
            reference to the LLM used for segmentation.
            One of 'gpt4', 'gpt3.5', 'claude', 'flant5'
        """

        llm_dict = {
            "gpt4": gpt4_segment,
            "gpt35": gpt35_segment,
            "claude": claude_segment,
            "flant5": flant5_segment,
        }

        self.llm = llm_dict[llm]

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

        segmented_paragraph = self.chain.run({"example": human_example, "paragraph": parag})

        paragraph = self._parse_llm_segm(segmented_paragraph)
        paragraph.pop()
        return paragraph

    def _parse_llm_segm(self, llm_output: str) -> List[dict]:
        """
        Parse the output of LLMChain for paragraph segmentation into a JSON object.

        Input:
            llm_segm: the output of the segmentation LLM.

        Output:
            a formated JSON object with all information.
        """

        output = []
        segments = re.split(
            "Step end #", llm_segm
        )  # split the paragraph text into segments by step

        for segment in range(0, len(segments)):
            dict_temp = {}
            sentences = re.split(
                "\n", segments[segment]
            )  # split text segment, text class, explanation and step order
            for j in range(0, len(sentences)):
                item = sentences[j].split(": ")  # split label and its content
                #            print('item:', item)
                try:
                    if (
                        item[0] == "text segment"
                        or item[0] == "text class"
                        or item[0] == "explanation"
                        or item[0] == "step order"
                    ):  # continue if the label does not exist
                        dict_temp[item[0]] = item[1]  # save index and value in the dictionary

                    else:
                        continue
                except:
                    if item[0] == "":  # continue if the label does not exist
                        continue

                    else:
                        dict_temp[item[0]] = item[1]  # save index and value in the dictionary

            output.append(dict_temp)  # save the dictionary into the list
        return output
