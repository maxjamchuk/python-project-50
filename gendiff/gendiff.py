from typing import Any

from .parsers import parse


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


def generate_diff(first_file: str, second_file: str) -> str:
    first_data = parse(first_file)
    second_data = parse(second_file)
    return build_diff(first_data, second_data)
