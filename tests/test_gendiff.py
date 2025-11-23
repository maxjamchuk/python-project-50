import json
from pathlib import Path

from gendiff import generate_diff

FIXTURES_DIR = Path(__file__).parent / "test_data"


def read_file(path: Path) -> str:
    return path.read_text().strip()


def test_generate_diff_flat_json() -> None:
    file1 = FIXTURES_DIR / "file1.json"
    file2 = FIXTURES_DIR / "file2.json"
    expected = read_file(FIXTURES_DIR / "expected_flat.txt")
    diff = generate_diff(str(file1), str(file2))
    assert diff == expected


def test_generate_diff_flat_yaml() -> None:
    file1 = FIXTURES_DIR / "file1.yml"
    file2 = FIXTURES_DIR / "file2.yml"
    expected = read_file(FIXTURES_DIR / "expected_flat.txt")

    diff = generate_diff(str(file1), str(file2))

    assert diff == expected


def test_generate_diff_nested_json_stylish() -> None:
    file1 = FIXTURES_DIR / "nested1.json"
    file2 = FIXTURES_DIR / "nested2.json"
    expected = read_file(FIXTURES_DIR / "expected_stylish_nested.txt")

    diff = generate_diff(str(file1), str(file2), format_name="stylish")

    assert diff == expected


def test_generate_diff_nested_yaml_stylish() -> None:
    file1 = FIXTURES_DIR / "nested1.yml"
    file2 = FIXTURES_DIR / "nested2.yml"
    expected = read_file(FIXTURES_DIR / "expected_stylish_nested.txt")

    diff = generate_diff(str(file1), str(file2))

    assert diff == expected


def test_generate_diff_nested_json_plain() -> None:
    file1 = FIXTURES_DIR / "nested1.json"
    file2 = FIXTURES_DIR / "nested2.json"
    expected = read_file(FIXTURES_DIR / "expected_plain.txt")

    diff = generate_diff(str(file1), str(file2), format_name="plain")

    assert diff == expected


def test_generate_diff_nested_json_json_format() -> None:
    file1 = FIXTURES_DIR / "nested1.json"
    file2 = FIXTURES_DIR / "nested2.json"

    raw = generate_diff(str(file1), str(file2), format_name="json")
    data = json.loads(raw)

    assert isinstance(data, list)

    common_nodes = [node for node in data if node["key"] == "common"]
    assert len(common_nodes) == 1
    common = common_nodes[0]
    assert common["type"] == "nested"
    assert isinstance(common["children"], list)

    follow_nodes = [n for n in common["children"] if n["key"] == "follow"]
    assert len(follow_nodes) == 1
    follow = follow_nodes[0]
    assert follow["type"] == "added"
    assert follow["value"] is False

    group1_nodes = [node for node in data if node["key"] == "group1"]
    assert len(group1_nodes) == 1
    group1 = group1_nodes[0]
    baz_nodes = [n for n in group1["children"] if n["key"] == "baz"]
    assert len(baz_nodes) == 1
    baz = baz_nodes[0]
    assert baz["type"] == "updated"
    assert baz["old_value"] == "bas"
    assert baz["new_value"] == "bars"
