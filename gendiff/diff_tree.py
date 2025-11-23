from typing import Any, Literal, TypedDict


NodeType = Literal["added", "removed", "unchanged", "updated", "nested"]


class DiffNode(TypedDict, total=False):
    key: str
    type: NodeType
    value: Any
    old_value: Any
    new_value: Any
    children: list["DiffNode"]


def build_diff_tree(first: dict[str, Any], second: dict[str, Any]) -> list[DiffNode]:
    nodes: list[DiffNode] = []
    all_keys = sorted(set(first.keys()) | set(second.keys()))

    for key in all_keys:
        in_first = key in first
        in_second = key in second

        if in_first and not in_second:
            nodes.append(
                DiffNode(
                    key=key,
                    type="removed",
                    value=first[key],
                )
            )
            continue

        if in_second and not in_first:
            nodes.append(
                DiffNode(
                    key=key,
                    type="added",
                    value=second[key],
                )
            )
            continue

        old_value = first[key]
        new_value = second[key]

        if isinstance(old_value, dict) and isinstance(new_value, dict):
            children = build_diff_tree(old_value, new_value)
            nodes.append(
                DiffNode(
                    key=key,
                    type="nested",
                    children=children,
                )
            )
        elif old_value == new_value:
            nodes.append(
                DiffNode(
                    key=key,
                    type="unchanged",
                    value=old_value,
                )
            )
        else:
            nodes.append(
                DiffNode(
                    key=key,
                    type="updated",
                    old_value=old_value,
                    new_value=new_value,
                )
            )

    return nodes
