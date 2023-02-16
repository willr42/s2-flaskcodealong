from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from swagger_gen.lib.wrappers import swagger_metadata
from swagger_gen.swagger import Swagger
import click

# Setup
app = Flask(__name__)
# Best to read this line in reverse order. The string looks for an app_config object in the config.py file
# Then sets the whole application config to use the fields
# on that provided object.
app.config.from_object("config.app_config")

# Initialise libraries
db = SQLAlchemy(app)
ma = Marshmallow(app)


# Create book model
# This is translated by SQLAlchemy into a DB table & columns (when we run the db.create_all())
class Book(db.Model):
    __tablename__ = "books"
    book_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    genre = db.Column(db.String())
    length = db.Column(db.Integer)
    year = db.Column(db.Integer)


# Create book schema
# This is Marshmallow, it translates a Python object (Book) to a JSON object
class BookSchema(ma.Schema):
    class Meta:
        fields = ("book_id", "title", "genre", "length", "year")


# Here's where we define the actual schemas
book_schema = BookSchema()
books_schema = BookSchema(many=True)


# Command line
@app.cli.command("create")
def create_db():
    db.create_all()
    print("Tables created")


@app.cli.command("drop")
def drop_db():
    # I added this confirmation step
    if click.confirm("Are you sure you want to drop all tables?", False):
        db.drop_all()
        print("Tables dropped")


@app.cli.command("seed")
def seed_db():
    # Create book objects
    book1 = Book(
        title="The Left Hand of Darkness",
        genre="fantasy",
        length=286,
        year=1969,
    )
    book2 = Book(
        title="Dune",
        genre="fantasy",
        length=600,
        year=1987,
    )
    # Insert into database and "save" with commit
    db.session.add_all([book1, book2])
    db.session.commit()


# Route returning all books in DB
@app.route("/books", methods=["GET"])
@swagger_metadata(summary="Get books", description="Returns all books in database")
def get_books():
    # Query DB, store result
    book_list = Book.query.all()
    # Return result in a format that can be understood (JSON)
    return books_schema.dump(book_list)


@app.route("/books/<int:id>", methods=["GET"])
def get_book(id):
    # Query by specific ID as primary key
    book = Book.query.get(id)
    return book_schema.dump(book)


@app.route("/books", methods=["POST"])
def add_book():
    # load the fields from the request JSON
    book_fields = book_schema.load(request.json)

    # Create new empty book
    new_book = Book()

    # dynamically loop over the keys
    for field in book_fields:
        setattr(new_book, field, book_fields[field])

    # or you can just loop over the keys manually as done in class
    #
    # new_book = Book(
    #     title=book_fields["title"],
    #     year=book_fields["year"],
    #     genre=book_fields["genre"],
    #     length=book_fields["length"],
    # )

    # commit to DB
    db.session.add(new_book)
    db.session.commit()

    return book_schema.dump(new_book)


swagger = Swagger(app=app, title="app title")
swagger.configure()
