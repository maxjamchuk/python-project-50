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
