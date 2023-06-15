"""
utilities for segmentation
"""
import time
import json
import re

from syn2act.segment.gpt import chain
from syn2act.segment.prompt import example

# segment paragraph texts into
def paragraph2SegmentDict(paragraph):
    """
    paragraph input will be segmented, together with text class, explanation and step order
    """
    output = []
    segments = re.split("Step end #", paragraph)  # split the paragraph text into segments by step

    for segment in range(0, len(segments)):
        dict_temp = {}
        sentences = re.split(
            "\n", segments[segment]
        )  # split text segment, text class, explanation and step order
        for j in range(0, len(sentences)):
            item = sentences[j].split(": ")  # split label and its content
            #            print('item:', item)
            if item[0] == "":  # continue if the label does not exist
                continue
            else:
                dict_temp[item[0]] = item[1]  # save index and value in the dictionary

        output.append(dict_temp)  # save the dictionary into the list
    return output


# print output as csv structure
def printOutput(output):
    """
    Pretty print
    """

    print(json.dumps(output, sort_keys=False, indent=3, ensure_ascii=False))


def paragraph2SegmentJson(text):
    """
    Segment a synthesis description paragraph, using LLMs, into numerous segmented paragraph, together with class, explanation and step order.
    Save these segments into a JSON .
    """

    # step 1
    start_time = time.time()
    segmented_paragraph = chain.run({"example": example, "paragraph": text})
    # print(segmented_paragraph)
    end_time = time.time()
    # print("time: ", end_time - start_time)

    paragraph = paragraph2SegmentDict(segmented_paragraph)
    paragraph.pop()

    printOutput(paragraph)
