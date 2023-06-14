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
    "main",
]

logger = logging.getLogger(__name__)


@click.group()
@click.version_option()
def main():
    # Import data
    path_data_applications = "data/Extracted_Data_2001_Sep2016_USPTOapplications_new.csv"
    path_data_grant = "data/Extracted_Data_1976_Sep2016_USPTOgrants_new.csv"

    data_app = pd.read_csv(path_data_applications, encoding="utf8")
    data_grant = pd.read_csv(path_data_grant, encoding="utf8")

    # segment paragraph, extract data and save as json
    json_list = []
    for text in data_app.head(1)["Paragraph Text"]:
        json_text = paragraph2json(text)
        json_list.append(json_text)
        print("\n\n")

    for text in data_grant.head(1)["Paragraph Text"]:
        json_text = paragraph2json(text)
        json_list.append(json_text)
        print("\n\n")

    json_string = json.dumps(json_list)
    # Using a JSON string
    with open("json_data_test.json", "w") as outfile:
        outfile.write(json_string)


if __name__ == "__main__":
    main()
