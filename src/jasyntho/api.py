# -*- coding: utf-8 -*-

"""Main code."""


def segment_sample(model):
    """
    Main data processing pipeline for USPTO
    """

    import os
    import pickle
    import random

    from jasyntho.segment import Segmentor

    with open("DATASET_PARAGRAPH_Q2_Q3.pickle", "rb") as r:
        DATA = pickle.load(r)

    # Initialize Segmentor object with chosen model
    segmenter = Segmentor(model)

    # Select name for pickle to store
    name_db = f"DATABASE_Q2_Q3_{model}.pickle"

    # infinitely process the pipeline
    while True:
        # check if the pickle file exists
        if os.path.isfile(name_db):
            with open(name_db, "rb") as f:
                DATABASE = pickle.load(f)
        else:
            DATABASE = {}

        if len(DATABASE) % 50 == 0:
            print(f"DB size: {len(DATABASE)}")

        # step 1: check if paragraph (p) has been processed and saved into DATABASE;
        # if not, undergo paragraph segmentation
        # generate a random number in the range of DATASET_PARAGRAPH_Q2_Q3
        num = random.randint(0, len(DATA) - 1)

        parag = DATA[num]

        if parag not in DATABASE.keys():
            segm_parag = segmenter.syn2segment(parag)

            # update the DB
            DATABASE[parag] = segm_parag

            # Store the updated DB
            with open(name_db, "wb") as f:
                pickle.dump(DATABASE, f)

        else:
            # Stop the program if no more samples possible
            if len(DATABASE) == len(DATA):
                break

            continue
