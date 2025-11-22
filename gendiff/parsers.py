import json
from pathlib import Path
from typing import Any

import yaml


def parse(path: str) -> dict[str, Any]:
    file_path = Path(path)
    ext = file_path.suffix.lower()

    if ext == ".json":
        with file_path.open() as f:
            return json.load(f)

    if ext in {".yml", ".yaml"}:
        with file_path.open() as f:
            return yaml.safe_load(f) or {}

    raise ValueError(f"Unsupported file format: {ext}")
