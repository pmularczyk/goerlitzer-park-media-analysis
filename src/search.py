# Standard library imports
import re
import json
import argparse
from pathlib import Path
from os.path import dirname
from pprint import pprint

# Local application imports
from utils.utils import remove_umlaute
from client.client import Client

def get_data_as_json():
    client = Client()
    df = client.get_current_entries()
    
    output = list()
    for row, col in df.iterrows():
        obj = {
            "id": col["id"],
            "date": col["date"],
            "place": col["place"],
            "original": col["original"],
            "source": col["source"],
            "tag": col["tag"],
            "title": col["title"],
            "subtitle": col["subtitle"],
            "author": col["author"],
            "article": col["article"],
            "additional": col["additional"],
            "link": col["link"]
        }
        output.append(obj)
    return output

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--word', type=str, required=True, help='Enter the word you are searching for')
    args = parser.parse_args()
    return args

def get_output_path(word):
    current = Path(dirname(__file__)).absolute()
    project_path = current.parent
    result = project_path.joinpath("out").joinpath("res")
    output_path = result.joinpath(word)
    return output_path



if __name__ == "__main__":
    data = get_data_as_json()
    args = parse_arguments()

    word = args.word.lower()
    search_with = r"\b" + word + r"\b"

    output = list()
    for article in data:
        repl_pattern = "\W+"

        title = "" if article["title"] is None else article["title"]
        subtitle = "" if article["subtitle"] is None else article["subtitle"]

        # ---------------- Create Theme ---------------- #
        if title == "" and subtitle == "" and article["source"] == "Twitter":
            theme = str(article["date"]) + "_" + article["author"]
            theme = re.sub("-", "_", theme).lower()
        elif title == "" and subtitle == "" and article["source"] != "Twitter":
            theme = Path(article["link"]).name.replace(".html", "")
            theme = str(article["date"]) + "_" + theme
            theme = re.sub(repl_pattern, "_", theme).lower()
        else:
            theme = str(article["date"]) + "_" + title + " " + subtitle
            theme = re.sub(repl_pattern, "_", theme).lower()

        # ---------------- Create Complete Title ---------------- #
        if title == "" and subtitle == "" and article["source"] == "Twitter":
            continue
        elif title == "" and subtitle == "" and article["source"] != "Twitter":
            continue
        else:
            complete_title = title + " " + subtitle

        id = article["id"]
        art = article["article"].lower()
        source = article["source"]

        matches = re.findall(search_with, art)
        match_title = re.findall(search_with, complete_title)

        count_matches = len(matches)
        count_title_matches = len(match_title)
        if count_matches == 0:
            result = None
        else:
            result = count_matches
        
        if count_title_matches == 0:
            title_result = None
        else:
            title_result = count_title_matches
        
        obj = {
            "id": id,
            "source": source,
            "theme": theme,
            word: {
                "Matches in Article": result,
                "Matches in Title": title_result
            }
        }
        output.append(obj)

    found = list(filter(lambda d: d[word]['Matches in Article'] is not None or d[word]['Matches in Title'], output))
    with open(get_output_path(f"search_word_{word}.json"), "w") as file:
        json.dump(found, file, indent=4)
    pprint(found)
