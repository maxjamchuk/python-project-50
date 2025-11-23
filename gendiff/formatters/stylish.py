from typing import Any

from gendiff.diff_tree import DiffNode

INDENT_SIZE = 4
SYMBOL_OFFSET = 2


def to_str(value: Any) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    if value is None:
        return "null"
    return str(value)


def format_value(value: Any, depth: int) -> str:
    if not isinstance(value, dict):
        return to_str(value)

    indent = " " * (depth * INDENT_SIZE)
    closing_indent = " " * ((depth - 1) * INDENT_SIZE)

    lines = ["{"]
    for key in sorted(value.keys()):
        val_str = format_value(value[key], depth + 1)
        lines.append(f"{indent}{key}: {val_str}")
    lines.append(f"{closing_indent}}}")
    return "\n".join(lines)


def _format_nodes(nodes: list[DiffNode], depth: int) -> str:
    lines: list[str] = ["{"]
    current_indent = " " * (depth * INDENT_SIZE - SYMBOL_OFFSET)
    closing_indent = " " * ((depth - 1) * INDENT_SIZE)

    for node in nodes:
        node_type = node["type"]
        key = node["key"]

        if node_type == "nested":
            children_str = _format_nodes(node["children"], depth + 1)
            lines.append(f"{current_indent}  {key}: {children_str}")
        elif node_type == "added":
            value_str = format_value(node["value"], depth + 1)
            lines.append(f"{current_indent}+ {key}: {value_str}")
        elif node_type == "removed":
            value_str = format_value(node["value"], depth + 1)
            lines.append(f"{current_indent}- {key}: {value_str}")
        elif node_type == "unchanged":
            value_str = format_value(node["value"], depth + 1)
            lines.append(f"{current_indent}  {key}: {value_str}")
        elif node_type == "updated":
            old_str = format_value(node["old_value"], depth + 1)
            new_str = format_value(node["new_value"], depth + 1)
            lines.append(f"{current_indent}- {key}: {old_str}")
            lines.append(f"{current_indent}+ {key}: {new_str}")

    lines.append(f"{closing_indent}}}")
    return "\n".join(lines)


def format_stylish(tree: list[DiffNode]) -> str:
    return _format_nodes(tree, depth=1)
