# Third party imports
import pandas as pd
from sqlalchemy import TEXT, DATE, INTEGER

class DataLoader:
    def __init__(self, client, df):
        self.client = client
        self.df = df
    
    def increment_id(self):
        self.df["id"] = self.client.get_current_index()
        return self.df

    def load_to_database(self):
        
        df = self.increment_id()

        dtypes = {
            "id": INTEGER,
            "date": DATE,
            "place": TEXT,
            "original": TEXT,
            "source": TEXT,
            "tag": TEXT,
            "title": TEXT,
            "subtitle": TEXT,
            "author": TEXT,
            "article": TEXT,
            "additional": TEXT,
            "link": TEXT
        }

        df.to_sql(name="Articles", 
                  con=self.client.conn,
                  index_label="id",
                  if_exists="append",
                  index=False,
                  dtype=dtypes
        )
        print(self.client.get_current_entries())