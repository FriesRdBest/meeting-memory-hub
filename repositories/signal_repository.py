from __future__ import annotations

from pathlib import Path

from models.signal import Signal
from repositories.json_store import read_records, write_records


class SignalRepository:
    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path

    def list_all(self) -> list[Signal]:
        records = read_records(self.file_path)
        return [Signal.from_dict(record) for record in records]

    def save_all(self, signals: list[Signal]) -> None:
        records = [signal.to_dict() for signal in signals]
        write_records(self.file_path, records)
