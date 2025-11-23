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