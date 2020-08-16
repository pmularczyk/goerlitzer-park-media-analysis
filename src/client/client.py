# Standard library imports
from pathlib import Path
from os.path import dirname

# Third party imports
import pandas as pd
from sqlalchemy import create_engine

class Client:
    def __init__(self):
        self.conn = create_engine(self.create_connection_string())

    def create_connection_string(self):
        current = Path(dirname(__file__)).absolute()
        db_path = current.parent.parent.joinpath("database").joinpath("db.sqlite")
        connection_uri = f"sqlite:///{db_path}"
        return connection_uri

    def get_current_index(self):
        query = "SELECT COUNT(*) AS n FROM Articles"
        result = pd.read_sql(query, self.conn)
        current = result.values[0][0]
        return current
    
    def get_current_entries(self):
        query = "SELECT * FROM Articles"
        df = pd.read_sql(query, self.conn)
        return df