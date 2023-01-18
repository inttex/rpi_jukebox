import json
import traceback


def load_last_parameters(default_parameters: dict, path: str):
    """TODO: Docstring for load_last_parameters.
    :
    :returns: TODO

    """

    parameters = dict(default_parameters)
    try:
        with open(path, 'r') as myfile:
            last_parameters = json.load(myfile)
        for key, el in last_parameters.items():
            if key in parameters:
                parameters[key] = el
    except EOFError:
        print('last parameter file is probably empty..')
    except IOError:
        print('could not access or find last parameter file', traceback.print_exc())

    return parameters

def save_current_parameters(parameters: dict, path: str):
    """TODO: Docstring for save_current_parameters.

    :parameters: TODO
    :path: TODO
    :returns: TODO

    """
    try:
        with open(path, 'w') as myfile:
            json.dump(parameters, myfile)
    except IOError:
        print('could not access or find last parameter file', traceback.print_exc())
