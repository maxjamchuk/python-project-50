from typing import Any

from .parsers import parse
from .diff_tree import build_diff_tree, DiffNode
from .formatters import format_diff


def to_str(value: Any) -> str:
    match value:
        case bool():
            return str(value).lower()
        case None:
            return "null"
        case _:
            return str(value)


def build_diff(first: dict[str, Any], second: dict[str, Any]) -> str:
    sentinel = object()
    lines: list[str] = ["{"]

    for key in sorted(first.keys() | second.keys()):
        old = first.get(key, sentinel)
        new = second.get(key, sentinel)

        if old is not sentinel and new is not sentinel:
            if old == new:
                lines.append(f"    {key}: {to_str(old)}")
            else:
                lines += [
                    f"  - {key}: {to_str(old)}",
                    f"  + {key}: {to_str(new)}",
                ]
        elif old is not sentinel:
            lines.append(f"  - {key}: {to_str(old)}")
        else:
            lines.append(f"  + {key}: {to_str(new)}")

    lines.append("}")
    return "\n".join(lines)


def generate_diff(
        first_file: str,
        second_file: str,
        format_name: str = "stylish"
    ) -> str:
    first_data: dict[str, Any] = parse(first_file)
    second_data: dict[str, Any] = parse(second_file)
    tree: list[DiffNode] = build_diff_tree(first_data, second_data)
    return format_diff(tree, format_name=format_name)
