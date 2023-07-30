"""Main module."""

import typer
import sqlalchemy

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from sqlalchemy.engine import URL
from sqlalchemy_utils import database_exists, create_database, drop_database

from model import User, Address, Base

from alembic import config

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = config.Config("alembic.ini")

app = typer.Typer()

# url = URL.create(
#     drivername="postgresql",
#     username="postgres",
#     password="mysecretpassword",
#     # host="host.docker.internal",  # use this if accessing a docker desktop container outsode the devcontainer!
#     host="localhost",
#     port="5432",
#     database="sampleDb",
# )
url = config.get_main_option("sqlalchemy.url")


@app.command()
def create_db():
    print("sql sqlalchemy version: " + sqlalchemy.__version__)

    engine = create_engine(url, echo=True)  # echo for dev to outputing SQL

    if not database_exists(engine.url):
        print("Creating db")
        create_database(engine.url)
    else:
        print("Db already exists")

    print("Creating all tables")
    Base.metadata.create_all(engine)

    print("Loading some data")
    with Session(engine) as session:
        spongebob = User(
            name="spongebob",
            fullname="Spongebob Squarepants",
            addresses=[Address(email_address="spongebob@sqlalchemy.org")],
        )
        sandy = User(
            name="sandy",
            fullname="Sandy Cheeks",
            addresses=[
                Address(email_address="sandy@sqlalchemy.org"),
                Address(email_address="sandy@squirrelpower.org"),
            ],
        )
        patrick = User(name="patrick", fullname="Patrick Star")
        session.add_all([spongebob, sandy, patrick])
        session.commit()
    print("Database create complete")


@app.command()
def drop_db():
    engine = create_engine(url, echo=True)  # echo for dev to outputing SQL

    if database_exists(engine.url):
        print("Dropping db")
        drop_database(engine.url)
    else:
        print("Skipped - Db does not exist")


@app.command()
def query_db():
    engine = create_engine(url, echo=True)  # echo for dev to outputing SQL
    session = Session(engine)

    stmt = select(User).where(User.name.in_(["spongebob", "sandy"]))

    for user in session.scalars(stmt):
        print(user)


if __name__ == "__main__":
    app()  # pragma: no cover
