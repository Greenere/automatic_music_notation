import json

_NAME = "exc.json"

def leave_message(key, value):
    with open(_NAME, "r") as f:
        data = json.load(f)
    data[key] = value
    with open(_NAME, "w") as f:
        json.dump(data, f, indent=2)

def read_message(key):
    with open(_NAME, "r") as f:
        data = json.load(f)
    return data[key]

