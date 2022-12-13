"""
A simple exchange package that uses a json file
to allow two proceses exchange information
"""

import json

_NAME = "./source/exc.json"

def leave_message(key:str, value:str) -> None:
    with open(_NAME, "r") as f:
        data = json.load(f)
    data[key] = value
    with open(_NAME, "w") as f:
        json.dump(data, f, indent=2)

def read_message(key:str)->None:
    with open(_NAME, "r") as f:
        data = json.load(f)
    return data[key]

