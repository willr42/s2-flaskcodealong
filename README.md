# Coding along with Jairo

## Setup

1. `python3 -m venv .venv`
2. `source .venv/bin/activate`
3. `pip install -r requirements.txt` (note I added the python-dotenv package to use the config.py)
4. Set up the `.env.example` file with your database URL, rename to `.env`
5. `flask create`, `flask seed` to create the db tables and seed with data
6. `flask run` to run the app

## Usage

- **GET** `localhost:5000/books`: returns all books in the DB
- **GET** `localhost:5000/books/<id>`: returns book in the DB by ID
- **POST** `localhost:5000/books`: adds book to the database
