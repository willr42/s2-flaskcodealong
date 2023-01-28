from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import click

# Setup
app = Flask(__name__)
app.config.from_object("config.app_config")

# Models
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Book(db.Model):
    __tablename__ = "books"
    book_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    genre = db.Column(db.String())
    length = db.Column(db.Integer)
    year = db.Column(db.Integer)


class BookSchema(ma.Schema):
    class Meta:
        fields = ("book_id", "title", "genre", "length", "year")


book_schema = BookSchema()
books_schema = BookSchema(many=True)


@app.cli.command("create")
def create_db():
    db.create_all()
    print("Tables created")


@app.cli.command("drop")
def drop_db():
    if click.confirm("Are you sure you want to drop all tables?", False):
        db.drop_all()
        print("Tables dropped")


@app.cli.command("seed")
def seed_db():

    # Create book objects
    book1 = Book(
        title="Harry Potter & the Philosopher's Stone",
        genre="fantasy",
        length=400,
        year=1999,
    )
    book2 = Book(
        title="Dune",
        genre="fantasy",
        length=600,
        year=1987,
    )
    db.session.add_all([book1, book2])
    db.session.commit()
