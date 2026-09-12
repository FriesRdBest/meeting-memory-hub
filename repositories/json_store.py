from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def read_records(file_path: Path) -> list[dict[str, Any]]:
    if not file_path.exists():
        return []

    with file_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def write_records(file_path: Path, records: list[dict[str, Any]]) -> None:
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with file_path.open("w", encoding="utf-8") as file:
        json.dump(records, file, indent=2)
