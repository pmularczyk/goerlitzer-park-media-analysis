# Standard library imports
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from os.path import dirname

# Third party imports
import pandas as pd

# Local application imports
from utils.utils import to_datetime, remove_umlaute, remove_accents, remove_quotes


def get_template():
    current = Path(dirname(__file__)).absolute()
    filepath = current.parent.joinpath("config").joinpath("template.json")
    with open(filepath, "r") as json_file:
        template = json.load(json_file)
    return template

def parse_xml(filepath):
    tree = ET.parse(filepath)
    root = tree.getroot()

    # create dictionary
    data = {element.tag.lower(): element.text for element in root}
    data = {key: value.strip().replace("\n", " ") for key, value in data.items() if value is not None}
    data = {key: remove_umlaute(value) for key, value in data.items()}
    data = {key: remove_accents(value) for key, value in data.items()}
    data = {key: remove_quotes(value) for key, value in data.items()}
    return data

def create_dataframe(data):
    # process date string
    date = to_datetime(data["date"])
    data["date"] = date

    # get template and fill template with data
    template = get_template()
    template.update(data)

    # create dataframe
    df = pd.DataFrame([template])
    return df