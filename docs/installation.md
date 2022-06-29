# Installation

You can either install LinkML Validator directly from [GitHub repository](https://github.com/linkml/linkml-validator) or from [PyPI](https://pypi.org/project/linkml-validator/).

## Installing from GitHub

**Clone the repository**

```sh
git clone https://github.com/linkml/linkml-validator
cd linkml-validator
```

**Set up a virtual environment**

> This step is optional and depends on how you prefer to set up a virtual environment. 

```
python3 -m venv env
source env/bin/activate
```

**Install**


```sh
python setup.py install
```

**Installation for development**

To install development dependencies (like `pytest`, `mkdocs`, etc.):

```sh
pip install -e ".[dev]"
```
<br>

To test that the installation is successful, try the following:

```sh
linkml-validator --help
```

You should see the usage for `linkml-validator` CLI.


## Installing from PyPI

To install from PyPI, you just simply have to:

```sh
pip install linkml-validator
```

To install as specific version of LinkML Validator,

```sh
pip install linkml-validator==0.4.0
```
