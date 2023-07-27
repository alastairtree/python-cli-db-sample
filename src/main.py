"""Main module."""

import typer
import sqlalchemy

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from sqlalchemy.engine import URL
from sqlalchemy_utils import database_exists, create_database, drop_database

from model import User, Address, Base

app = typer.Typer()

url = URL.create(
    drivername="postgresql",
    username="postgres",
    password="mysecretpassword",
    host="host.docker.internal",  # use localhost etc if not inside docker desktop!
    port="5432",
    database="sampleDb",
)


@app.command()
def hello(name: str):
    print(f"Hi {name}!")
    print("sql alc vers: " + sqlalchemy.__version__)


@app.command()
def goodbye(name: str, formal: bool = False):
    if formal:
        print(f"Goodbye Ms. {name}. Have a good day.")
    else:
        print(f"Bye {name}!")


@app.command()
def create_db():
    engine = create_engine(url, echo=True)  # echo for dev to outputing SQL

    if not database_exists(engine.url):
        print("Creating db")
        create_database(engine.url)

    print(f"Db Exists? {database_exists(engine.url)}")

    connection = engine.connect()

    Base.metadata.create_all(engine)

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


@app.command()
def drop_db():
    engine = create_engine(url, echo=True)  # echo for dev to outputing SQL

    if database_exists(engine.url):
        print("Dropping db")
        drop_database(engine.url)

    print(f"Db Exists? {database_exists(engine.url)}")


@app.command()
def query_db():
    engine = create_engine(url, echo=True)  # echo for dev to outputing SQL
    session = Session(engine)

    stmt = select(User).where(User.name.in_(["spongebob", "sandy"]))

    for user in session.scalars(stmt):
        print(user)


if __name__ == "__main__":
    app()  # pragma: no cover
