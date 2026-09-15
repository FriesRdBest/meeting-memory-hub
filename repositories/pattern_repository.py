from __future__ import annotations

from pathlib import Path

from models.pattern import Pattern
from repositories.json_store import read_records, write_records


class PatternRepository:
    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path

    def list_all(self) -> list[Pattern]:
        records = read_records(self.file_path)
        return [Pattern.from_dict(record) for record in records]

    def save_all(self, patterns: list[Pattern]) -> None:
        records = [pattern.to_dict() for pattern in patterns]
        write_records(self.file_path, records)
