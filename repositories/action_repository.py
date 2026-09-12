from __future__ import annotations

from pathlib import Path

from models.action import Action
from repositories.json_store import read_records, write_records


class ActionRepository:
    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path

    def list_all(self) -> list[Action]:
        records = read_records(self.file_path)
        return [Action.from_dict(record) for record in records]

    def save_all(self, actions: list[Action]) -> None:
        records = [action.to_dict() for action in actions]
        write_records(self.file_path, records)
