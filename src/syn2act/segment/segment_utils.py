import re
import json

# segment paragraph texts into 
def paragraph2SegmentDict (paragraph):
    output = []
    segments = re.split("Step end #",paragraph)   # split the paragraph text into segments by step

    for segment in range(0, len(segments)):
        dict_temp = {}
        sentences = re.split("\n",segments[segment]) # split text egment, text class, explanation and step order 
        for j in range(0, len(sentences)):
            item = sentences[j].split(": ")          # split label and its content
#            print('item:', item)
            if item[0] == '':                        # continue if the label does not exist
                continue
            else:
                dict_temp[item[0]] = item[1]         # save index and value in the dictionary
        
        output.append(dict_temp)                     # save the dictionary into the list
    return output

# print output as csv structure
def printOutput(output):
    print (json.dumps(output, sort_keys = False, indent = 3, ensure_ascii=False))
