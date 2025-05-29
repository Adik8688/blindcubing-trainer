import json
import os


def get_data(filepath):
    '''
    Returns content of json file
    '''
    print(filepath)
    if not os.path.exists(filepath):
        return {}
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except:
        raise Exception(f"Problemo with {filepath}")

def save_data(data, filepath):
    '''
    Saves data to the json file
    '''

    data = dict(sorted(data.items()))

    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)