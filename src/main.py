"""Main module."""

import sqlalchemy
import typer
from alembic import config
from sqlalchemy import create_engine, select
from sqlalchemy.engine import URL
from sqlalchemy.orm import Session
from sqlalchemy_utils import create_database, database_exists, drop_database

from model import Address, Base, User

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = config.Config("alembic.ini")

app = typer.Typer()

# url creds should probably come from environment variables but below you can either hardcode or load from config.
# url = URL.create(
#     drivername="postgresql",
#     username="postgres",
#     password="postgres",
#     host="localhost",
#     port="5432",
#     database="sampleDb",
# )

url = config.get_main_option("sqlalchemy.url")
engine = create_engine(url, echo=True)  # echo for dev to outputing SQL


@app.command()
def create_db():
    print("sql sqlalchemy version: " + sqlalchemy.__version__)

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
    if database_exists(engine.url):
        print("Dropping db")
        drop_database(engine.url)
    else:
        print("Skipped - Db does not exist")


@app.command()
def query_db():
    session = Session(engine)

    stmt = select(User).where(User.name.in_(["spongebob", "sandy"]))

    for user in session.scalars(stmt):
        print(user)


if __name__ == "__main__":
    app()  # pragma: no cover
