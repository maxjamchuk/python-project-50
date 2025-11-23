from typing import Any

from gendiff.diff_tree import DiffNode


def _stringify(value: Any) -> str:
    handlers = {
        dict: lambda _: "[complex value]",
        list: lambda _: "[complex value]",
        bool: lambda v: str(v).lower(),
        type(None): lambda _: "null",
        int: str,
        float: str,
    }

    for t, f in handlers.items():
        if isinstance(value, t):
            return f(value)

    return f"'{value}'"


def _walk(nodes: list[DiffNode], parent_path: str = "") -> list[str]:
    lines = []

    handlers = {
        "added": lambda n, path: f"Property '{path}' was added with value: {_stringify(n['value'])}",
        "removed": lambda n, path: f"Property '{path}' was removed",
        "updated": lambda n, path: (
            f"Property '{path}' was updated. "
            f"From {_stringify(n['old_value'])} to {_stringify(n['new_value'])}"
        ),
    }

    for node in nodes:
        node_type = node["type"]
        key = node["key"]
        path = f"{parent_path}.{key}" if parent_path else key

        if node_type == "nested":
            lines.extend(_walk(node["children"], path))
        elif node_type == "unchanged":
            continue
        else:
            lines.append(handlers[node_type](node, path))

    return lines



def format_plain(tree: list[DiffNode]) -> str:
    lines = _walk(tree)
    return "\n".join(lines)
