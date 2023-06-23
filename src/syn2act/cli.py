# -*- coding: utf-8 -*-

"""Command line interface for :mod:`syn2act`.

Why does this file exist, and why not put this in ``__main__``? You might be tempted to import things from ``__main__``
later, but that will cause problems--the code will get executed twice:

- When you run ``python3 -m syn2act`` python will execute``__main__.py`` as a script.
  That means there won't be any ``syn2act.__main__`` in ``sys.modules``.
- When you import __main__ it will get executed again (as a module) because
  there's no ``syn2act.__main__`` in ``sys.modules``.

.. seealso:: https://click.palletsprojects.com/en/8.1.x/setuptools/#setuptools-integration
"""

import logging

import click

__all__ = [
    "segment",
]

logger = logging.getLogger(__name__)


# @click.group()
# @click.version_option()
@click.command()
@click.option(
    "--model",
    default="gpt-3.5-turbo-16k",
    type=click.Choice(["gpt-4", "gpt-3.5-turbo-16k", "anthropicai"]),
    help="what model to use for the segmentation pipeline.",
)
def segment(model):
    """
    Main data processing pipeline for USPTO
    """

    import os
    import pickle
    import random

    from syn2act import Segmentor

    with open("DATASET_PARAGRAPH_Q2_Q3.pickle", "rb") as r:
        DATA = pickle.load(r)

    available_models = ["gpt-4", "gpt-3.5-turbo-16k", "anthropicai"]

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

        if len(DATABASE)%50==0:
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


@click.group()
def main():
    """main"""
    return 0


if __name__ == "__main__":
    main()
