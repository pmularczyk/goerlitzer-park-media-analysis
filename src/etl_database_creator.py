# Standard library imports
from pathlib import Path

# Third party imports
from sqlalchemy import create_engine

def create_table(path):
    db_uri = f"sqlite:///{path}"
    engine = create_engine(db_uri)
    # create table
    engine.execute('CREATE TABLE "Articles" ('
                   'id INTEGER NOT NULL,'
                   'date DATE,'
                   'place TEXT,'
                   'original TEXT,'
                   'source TEXT,'
                   'tag TEXT,'
                   'title TEXT,'
                   'subtitle TEXT,'
                   'author TEXT,'
                   'article TEXT NOT NULL,'
                   'additional TEXT,'
                   'link TEXT,'
                   'PRIMARY KEY (id));'
    )
    print(f"Database created in: {path}")

if __name__ == "__main__":

    current = Path(__file__).absolute().parent.parent
    db_dir = current.joinpath("database")
    db_name = "db.sqlite"
    db_path = db_dir.joinpath(db_name)

    create_table(db_path)