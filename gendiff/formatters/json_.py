import json

from gendiff.diff_tree import DiffNode


def format_json(tree: list[DiffNode]) -> str:
    return json.dumps(tree, indent=2)
