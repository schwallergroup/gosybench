<!--
<p align="center">
  <img src="https://github.com/schwallergroup/gosybench/raw/main/docs/source/logo.png" height="150">
</p>
-->

<h1 align="center">
  GOSyBench
</h1>


[![tests](https://github.com/schwallergroup/gosybench/actions/workflows/tests.yml/badge.svg)](https://github.com/schwallergroup/gosybench)
[![DOI:10.18653/v1/2024.langmol-1.9](https://zenodo.org/badge/DOI/10.18653/v1/2024.langmol-1.9.svg)](https://aclanthology.org/2024.langmol-1.9/)
[![PyPI](https://img.shields.io/pypi/v/gosybench)](https://img.shields.io/pypi/v/gosybench)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/gosybench)](https://img.shields.io/pypi/pyversions/gosybench)
[![Documentation Status](https://readthedocs.org/projects/gosybench/badge/?version=latest)](https://gosybench.readthedocs.io/en/latest/?badge=latest)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Cookiecutter template from @SchwallerGroup](https://img.shields.io/badge/Cookiecutter-schwallergroup-blue)](https://github.com/schwallergroup/liac-repo)
[![Learn more @SchwallerGroup](https://img.shields.io/badge/Learn%20%0Amore-schwallergroup-blue)](https://schwallergroup.github.io)


A benchmark for Knowledge Graph Extraction from Total Synthesis documents.

## 💪 Getting Started

```python
from gosybench.basetypes import STree
from gosybench.evaluate import GOSyBench
from gosybench.metrics import GraphEval, TreeMetrics


def test_method(path: str) -> STree:
    # Define your method for KGE here.
    return STree(products=[], graph=nx.DiGraph())

gosybench = GOSyBench(
    project="my-eval",
    describe=TreeMetrics(),
    metrics=GraphEval(),
)

# Evaluate
gosybench.evaluate(test_method)
```

## 🚀 Installation

The most recent code and data can be installed directly from GitHub with:

```bash
$ pip install git+https://github.com/schwallergroup/gosybench.git
```

Optionally, you can install **Jasyntho**, our package for KGE.

```bash
$ pip install "git+https://github.com/schwallergroup/gosybench.git#egg=gosybench[jasyntho]"
```


--- 

## 🚀 Advanced Usage

<details>
  <summary>See advanced usage.</summary>
<br>


## 🌱 Jasyntho

Jasyntho is a package for Knowledge Graph Extraction of Total Syntheses.
It relies on LLMs for some core functionalities.

Make sure to create an `.env` file with the API keys of the LLM providers you want to use:
```bash
OPENAI_API_KEY=sk-... 
ANTHROPIC_API_KEY=sk-ant-...
```


Download the paper you want to extract in a directory like this

```bash
jacs.9b12546
    ├── doi.txt
    ├── paper.pdf
    └── si_0.pdf
```

```paper.pdf``` is the main article, and ```si_0.pdf``` is the Supplementary Information of that article.

Then, use Jasyntho like:

```python

from jasyntho import SynthTree

tree = SynthTree.from_dir(path)
tree.rxn_extract = ExtractReaction(llm=model)

tree.raw_prods = await tree.async_extract_rss(
    mode=method, si_select=si_select
)
tree.products = [p for p in tree.raw_prods if not p.isempty()]
tree.full_g = tree.get_full_graph(tree.products)
```


</details>


## ✅ Citation

Andres M Bran, Zlatko Jončev, and Philippe Schwaller. 2024. Knowledge Graph Extraction from Total Synthesis Documents. In Proceedings of the 1st Workshop on Language + Molecules (L+M 2024), pages 74–84, Bangkok, Thailand. Association for Computational Linguistics.
```bibtex
@inproceedings{m-bran-etal-2024-knowledge,
    title = "Knowledge Graph Extraction from Total Synthesis Documents",
    author = "M Bran, Andres  and  Jon{\v{c}}ev, Zlatko  and Schwaller, Philippe",
    booktitle = "Proceedings of the 1st Workshop on Language + Molecules (L+M 2024)",
    year = "2024",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2024.langmol-1.9",
    doi = "10.18653/v1/2024.langmol-1.9",
    pages = "74--84",
 }
```











## 🛠️ For Developers


<details>
  <summary>See developer instructions</summary>

## 👐 Contributing

Contributions, whether filing an issue, making a pull request, or forking, are appreciated. See
[CONTRIBUTING.md](https://github.com/schwallergroup/gosybench/blob/master/.github/CONTRIBUTING.md) for more information on getting involved.

## 👋 Attribution

### ⚖️ License

The code in this package is licensed under the MIT License.


<!--
### 💰 Funding

This project has been supported by the following grants:

| Funding Body                                             | Program                                                                                                                       | Grant           |
|----------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------|-----------------|
| DARPA                                                    | [Automating Scientific Knowledge Extraction (ASKE)](https://www.darpa.mil/program/automating-scientific-knowledge-extraction) | HR00111990009   |
-->

### 🍪 Cookiecutter

This package was created with [@audreyfeldroy](https://github.com/audreyfeldroy)'s
[cookiecutter](https://github.com/cookiecutter/cookiecutter) package using [@cthoyt](https://github.com/cthoyt)'s
[cookiecutter-snekpack](https://github.com/cthoyt/cookiecutter-snekpack) template.

## 🛠️ For Developers

<details>
  <summary>See developer instructions</summary>

The final section of the README is for if you want to get involved by making a code contribution.

### Development Installation

To install in development mode, use the following:

```bash
$ git clone git+https://github.com/schwallergroup/gosybench.git
$ cd gosybench
$ pip install -e .
```

### 🥼 Testing

After cloning the repository and installing `tox` with `pip install tox`, the unit tests in the `tests/` folder can be
run reproducibly with:

```shell
$ tox
```

Additionally, these tests are automatically re-run with each commit in a [GitHub Action](https://github.com/schwallergroup/gosybench/actions?query=workflow%3ATests).

### 📖 Building the Documentation

The documentation can be built locally using the following:

```shell
$ git clone git+https://github.com/schwallergroup/gosybench.git
$ cd gosybench
$ tox -e docs
$ open docs/build/html/index.html
``` 

The documentation automatically installs the package as well as the `docs`
extra specified in the [`setup.cfg`](setup.cfg). `sphinx` plugins
like `texext` can be added there. Additionally, they need to be added to the
`extensions` list in [`docs/source/conf.py`](docs/source/conf.py).

### 📦 Making a Release

After installing the package in development mode and installing
`tox` with `pip install tox`, the commands for making a new release are contained within the `finish` environment
in `tox.ini`. Run the following from the shell:

```shell
$ tox -e finish
```

This script does the following:

1. Uses [Bump2Version](https://github.com/c4urself/bump2version) to switch the version number in the `setup.cfg`,
   `src/gosybench/version.py`, and [`docs/source/conf.py`](docs/source/conf.py) to not have the `-dev` suffix
2. Packages the code in both a tar archive and a wheel using [`build`](https://github.com/pypa/build)
3. Uploads to PyPI using [`twine`](https://github.com/pypa/twine). Be sure to have a `.pypirc` file configured to avoid the need for manual input at this
   step
4. Push to GitHub. You'll need to make a release going with the commit where the version was bumped.
5. Bump the version to the next patch. If you made big changes and want to bump the version by minor, you can
   use `tox -e bumpversion -- minor` after.
</details>
