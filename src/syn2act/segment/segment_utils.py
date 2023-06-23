"""
utilities for segmentation
"""
import json
import re
from time import time

from syn2act.segment.gpt import chain
from syn2act.segment.prompt import example


def syn2segment(parag: str):
    """
    Semantical segmentation of synthesis paragraph into
    ['reaction set-up', 'workup', 'purification', 'analysis']

    Input:
        parag: a string containing synthesis paragraph text

    Output:
        json object with ['segment', 'class', 'order'] properties for each segment.
    """

    segmented_paragraph = chain.run({"example": example, "paragraph": parag})

    paragraph = _parse_llm_segm(segmented_paragraph)
    paragraph.pop()
    return paragraph


def _parse_llm_segm(llm_segm: str):
    """
    Parse the output of LLMChain for paragraph segmentation into a JSON object.

    Input:
        llm_segm: the output of the segmentation LLM.

    Output:
        a formated JSON object with all information.
    """

    output = []
    segments = re.split("Step end #", llm_segm)  # split the paragraph text into segments by step

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
