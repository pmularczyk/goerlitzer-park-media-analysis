# Standard library imports
import re
import string
import unicodedata
from datetime import datetime as dt

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

def to_datetime(date_string):

    assert isinstance(date_string, str), "Input has to be of type string"

    # dots_replaced = date_string.replace(".", "-")
    date_only = re.sub(r"^\w+\s", "", date_string)
    date = dt.strptime(date_only, "%Y-%m-%d").date()
    return date