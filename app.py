from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Setup
app = Flask(__name__)
app.config.from_object("config.app_config")

# Models
db = SQLAlchemy(app)


class Book(db.Model):
    __tablename__ = "books"
    book_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    genre = db.Column(db.String())
    length = db.Column(db.Integer)
    year = db.Column(db.Integer)
