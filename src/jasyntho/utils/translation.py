"""Translation utils between molecular representations."""

import re

# silence py2opsin
import warnings
from json import JSONDecodeError
from typing import List, Optional

import networkx as nx
import requests
from py2opsin import py2opsin

warnings.filterwarnings("ignore", category=RuntimeWarning, module="py2opsin")


def name_to_smiles(name: str, subs_label: str) -> Optional[str]:
    """Convert IUPAC name into SMILES."""
    s = py2opsin(name)
    if s:
        return s

    # Maybe substance label is in name. Remove if so
    if subs_label in name:
        regex = f"\(?{subs_label}\)?"
        name = re.sub(regex, "", name)
        s = py2opsin(name)
        if s:
            return s
    return None
