from gendiff.diff_tree import DiffNode
from .plain import format_plain
from .stylish import format_stylish


def format_diff(tree: list[DiffNode], format_name: str = "stylish") -> str:
    if format_name in (None, "stylish"):
        return format_stylish(tree)
    if format_name == "plain":
        return format_plain(tree)

    raise ValueError(f"Unknown format: {format_name}")
