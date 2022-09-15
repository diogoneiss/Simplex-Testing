import pytest
from pathlib import Path

from utils.readJsonData import inject_test_data
import os

def pytest_configure():
    pytest.input_test_data = get_json_input()


def get_json_input() -> list:
    """ Retorna a lista dentro do arquivo cases/input.json
    """
    workingDirectory = os.path.dirname(__file__)
    test_data = inject_test_data(file=Path("./tests/cases/input.json"), currentDir=workingDirectory)
    test_data = test_data.rawInputs
    return test_data