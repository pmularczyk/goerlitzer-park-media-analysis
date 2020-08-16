# Standard library imports
import re
import json
from os.path import dirname
from pathlib import Path

# Third party imports
import pandas as pd

# Local application imports
from utils.utils import remove_umlaute


def save_file(content, filename):
    current = Path(dirname(__file__)).absolute()
    project_path = current.parent
    resources = project_path.joinpath("resources").joinpath("sentiment_words")
    sentiment_words = resources.joinpath(filename)
    with open(sentiment_words, "a") as file:
        file.write(content)

def store_json(output_path, content):
    with open(output_path, 'w') as file:
        file.write(json.dumps(content, indent=4))

def substitution_map():
    to_substitute = ["NN", "VVINF", "ADJX"]
    substitution = ["noun", "verb", "adjective"]
    length = len(to_substitute)
    substitution_map = {to_substitute[i]: substitution[i] for i in range(length)}
    return substitution_map

def substitute(data):
    for key, value in substitution_map().items():
        data = data.replace(key, value)
    return data

def string_to_list(entry):
    if entry.__contains__(","):
        entry = entry.split(",")
    return entry

    # NN = Substantiv, noun
    # VVINF = Verb, verb
    # ADJX = Adjektiv, adjective

    # SentiWS_v1.8b_Negative.txt
    # SentiWS_v1.8b_Positive.txt

# current = Path(dirname(__file__)).absolute().parent
# resources = current.joinpath("resources").joinpath("sentiment_words")
# sentiment_words = resources.joinpath("SentiWS_v1.8b_Positive.txt")

# with open(sentiment_words, "r", encoding="utf-8") as file:    
#     for line in file:
#         formatted = remove_umlaute(line)
#         formatted = formatted.replace("|", "\t")
#         formatted = substitute(formatted)

def load_data(path):
    data = pd.read_csv(path, sep="\t", error_bad_lines=False,
                    names=["word", "type", "score", "flexions"])
    return data

def duplicate_initial_word(data):
    # Copy over first/ initial word
    length = len(data)
    for i in range(length):
        row = ({"word": data.iloc[i]["word"],
                "type": data.iloc[i]["type"],
                "score": data.iloc[i]["score"],
                "flexions": data.iloc[i]["word"]
                })
        data = data.append(row, ignore_index=True)
    # Sorts by category column
    data = data.sort_values(by=["word"]).reset_index(drop=True)
    # Drop rows where initial flexion was empty
    data = data.dropna()
    return data

def unnest_list_of_flexions(data):
    # Unnest list of flexions
    data["flexions"] = data.flexions.apply(string_to_list)
    length = len(data)
    for i in range(length):
        if type(data.iloc[i]["flexions"]) == list and (len(data.iloc[i]["flexions"])) > 1:
            while (len(data.iloc[i]["flexions"])) != 1:
                row = ({"word": data.iloc[i]["word"],
                        "type": data.iloc[i]["type"],
                        "score": data.iloc[i]["score"],
                        "flexions": data.iloc[i]["flexions"].pop()})
                data = data.append(row, ignore_index=True)
    # Remove the list
    data.flexions = data.flexions.apply(
        lambda entry: entry[0] if isinstance(entry, list) else entry)
    return data

def data_to_json(data):
    output = list()
    for row, col in data.iterrows():
        obj = {
            "keyword": col["flexions"],
            "word": col["word"],
            "type": col["type"],
            "score": col["score"]
        }
        output.append(obj)

    result = {element["keyword"]: {"word": element["word"],
                                "type": element["type"],
                                "score": element["score"]} for element in output}
    return result


if __name__ == "__main__":

    path = r"D:\git\Goerli\resources\sentiment_words\negative_words.txt"
    output_path = r"D:\git\Goerli\resources\sentiment_words\negative_words.json"
    data = load_data(path)
    data = duplicate_initial_word(data)
    data = unnest_list_of_flexions(data)
    data = data_to_json(data)
    store_json(output_path, data)

