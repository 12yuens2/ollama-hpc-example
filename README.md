# Ollama HPC Example

[Ollama](https://ollama.com/) is a tool for running LLM and is very well set up for running quantised models. 
They have a large collection of [easily installable models](https://ollama.com/library), and I believe it is possible to [run your own model](https://github.com/ollama/ollama/blob/main/docs/import.md), but I haven't tried this personally.
Ollama also has a [Python library](https://github.com/ollama/ollama-python) available to be installed through [pip](https://pypi.org/project/ollama/).

This resource aims to show how to get Ollam running on Baskerville HPC, by providing a minimal example.

## This Package

This package has only the `ollama` Python package dependency and is made to be a minimal thing that can be run that uses an LLM and saves the result somewhere. 
It only has six things:

* `pyproject.toml` - To set up the python environment.
* `script/score_pizza.py` - A simple script with no arguments which will use the LLM.
* `data/pizza_types.csv` - Some data that is read.
* `data/pizza_scored.csv` - A CSV that is saved by the model this will change each time as the model is non-deterministic.
* `ollama_batch/batch-ollama-setup.sh` - Batch script that sets up the Ollama program and the python enviroment on Baskerville, it only needs to be run once.
* `ollama_batch/batch-ollama-run.sh` - SBATCH script to run the python script which interacts with the Ollama server.

## Ollama CLT

#### Installation

In order to get Ollama running in Python the command line program Ollama is needed.
If the model is not installed then there will be a connection error thrown by the python program.

Normally this can be installed with `curl` though `curl -fsSL https://ollama.com/install.sh | sh`, but this DOES NOT WORK on Baskerville.

It instead can be installed with:
```bash
mkdir ollama_install
pushd ollama_install
curl -L https://ollama.com/download/ollama-linux-amd64.tgz -o ollama-linux-amd64.tgz
mkdir usr
tar -C usr -xvf ollama-linux-amd64.tgz 
popd
```

This places the Ollama install in the `ollama_install` directory, but to run it the environment variables need to be set.

#### Enviroment Variables

There are a couple of environment variables that are needed to run with this custom install.

  * `PATH` - Needs to point to `/ollama_install/usr/bin`.
  * `LD_LIBRARY_PATH` - Needs to point to `/ollama_install/usr/lib`.
  * `OLLAMA_MODELS` - Needs to point to `/ollama_install/models`. This is where Ollama installs the models and they are large so make sure that they are in your project folder. 
  * `OLLAMA_HOST` - This is the IP address the server should watch this needs to be set as if multiple Ollama servers are running at the same time at the same port they will interfere.

#### Running Ollama

This Ollama is [documented here](https://github.com/ollama/ollama/tree/main/docs).
The documentation is a bit sparse, but the main commands seem to be.

  * `ollama serve` - which starts a connection port 11434 by default that commands can be sent to
  * `ollama list`  - which lists the available models 
  * `ollama pull` - which downloads a model from the library
  * `ollama run` - which opens up an interactive session in the terminal


## Ollama-python

There is a [Python library](https://github.com/ollama/ollama-python), but the documentation is quite limited.
The variable names are well-named and the whole package is quite simple so most of the options can be inferred from the source code. 
Most of the options are passed in a [options dictionary](https://github.com/ollama/ollama-python/blob/ebe332b29d5c65aeccfadd4151bf6059ded7049b/ollama/_types.py#L145)
and the host addressed is [passed to the client](https://github.com/ollama/ollama-python/blob/ebe332b29d5c65aeccfadd4151bf6059ded7049b/ollama/_client.py#L38).

There is an option called `stream` which I believe means ollama provides the result word by word.
This probably isn't what we want if we are trying to do data science and more if you want to integrate it with a GUI.