from __future__ import annotations

import json
from pathlib import Path


def read_records(file_path: Path) -> list[dict[str, object]]:
    if not file_path.exists():
        return []

    with file_path.open("r", encoding="utf-8") as file:
        content = file.read().strip()

    if not content:
        return []

    records = json.loads(content)

    if not isinstance(records, list):
        raise ValueError(
            f"Expected a list of records in {file_path}, but found another type."
        )

    return [record for record in records if isinstance(record, dict)]


def write_records(
    file_path: Path,
    records: list[dict[str, object]],
) -> None:
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with file_path.open("w", encoding="utf-8") as file:
        json.dump(
            records,
            file,
            ensure_ascii=False,
            indent=2,
        )
        file.write("\n")
