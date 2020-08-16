# Third party imports
import pandas as pd
import re
import string
import unicodedata
from os.path import dirname
from datetime import datetime as dt
from pathlib import Path

def remove_accents(data):
    list_of_chars = list()
    for char in unicodedata.normalize('NFKD', data):
        if char in string.printable:
            list_of_chars.append(char)
    result = ''.join(list_of_chars)
    return result

def remove_quotes(data):
    data = data.replace('"', '')
    data = data.replace("'", "")
    return data

def generate_replacement_map():
    umlaute = ['ä', 'Ä', 'ö', 'Ö', 'ü', 'Ü', 'ß']
    replacements = [b'ae', b'Ae', b'oe', b'Oe', b'ue', b'Ue', b'ss']
    length = len(umlaute)
    replacement_map = {umlaute[i].encode(): replacements[i] for i in range(length)}
    return replacement_map

def remove_umlaute(data):
    data = data.encode()
    for key, value in generate_replacement_map().items():
        data = data.replace(key, value)
    result = data.decode('utf-8')
    return result

def get_input_file(file):
    current = Path(dirname(__file__)).absolute()
    project_path = current.parent.parent
    xls_data = project_path.joinpath("resources").joinpath("raw_xls")
    input_file = xls_data.joinpath(file)
    return input_file

def get_output_path(source):
    current = Path(dirname(__file__)).absolute()
    project_path = current.parent.parent
    xls_data = project_path.joinpath("resources").joinpath("articles")
    output_path = xls_data.joinpath(source)
    return output_path

week = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']
week_mapping = {idx: element for idx, element in enumerate(week)}

top = """<?xml version="1.0" encoding="UTF-8"?>
<root>"""
bottom = "</root>"

path = get_input_file("Facebook_Analyse.xls")
out_path = get_output_path("facebook_articles")

df = pd.read_excel(path, parse_dates=[1])
df = df.fillna(0)


for row, col in df.iterrows():
    if isinstance(col["Date"], int):
        continue
    elif isinstance(col["Article"], int):
        continue
    else:
        date = col["Date"].date()
        weekday = col["Date"].date().weekday()
        week_day_abbr = week_mapping[weekday]
        date_tag = "<Date> " + week_day_abbr + " " + str(date) + "</Date>"
        
        source = "" if col["Source"] == 0 else remove_accents(remove_umlaute(col["Source"]))
        source_tag = "<Source> " + source +  "</Source>"
        
        place =  "" if col["Place"] == 0 else remove_accents(remove_umlaute(col["Place"]))
        place_tag = "<Place> " + place +  "</Place>"
        
        subtitle = "" if col["Subtitle"] == 0 else remove_accents(remove_umlaute(col["Subtitle"]))
        subtitle_tag = "<Subtitle> " + subtitle +  "</Subtitle>"
        
        title = "" if col["Title"] == 0 else remove_accents(remove_umlaute(col["Title"]))
        title_tag = "<Title> " + title +  "</Title>"
        
        author = "" if col["Author"] == 0 else remove_accents(remove_umlaute(col["Author"]))
        author_tag = "<Author> " + author +  "</Author>"
        
        orig = "" if col["Original"] == 0 else col["Original"]
        orig_tag = "<Original> " + orig +  "</Original>"
    
        additional = "" if col["Additional"] == 0 else remove_accents(remove_umlaute(col["Additional"]))
        additional_tag = "<Additional> " + additional +  "</Additional>"
        
        article = remove_accents(remove_umlaute(col["Article"]))
        article_tag = "<Article> " + article +  "</Article>"
        
        link = "" if col["Link"] == 0 else col["Link"]
        link_tag = "<Link> " + link +  "</Link>"
        
        content = top + source_tag + date_tag + place_tag + title_tag + subtitle_tag + author_tag + article_tag + additional_tag + link_tag + bottom

        # pattern = "\W+"
        # name = re.sub(pattern, "_", title).lower()
        # name = str(date)+ "_" + name + "_" + str(row + 1)

        name = str(date)+ "_" + author.lower().replace(" ", "_")  # tweets and facebook

        # name = Path(link).name.replace(".html", "") # ZDF
        # name = str(date)+ "_" + name

        filepath = out_path.joinpath(name + ".xml")

        with open(filepath, "w") as file:
            file.write(content)
