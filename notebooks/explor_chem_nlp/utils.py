"""
SequenceCalculator helps calculate the number of sequence starting with srq1 and ending with seq2.

To do so, import sequencecalculator(seq1, seq2, database), where:
    seq1 and seq2 should be one of the following characters: 'r-', 'w-', 'p-', 'a-', or 'u-'
    database is the pickle file 
"""

import pickle
import re

import Levenshtein
import numpy as np
from sklearn import preprocessing


def sequence_recorder(cls):
    if cls == "reaction set-up":
        return "r-"

    elif cls == "work-up":
        return "w-"

    elif cls == "purification":
        return "p-"

    elif cls == "analysis":
        return "a-"

    elif cls == "unclassified":
        return "u-"

    # else:
    #     return 'u-'


def sequence_checker(seq1, seq2, segm_parag):
    flag1 = 0
    flag2 = 0
    if_break = 0

    for i in range(len(segm_parag)):
        chr = sequence_recorder(segm_parag[i]["text class"])

        if if_break == 0:
            if chr == seq1:
                flag1 = 1
                if_break = 1
            continue

        if if_break == 1:
            if chr == seq2:
                flag2 = 1

    if flag1 == 1 & flag2 == 1:
        return int(1)

    else:
        return int(0)


def sequence_calculator(seq1, seq2, list_examples):
    total = 0
    for segm_parag in list_examples:
        value = sequence_checker(seq1, seq2, segm_parag)
        total = total + value

    output_string = (
        "The number of sequence starting with " + seq1 + " and ending with " + seq2 + " is: "
    )

    return total


def sequence_matrix_creator(list_examples_quar):
    ls = []
    char_list = ["r-", "w-", "p-", "a-"]

    for i in range(len(char_list)):
        for j in range(len(char_list)):
            output = sequence_calculator(char_list[i], char_list[j], list_examples_quar)
            ls.append(output)

    arr = np.array(ls)
    new_arr = arr.reshape(4, 4)

    return new_arr


def compressed_seq(segm_parags):
    str_temp = ""
    str_list = []

    for segm in segm_parags:
        seq = sequence_recorder(segm["text class"])

        # check if str_list is empty
        if len(str_list) == 0:
            str_list.append(seq)

        else:
            # if seq is the same as the last seq in the list, do not append it
            # in the list as we want to compress a sequence
            if str_list[-1] == seq:
                continue

            else:
                str_list.append(seq)

    # make a compressed string
    for s in str_list:
        str_temp = str_temp + s

    return str_temp


def compressed_class(segm_parags):
    class_list = []

    for segm in segm_parags:
        cls = segm["text class"]

        # check if str_list is empty
        if len(class_list) == 0:
            class_list.append(cls)

        else:
            # if seq is the same as the last seq in the list, do not append it
            # in the list as we want to compress a sequence
            if class_list[-1] == cls:
                continue

            else:
                class_list.append(cls)

    return class_list


def class_checker(seq1, seq2, class_list):
    flag1 = 0
    flag2 = 0
    if_break = 0

    for cls in class_list:
        chr = sequence_recorder(cls)

        if if_break == 0:
            if chr == seq1:
                flag1 = 1
                if_break = 1
            continue

        if if_break == 1:
            if chr == seq2:
                flag2 = 1

    if flag1 == 1 & flag2 == 1:
        return int(1)

    else:
        return int(0)


def class_calculator(seq1, seq2, class_list):
    total = 0
    for cls in class_list:
        value = class_checker(seq1, seq2, cls)
        total = total + value

    return total


def class_matrix_creator(class_list):
    ls = []
    char_list = ["r-", "w-", "p-", "a-"]

    for i in range(len(char_list)):
        for j in range(len(char_list)):
            total = class_calculator(char_list[i], char_list[j], class_list)
            ls.append(total)

    arr = np.array(ls)
    arr_norm = preprocessing.normalize([arr])
    new_arr = arr_norm.reshape(4, 4)

    return new_arr


def rxn_setup_work_up_text(segm_parags):
    rxn_set_up_str = ""
    work_up_str = ""
    flag = 0  # check if a work-up exists; if the work-up exists, the 2nd rxn set-up should not be concat to the rxn- set-up string

    for segm in segm_parags:
        cls = segm["text class"]
        text_segm = segm["text segment"][1:-1]

        if cls == "reaction set-up":
            if flag == 0:  # a work-up is not in the string, rxn set-up can be concat to the string
                if rxn_set_up_str == "":
                    rxn_set_up_str += text_segm
                else:
                    rxn_set_up_str += " "
                    rxn_set_up_str += text_segm
            else:  # a work-up is in the string, this is the 2nd rxn set-up, and we will not concat it into the string; two strings can be returned
                return rxn_set_up_str, work_up_str

        elif cls == "work-up":
            # Do not add the text segment into the string if a work-up happens before a rxn set-up
            if rxn_set_up_str == "":
                continue
            else:
                if work_up_str == "":
                    work_up_str += text_segm
                    flag = 1
                else:
                    work_up_str += " "
                    work_up_str += text_segm
                    flag = 1

    return rxn_set_up_str, work_up_str

    # situation 0: r-w- V
    # situation 0.5: r-w-w- V
    # situation 1: r-r-w-w- V
    # situation 2: r-w-r-w-
    # situation 3: w-r- V
    # situation 4: r-a-


def edit_distance_checkor(parag, segm_parags):
    resulting_parag = ""

    for segm in segm_parags:
        resulting_parag += segm["text segment"][1:-1]
        if segm != segm_parags[-1]:
            resulting_parag += " "

    edit_dist = Levenshtein.distance(resulting_parag, parag)
    return edit_dist


def str_combine(str1, str2):
    str_temp = str1 + " " + str2
    return str_temp


def class_check(class1, class2):
    if class1 == class2:
        return True
    else:
        return False


# compress segments if they have the same text classes
def segms_compress(segms):
    str_temp = ""
    text_class = ""
    step_order = 0
    ls = []

    if len(segms) == 1:
        return segms

    else:
        for i in range(0, len(segms) - 1):
            if class_check(segms[i]["text class"], segms[i + 1]["text class"]):
                if str_temp != "":
                    str_temp = str_combine(str_temp, segms[i + 1]["text segment"][1:-1])
                    text_class = text_class
                    step_order = step_order

                else:
                    str_temp = str_combine(
                        segms[i]["text segment"][1:-1], segms[i + 1]["text segment"][1:-1]
                    )
                    text_class = segms[i]["text class"]
                    step_order = str(int(segms[i]["step order"]) - i + len(ls))

            else:
                if str_temp != "":
                    ls.append(
                        {
                            "text segment": str_temp,
                            "text class": text_class,
                            "step order": step_order,
                        }
                    )
                    str_temp = ""

                else:  # r-w-w
                    dict_temp = {
                        "text segment": segms[i]["text segment"],
                        "text class": segms[i]["text class"],
                        "step order": str(int(segms[i]["step order"]) - i + len(ls)),
                    }
                    ls.append(dict_temp)

        if str_temp != "":
            ls.append(
                {"text segment": str_temp, "text class": text_class, "step order": step_order}
            )

        else:  # r-w-r-w
            dict_temp = {
                "text segment": segms[i + 1]["text segment"],
                "text class": segms[i + 1]["text class"],
                "step order": str(int(segms[i]["step order"]) - i + len(ls)),
            }
            ls.append(dict_temp)

        return ls

        # r- V
        # r-r- V
        # r-r-r- V
        # r- w- V
        # r-w-w
        # r-r-w-w V
        # r-w-r-w- V


def check_substring(substring):
    """
    A paragraph segment (substring) consists of a text segment, a text class and a step order
    closed by a pair of braces "{}"; any paragraph segment (substring) that contains multiple
    text segments, text classes, step orders, or the symbols '{' or '}' is not in the valid
    format as required for the output.
    """

    left_brace_count = substring.count("{")
    right_brace_count = substring.count("}")
    text_segment_count = substring.count("text segment")
    text_class_count = substring.count("text class")
    step_order_count = substring.count("step order")

    if (
        left_brace_count
        == 1 & right_brace_count
        == 1 & text_segment_count
        == 1 & text_class_count
        == 1 & step_order_count
        == 1
    ):
        return True

    else:
        return False


def check_segment_format(string):
    """
    Return 1 if the segment follow the format "{ text segment -text class - step order }"
    Return o if not
    """

    # step 1: split the string into substring by recognizing "}, "
    remove_delimiter = "}, "
    add_delimiter = "}"

    # Split a string without removing the delimiter
    substring_list = [
        substring + add_delimiter for substring in string.split(remove_delimiter) if substring
    ]

    # Removing the trailing delimiter "}" in the last element
    substring_list[-1] = substring_list[-1].rstrip(add_delimiter)

    # step 2: in each substring, check if text segment, text class, step order appear only once
    for substring in substring_list:
        check = check_substring(substring)

        # if a segment is not in the valid output format, return 0
        if check == False:
            return 0

        # otherwise, continue to check the format
        else:
            continue

    if check == True:
        return 1


def concat_text_segment(substring):
    """
    Check if the edit_distance between the referenced and resulting paragraphs is zero
    """

    # search for the text segment, which is in between text segment and text class
    raw_text_segment = re.search("text segment(.+?)text class", substring)

    # return the text segment if it exists
    if raw_text_segment is not None:
        text_segment = raw_text_segment.group(1)[5:-5]
        return text_segment

    # return empty text segment if it does not exist
    else:
        text_segment = raw_text_segment
        return ""


def check_edit_distance(parag, string):
    # step 1: split the string into substring by recognizing "}, "
    remove_delimiter = "}, "
    add_delimiter = "}"

    # Split a string without removing the delimiter
    substring_list = [
        substring + add_delimiter for substring in string.split(remove_delimiter) if substring
    ]

    # Removing the trailing delimiter "}" in the last element
    substring_list[-1] = substring_list[-1].rstrip(add_delimiter)

    # step 2: concatenate each segmented text
    concat_parag = ""

    for substring in substring_list:
        concat_parag += concat_text_segment(substring)

        # concatenate the string with a " " if something exists in the string
        if substring != substring_list[-1]:
            concat_parag += " "

    edit_dist = Levenshtein.distance(concat_parag, parag)

    return edit_dist
