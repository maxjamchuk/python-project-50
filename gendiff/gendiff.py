import json
from typing import Any


def read_json(path: str) -> dict[str, Any]:
    with open(path) as f:
        return json.load(f)


def generate_diff(first_file: str, second_file: str) -> str:
    first_data = read_json(first_file)
    second_data = read_json(second_file)

    return str()
