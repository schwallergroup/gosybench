<!--
<p align="center">
  <img src="https://github.com/schwallergroup/jasyntho/raw/main/docs/source/logo.png" height="150">
</p>
-->

<h1 align="center">
  jasyntho
</h1>


[![tests](https://github.com/schwallergroup/jasyntho/actions/workflows/tests.yml/badge.svg)](https://github.com/schwallergroup/jasyntho)
[![DOI:10.1101/2020.07.15.204701](https://zenodo.org/badge/DOI/10.48550/arXiv.2304.05376.svg)](https://doi.org/10.48550/arXiv.2304.05376)
[![PyPI](https://img.shields.io/pypi/v/jasyntho)](https://img.shields.io/pypi/v/jasyntho)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/jasyntho)](https://img.shields.io/pypi/pyversions/jasyntho)
[![Documentation Status](https://readthedocs.org/projects/jasyntho/badge/?version=latest)](https://jasyntho.readthedocs.io/en/latest/?badge=latest)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Cookiecutter template from @SchwallerGroup](https://img.shields.io/badge/Cookiecutter-schwallergroup-blue)](https://github.com/schwallergroup/liac-repo)
[![Learn more @SchwallerGroup](https://img.shields.io/badge/Learn%20%0Amore-schwallergroup-blue)](https://schwallergroup.github.io)


A library for extraction of implicit scientific insights from total synthesis documents. 

## 💪 Getting Started

Extracting the full synthetic sequence from a paper's SI

```python
from jasyntho import SynthTree

doc_src = 'tests/examples/synth_SI_sub.pdf'  # Src doc is typically an SI
stree = SynthTree(doc_src, OPENAI_API_KEY)   # Extract data and create synthetic tree

mtree = stree.merged_trees  # Synthetic sequence

# TODO: Create visualization
print(mtree)
```

```bash
21
├── 22
│   ├── S1
│   │   ├── cyclohexane
│   │   └── MeMgBr
│   ├── HBr
│   ├── DCM
...
```

Running segmentation of a single synthesis paragraph

```python
from jasyntho.segment import SegFlanT5

paragraph = (
  "To a rapidly stirred solution of saturated aqueous ammonium hydroxide (50 mL) and ice in a 0 deg. C. bath was added "
  "2,4-dichloro-5-nitropyrimidine (6.0 g, 31 mmol) in portions. The resulting yellow foamy mixture was allowed to stir "
  "for 30 min, at which point the precipitate was isolated by filtration. The solid was rinsed several times with ice-cold "
  "water and once with ice cold ethanol to give a peach-colored solid. The crude solid was purified by adsorption onto 18 g "
  "silica gel, followed by silica gel chromatography, eluting with 0-20% MeOH/dichloromethane to give "
  "2-chloro-5-nitropyrimidin-4-amine as an off-white solid. MS (ES+): 175 (M+H)+; Calc. for C4H3ClN4O2=174.55."
)

segment = SegFlanT5()
segm_prg = segment(paragraph)

print(segm_prg)
```

Produces
```bash
[
  {
    'text segment': "'To a rapidly stirred solution of saturated aqueous ammonium hydroxide (50 mL) and ice in a 0 deg. C. bath was added 2,4-dichloro-5-nitropyrimidine (6.0 g, 31 mmol) in portions. The resulting yellow foamy mixture was allowed to stir for 30 min, at which point the precipitate was isolated by filtration.'",
    'text class': 'reaction set-up',
    'step order': '1'
  },
  {
    'text segment': "'The solid was rinsed several times with ice-cold water and once with ice cold ethanol to give a peach-colored solid.'",
    'text class': 'work-up',
    'step order': '2'
  },
  {
    'text segment': "'The crude solid was purified by adsorption onto 18 g silica gel, followed by silica gel chromatography, eluting with 0-20% MeOH/dichloromethane to give 2-chloro-5-nitropyrimidin-4-amine as an off-white solid.'",
    'text class': 'purification',
    'step order': '3'
  },
  {
    'text segment': "'MS (ES+): 175 (M+H)+; Calc. for C4H3ClN4O2=174.55.'",
    'text class': 'analysis',
    'step order': '4'
  }
]
```

## 🚀 Installation

<!-- Uncomment this section after your first ``tox -e finish``
The most recent release can be installed from
[PyPI](https://pypi.org/project/jasyntho/) with:

```shell
$ pip install jasyntho
```
-->

The most recent code and data can be installed directly from GitHub with:

```bash
$ pip install git+https://github.com/schwallergroup/jasyntho.git
```


### Command Line Interface

The jasyntho command line tool is automatically installed. It can
be used from the shell with the `--help` flag to show all subcommands:

```shell
$ jasyntho --help
```

> TODO show the most useful thing the CLI does! The CLI will have documentation auto-generated
> by `sphinx`.


## 🛠️ For Developers


<details>
  <summary>See developer instructions</summary>

## 👐 Contributing

Contributions, whether filing an issue, making a pull request, or forking, are appreciated. See
[CONTRIBUTING.md](https://github.com/schwallergroup/jasyntho/blob/master/.github/CONTRIBUTING.md) for more information on getting involved.

## 👋 Attribution

### ⚖️ License

The code in this package is licensed under the MIT License.

<!--
### 📖 Citation

Citation goes here!
-->

<!--
### 🎁 Support

This project has been supported by the following organizations (in alphabetical order):

- [Harvard Program in Therapeutic Science - Laboratory of Systems Pharmacology](https://hits.harvard.edu/the-program/laboratory-of-systems-pharmacology/)

-->

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
$ git clone git+https://github.com/schwallergroup/jasyntho.git
$ cd jasyntho
$ pip install -e .
```

### 🥼 Testing

After cloning the repository and installing `tox` with `pip install tox`, the unit tests in the `tests/` folder can be
run reproducibly with:

```shell
$ tox
```

Additionally, these tests are automatically re-run with each commit in a [GitHub Action](https://github.com/schwallergroup/jasyntho/actions?query=workflow%3ATests).

### 📖 Building the Documentation

The documentation can be built locally using the following:

```shell
$ git clone git+https://github.com/schwallergroup/jasyntho.git
$ cd jasyntho
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
   `src/jasyntho/version.py`, and [`docs/source/conf.py`](docs/source/conf.py) to not have the `-dev` suffix
2. Packages the code in both a tar archive and a wheel using [`build`](https://github.com/pypa/build)
3. Uploads to PyPI using [`twine`](https://github.com/pypa/twine). Be sure to have a `.pypirc` file configured to avoid the need for manual input at this
   step
4. Push to GitHub. You'll need to make a release going with the commit where the version was bumped.
5. Bump the version to the next patch. If you made big changes and want to bump the version by minor, you can
   use `tox -e bumpversion -- minor` after.
</details>
