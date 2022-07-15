import json

def load_last_parameters(default_parameters: dict, path: str):
    """TODO: Docstring for load_last_parameters.
    :
    :returns: TODO

    """

    parameters = dict(default_parameters)
    try:
        with open(LAST_PARAMETERS_FILE, 'r') as myfile:
            last_parameters = json.load(myfile)
        for key, el in last_parameters.items():
            if key in parameters:
                parameters[key] = el
    except EOFError:
        print('last parameter file is probably empty..')
    except IOError:
        print('could not access or find last parameter file')

    return parameters
