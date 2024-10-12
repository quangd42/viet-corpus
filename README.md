# Viet corpus converter

### Introduction

This CLI tool is a wrapper around [genkey](https://github.com/semilin/genkey). The goal is to create a corpora .json file from a corpus text file that contains Vietnamese, for keyboard layout analysis and generation using [genkey](https://github.com/semilin/genkey).

### Installation

As this is a genkey wrapper, you will need to [download genkey](https://github.com/semilin/genkey/releases/tag/v1.2.1) to use it. Please note that this was built to work with the built release v1.2.1 specifically.

After downloading genkey, unzip it and copy the _innermost_ folder that contains genkey binary to `src/converter/genkey_runner` and rename it to `genkey`. For example, for mac release, copy the `mac` folder and rename it to `genkey`.

In the project folder start an virtual env and install the CLI.

```
python3 -m venv .venv
. .venv/bin/activate
pip install .
```

### Usage

Afterwards you can start using the CLI `converter`:

```
converter load <file_name.txt> --name <corpus_name> --limit 100000
```

To see more usage help:

```
converter --help
converter COMMAND --help
```

### Notes

All outputs will be stored in `/data` inside project folder. You can copy the outputted json corpora there to your genkey folder for further usage.
