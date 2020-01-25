import json
PARAMETERS_FILE_NAME = 'parameters.json'

def load_parameters():
    with open(PARAMETERS_FILE_NAME) as f:
        parameters = json.load(f)
    return parameters

parameters = load_parameters()