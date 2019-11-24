import json


def get_credentials(filepath):
    with open(filepath) as file:
        credentials = json.loads(file.read())
    return credentials
