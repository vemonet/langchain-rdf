<div align="center">

# LangChain RDF

<!-- [![PyPI - Version](https://img.shields.io/pypi/v/langchain-rdf.svg?logo=pypi&label=PyPI&logoColor=silver)](https://pypi.org/project/langchain-rdf/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/langchain-rdf.svg?logo=python&label=Python&logoColor=silver)](https://pypi.org/project/langchain-rdf/)
[![license](https://img.shields.io/pypi/l/langchain-rdf.svg?color=%2334D058)](https://github.com/vemonet/langchain-rdf/blob/main/LICENSE.txt)

[![Publish package](https://github.com/vemonet/langchain-rdf/actions/workflows/publish.yml/badge.svg)](https://github.com/vemonet/langchain-rdf/actions/workflows/publish.yml) -->

[![Test package](https://github.com/vemonet/langchain-rdf/actions/workflows/test.yml/badge.svg)](https://github.com/vemonet/langchain-rdf/actions/workflows/test.yml)

[![Hatch project](https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg){ loading=lazy .off-glb }](https://github.com/pypa/hatch) [![linting - Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json){ loading=lazy .off-glb }](https://github.com/astral-sh/ruff) [![code style - Black](https://img.shields.io/badge/code%20style-black-000000.svg){ loading=lazy .off-glb }](https://github.com/psf/black) [![types - Mypy](https://img.shields.io/badge/types-Mypy-blue.svg){ loading=lazy .off-glb }](https://github.com/python/mypy)

</div>

Loaders and utils to work with [RDF](https://www.w3.org/RDF/) data using [LangChain](https://python.langchain.com):

* `OntologyLoader`: load OWL ontology in your vectorstore for Retrieval Augmented Generation

## 📦️ Installation

This package requires Python >=3.8, install it from the git repository with:

```bash
pip install git+https://github.com/vemonet/langchain-rdf.git
```

## 🪄 Usage

### 🐍 Use with python

 Use this package in python scripts:

 ```python
from langchain_rdf import OntologyLoader

loader = OntologyLoader("https://semanticscience.org/ontology/sio.owl")
documents = loader.load()
print(documents)
 ```

## 🧑‍💻 Development setup

The final section of the README is for if you want to run the package in development, and get involved by making a code contribution.


### 📥️ Clone

Clone the repository:

```bash
git clone https://github.com/vemonet/langchain-rdf
cd langchain-rdf
```
### 🐣 Install dependencies

Install [Hatch](https://hatch.pypa.io), this will automatically handle virtual environments and make sure all dependencies are installed when you run a script in the project:

```bash
pipx install hatch
```

### ☑️ Run tests

Make sure the existing tests still work by running the test suite and linting checks. Note that any pull requests to the fairworkflows repository on github will automatically trigger running of the test suite;

```bash
hatch run test
```

To display all logs when debugging:

```bash
hatch run test -s
```



### ♻️ Reset the environment

In case you are facing issues with dependencies not updating properly you can easily reset the virtual environment with:

```bash
hatch env prune
```

Manually trigger installing the dependencies in a local virtual environment:

```bash
hatch -v env create
```

### 🏷️ New release process

The deployment of new releases is done automatically by a GitHub Action workflow when a new release is created on GitHub. To release a new version:

1. Make sure the `PYPI_TOKEN` secret has been defined in the GitHub repository (in Settings > Secrets > Actions). You can get an API token from PyPI at [pypi.org/manage/account](https://pypi.org/manage/account).
2. Increment the `version` number in the `pyproject.toml` file in the root folder of the repository.

    ```bash
    hatch version fix
    ```

3. Create a new release on GitHub, which will automatically trigger the publish workflow, and publish the new release to PyPI.

You can also build and publish from your computer:

```bash
hatch build
hatch publish
```
