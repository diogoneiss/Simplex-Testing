import os
from pathlib import Path


def create_full_path(file, currentDir):
    return os.path.join(currentDir, file)

def get_json_input(number: int) -> list:
    """ Retorna a lista dentro do arquivo cases/input.json
    """
    working_directory = os.path.dirname(__file__)
    
    input_path = create_full_path(Path(f"./tests/cases/end2end/{str(number)}"), working_directory)
    output_path = create_full_path(Path(f"./tests/cases/end2end/res-{str(number)}"), working_directory)
    
    test_data = test_data.rawInputs
    return test_data