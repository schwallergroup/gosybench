# extract info from segmented text
import time

from syn2act.segment.gpt import chain
from syn2act.segment.prompt import example
from syn2act.segment.segment_utils import paragraph2SegmentDict

from .analysis import *
from .purification import *
from .rxn_setup import *
from .rxn_workup import *


def paragraph2json(text):
    # step 1
    start_time = time.time()
    segmented_paragraph = chain.run({"example": example, "paragraph": text})
    print(segmented_paragraph)
    end_time = time.time()
    print("time: ", end_time - start_time)

    paragraph = paragraph2SegmentDict(segmented_paragraph)
    paragraph.pop()

    # step 2
    for i in range(len(paragraph)):
        if paragraph[i]["text class"] == "reaction set-up":
            output = chain_object.predict_and_parse(text=(paragraph[i]["text segment"]))["data"]
            print(output, "\n\n")
            # if (output):  # if the Kor-extracted data exist, append the segmented paragraph with the extracted-data
            #     paragraph[i]['properties'] = output['properties']

        elif paragraph[i]["text class"] == "work-up":
            output = chain_work_up.predict_and_parse(text=(paragraph[i]["text segment"]))["data"]
            print(output, "\n\n")
            # if (output):  # if the Kor-extracted data exist, append the segmented paragraph with the extracted-data
            #     paragraph[i]['properties'] = output['properties']

        elif paragraph[i]["text class"] == "purification":
            output = chain_purification.predict_and_parse(text=(paragraph[i]["text segment"]))[
                "data"
            ]
            print(output, "\n\n")
            # if (output):  # if the Kor-extracted data exist, append the segmented paragraph with the extracted-data
            #     paragraph[i]['properties'] = output['properties']

        elif paragraph[i]["text class"] == "analysis":
            output = chain_analysis.predict_and_parse(text=(paragraph[i]["text segment"]))["data"]
            print(output, "\n\n")
            # if (output):  # if the Kor-extracted data exist, append the segmented paragraph with the extracted-data
            #     paragraph[i]['properties'] = output['properties']

    print(paragraph)

    return paragraph
