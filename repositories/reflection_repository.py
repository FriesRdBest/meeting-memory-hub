from __future__ import annotations

from pathlib import Path

from models.reflection import Reflection
from repositories.json_store import read_records, write_records


class ReflectionRepository:
    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path

    def list_all(self) -> list[Reflection]:
        records = read_records(self.file_path)
        return [Reflection.from_dict(record) for record in records]

    def save_all(self, reflections: list[Reflection]) -> None:
        records = [reflection.to_dict() for reflection in reflections]
        write_records(self.file_path, records)
