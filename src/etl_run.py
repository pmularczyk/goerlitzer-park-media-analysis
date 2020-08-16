# Standard library imports
from os import listdir 
from os.path import dirname
from pathlib import Path

# Local application imports
from etl_extract_data import parse_xml, create_dataframe
from etl_load_data import DataLoader
from client.client import Client

def get_filepaths():
    current = Path(dirname(__file__)).absolute()
    project_path = current.parent
    resources = project_path.joinpath("resources").joinpath("articles")
    return resources

def main(directory):
    client = Client()
    for filepath in directory.rglob("*.xml"):
        data = parse_xml(filepath)
        df = create_dataframe(data)
        loader = DataLoader(client, df)
        loader.load_to_database()

if __name__ == "__main__":
    resources = get_filepaths()
    main(resources)