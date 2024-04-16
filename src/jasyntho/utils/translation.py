"""Translation utils between molecular representations."""

import re
import requests
from json import JSONDecodeError
from py2opsin import py2opsin
from typing import Optional, List
import networkx as nx


# silence py2opsin
import warnings
warnings.filterwarnings('ignore', category=RuntimeWarning, module='py2opsin')

def name_to_smiles(name: str, subs_label: str) -> Optional[str]:
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
