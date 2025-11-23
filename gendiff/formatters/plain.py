from typing import Any

from gendiff.diff_tree import DiffNode


def _stringify(value: Any) -> str:
    if isinstance(value, (dict, list)):
        return "[complex value]"
    if isinstance(value, bool):
        return str(value).lower()
    if value is None:
        return "null"
    if isinstance(value, (int, float)):
        return str(value)
    return f"'{value}'"


def _walk(nodes: list[DiffNode], parent_path: str = "") -> list[str]:
    lines: list[str] = []

    for node in nodes:
        node_type = node["type"]
        key = node["key"]
        path = f"{parent_path}.{key}" if parent_path else key

        if node_type == "nested":
            lines.extend(_walk(node["children"], path))
        elif node_type == "added":
            value_str = _stringify(node["value"])
            lines.append(
                f"Property '{path}' was added with value: {value_str}",
            )
        elif node_type == "removed":
            lines.append(
                f"Property '{path}' was removed",
            )
        elif node_type == "updated":
            old_str = _stringify(node["old_value"])
            new_str = _stringify(node["new_value"])
            lines.append(
                (
                    f"Property '{path}' was updated. "
                    f"From {old_str} to {new_str}"
                ),
            )
        elif node_type == "unchanged":
            continue

    return lines


def format_plain(tree: list[DiffNode]) -> str:
    lines = _walk(tree)
    return "\n".join(lines)
