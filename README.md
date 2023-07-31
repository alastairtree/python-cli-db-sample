# Sample python database command line app with developer environment and continuous integration

This repository demonstrates an opinionated setup for a python command line app with database access. It expands on [a python cli sample app](https://github.com/alastairtree/python-cli-devenv-and-ci-sample) to add database functionality:

- configure the VS Code IDE for easy python3 and database based development, including testing and linting and sql tools
- a docker based development environment and dev container running postgres
- an ORM (sqlalchemy) and database migrations (alembic)
- Continuous integration using GitHub Actions to run tests and generate coverage reports with tests connecting to a real database running in a container alongside the build runner.

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

# Database commands

CLI Commands to demonstrate database use, and to manage the database have been added. Typer has been used to make a user friendly CLI app.

```bash
# connect to postgress, create the database if required and then create 2 tables based on the ORM.  Thhis comand shows how to use the ORM to create the database schema and populate some rows of data
demo create-db

# Use sql alchemy to query the database.
demo query-db

# clean up once done and drop the database
demo drop-db
```

The database connection details including password are loaded from a config file alembic.ini but could asily be passed as a CLI command argument or environment variable.

# Database migrations

To enable you to manage a production database over time you can use alembic to migrate the data schema. Migrations are the .py files in the `/migrations` folder. The `alembic.ini` file configures the database connection string and the location of the migrations folder. Usw the `alembic` command line tool to add and run the migrations.

```bash
# remove the existing sample if already created using sqlalchemy
dropdb sampleDb -h localhost -U postgres
createdb sampleDb -h localhost -U postgres

# upgrade an empty database to the latest version
alembic upgrade head

# generate a SQL script so you can apply the migration manually
alembic upgrade head --sql > upgrade.sql

# create a new migration by detetcing changes in the ORM. Will create a new file in the migrations folder
alembic revision --autogenerate -m "Added some table or column"
```

## IDE, Docker, Python

The app uses VS code with docker the devcontainers feature to setup a python environment with all tools preinstalled. All you need is vscode and docker to be able develop.

You can connect to the database externally using Azure data studio or some other database tool on 127.0.0.1:5432 as well as using sqltools from within VSCode.


## Command line database access

It is also possible to connect to the database from the command line using psql which is pre-installed in the dev container. The database is exposed on port 5432 on localhost and host "db". The password is in the alembic.ini file.

```bash
$ psql -U postgres -p 5432 -h db -d sampleDb
Password for user postgres:
psql (15.3 (Debian 15.3-0+deb12u1))
Type "help" for help.
                      ^
sampleDb=# SELECT * FROM user_account;
 id |   name    |       fullname
----+-----------+-----------------------
  1 | spongebob | Spongebob Squarepants
  2 | sandy     | Sandy Cheeks
  3 | patrick   | Patrick Star
(3 rows)

sampleDb=# exit
```

## Tools - poetry, pyenv, SQLAlchemy etc

All these tools are preinstalled in the dev container:

- **Python3** - multiple versions installed and available, managed using pyenv
- **Poetry** - tool to manage python dependencies, tools and package
- **SQLAlchemy** - ORM to access the database
- **Alembic** - database migrations
- **isort, black and flake8** - configured to lint and tidy up your python code automatically. Executed using ./build.sh and CTRL+SHIFT+B (build in vscode)


## appsmith

A container for appsmith has been added to the docker compose tile. The UI is available at http://localhost:80, and it can connect to the database on host "db" on port 5432. The password is in the alembic.ini file.

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
