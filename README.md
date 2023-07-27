# Sample python command line app with developer environment and continuous integration

This repository demonstrates an opinionated setup for a python command line app. It shows how to

- configure the VS Code IDE for easy  python3 based development, including testing and linting
- a docker based development environment
- package management and python version tooling
- continuous integration using GitHub including unit tests and code coverage
- packaging and building the python CLI app ready for distribution

## Developer Quick start

- install vs code and docker (tested on windows with WSL2 and docker desktop)
- clone the repository
- open the repo in vscode and switch to the dev container (CTRL-P -> Reopen in dev container)
- open a terminal and run `poetry install` to restore dependencies
- run the code within poetry in a virtual environment: `poetry run demo hello bob`
- or run the code with python3 in a virtual environment: `poetry shell` and `poetry install` to setup env and then `python3 src/main.py hello alice` or even just `demo hello charlie` works because the command is actually installed in the virtual env.
- One click to run the tests and generate coverage: `./build.sh`
- One click to package the app into the /dist folder: `./pack.sh`
- One click to run the tests and package the app across multiple versions of python 3.9, 3.10, 3.11 etc: `./build-all.sh`

## How to install and use the tool

See `install.sh`.

- Download the tar from the GitHub Actions build artifacts (could also use the wheel (.whl) if you prefer)
- Make sure you have the correct version of python installed (probably python3.10). If not use pyenv (see install pyenv section below).
- Install pipx (not required but this ensures the tool is installed in it's own environment and dependencies cannot make a mess of your system)
- [Install it with pipx](https://pypa.github.io/pipx/docs/#pipx-install) `pipx install --python some-version path-to-tar` (or with pip if you must).
- Run `demo hello world` on the command line to check it installed ok

## IDE, Docker, Python

The app uses VS code with docker the devcontainers feature to setup a python environment with all tools preinstalled. All you need is vscode and docker to be able develop.

## Python command line app using typer

This repo publishes to the `/dist` folder a python wheel (.whl) and tar containing a CLI executable called `demo` that can be installed and run. This app uses the library typer to produce a user friendly interactive cli

## Tools - poetry, pyenv, isort, flake8, black

All these tools are preinstalled in the dev container:

- **Python3** - multiple versions installed and available, managed using pyenv
- **Poetry** - tool to manage python dependencies, tools and package
- **isort, black and flake8** - configured to lint and tidy up your python code automatically. Executed using ./build.sh and CTRL+SHIFT+B (build in vscode)

## Testing - pytest, code coverage

The project shows how to create unit test.

Either use the test runner in vscode (with debugging)

Or on the cli using pytest:

```
$ pytest

# or a subset of tests
$ pytest tests/test_main.py
$ pytest -k hello
```

The tests can be run:

- from inside vscode using the Testing window
- from the CLI against the current and multiple python versions (See quick start)
- In GitHub actions on every check-in

Test reports appear automatically in the github actions report

Code coverage data is generated on build into the folder `htmlcov`


## Continuous Integration with GitHub Actions

The `.github/workflows/ci.yml` define a workflow to run on build and test the CLI against multiple versions of python. Build artifacts are generated and a copy of the cli app is available for download for every build

## Want to know more?

Check out the [Tour](Tour.md)

## How to install pyenv

For ubuntu. pyenv makes life easier with miltiple versions.

1. Install [python build tooling](https://github.com/pyenv/pyenv/wiki#suggested-build-environment) (you are going to build and install python from source)
    ```
    sudo apt update; sudo apt install build-essential libssl-dev zlib1g-dev \
    libbz2-dev libreadline-dev libsqlite3-dev curl \
    libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
    ```
1. Install pyenv using the pyenv installer
    ```
    curl https://pyenv.run | bash
    ```
1. After installing, follow [these instructions](https://github.com/pyenv/pyenv#set-up-your-shell-environment-for-pyenv) to set up your shell environment.

## How to install a new version of python using pyenv

Install the version you want:
```bash
# choose what version you want
pyenv install 3.10  # can add many 3.9 3.10 3.11
# fix any shims so that commands like python3.10 work
pyenv rehash
python3.10 --version
# see what is installed
pyenv versions
```

If you want the current folder to always use a version set it as local

```bash
python3 --version # will print your system python version, say 3.8
pyenv local 3.10
python3 --version ## will now print the version of 3.10 installed by pyenv
```

## Troubleshooting

Make sure you have opened the folder in VS Code with Dev Containers.

Reinstall everything by re-running instal script (done for you in dev container init is using vscode)

```
./dev-env-first-time.sh
```

Check the tools are on the path and work:

```
$ poetry --version
Poetry (version 1.3.2)

# also you can update it
$ poetry self update
```

Start a shell (this creates a virtual env for you automatically) with the tools we need available. vscode may do this automagically when you spawn a terminal.

```
$ poetry shell
```

Restore dependencies

```
$ poetry install
```

and now you can run tools on the cli such as

```
pytest
flake8
black src
```

You may need to tell vscode to use your python venv: CTRL+P `Python: select Interpreter` and select the python in the `.venv/bin/python3` folder


Try changing from zsh to bash shell.
