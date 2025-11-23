from gendiff.diff_tree import DiffNode
from .stylish import format_stylish


def format_diff(tree: list[DiffNode], format_name: str = "stylish") -> str:
    if format_name in (None, "stylish"):
        return format_stylish(tree)

    raise ValueError(f"Unknown format: {format_name}")
