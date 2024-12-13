import os
import json


def read_json():
    script_dir = os.path.dirname(__file__)
    filepath = os.path.join(script_dir, "json.json")
    with open(filepath, "r") as file:
        data = json.load(file)
    return data
