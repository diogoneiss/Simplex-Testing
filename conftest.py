import pytest
import os
from pathlib import Path
from utils.readJsonData import inject_test_data
from utils.logger import setup_logger

def pytest_configure():
    pytest.input_test_data = get_json_input()
    setup_logger()


def get_json_input() -> list:
    """ Retorna a lista dentro do arquivo cases/input.json
    """
    working_directory = os.path.dirname(__file__)
    test_data = inject_test_data(file=Path("./tests/cases/input.json"), currentDir=working_directory)
    test_data = test_data.rawInputs
    return test_data
