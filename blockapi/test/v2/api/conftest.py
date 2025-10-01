import json
import os
from typing import Union

import pytest


def read_json_file(file_name: str) -> Union[list, dict]:
    json_path = os.path.abspath(os.path.join(os.path.dirname(__file__), file_name))
    with open(json_path, encoding="utf-8") as f:
        return json.load(f)


def read_file(file_name: str) -> str:
    json_path = os.path.abspath(os.path.join(os.path.dirname(__file__), file_name))
    with open(json_path, encoding="utf-8") as f:
        return f.read()


@pytest.fixture(scope='session')
def vcr_config():
    return {
        'decode_compressed_response': True,
    }
