"""Script to collect data for IUPAC name extraction from user."""

import os
import pickle

import numpy as np

# from jasyntho import SynthTree
# from jasyntho.utils import set_llm
# from jasyntho.utils import RetrieveName, name_to_smiles

# set_llm(llm_dspy='mistral-large-latest')
# iupac_retrieve = RetrieveName()


with open("pars.txt", "rb") as f:
    pars = pickle.load(f)

samples = []
for p in np.random.permutation(pars)[:40]:
    print(p)
    print("\n")
    is_fine_example = input("Is this a fine example? (y/n): ")
    if is_fine_example == "n":
        continue
    ref_key = input("ref_key: ")
    name = input("name: ")
    print("\n")

    samples.append(
        {
            "status": "good",
            "content": {"ref_key": ref_key, "name": name, "text": p},
        }
    )

print(f"{len(samples)} recovered.")

import json

try:
    with open("samples_iupac.json", "r") as f:
        data = json.load(f)
    data.extend(samples)
except:
    data = samples
    pass


with open("samples_iupac.json", "w") as f:
    json.dump(data, f, indent=4)
