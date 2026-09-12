from __future__ import annotations

from models.signal import Signal
from repositories.signal_repository import SignalRepository


class SignalService:
    def __init__(self, repository: SignalRepository) -> None:
        self.repository = repository

    def list_signals(self) -> list[Signal]:
        return self.repository.list_all()

    def save_signals(self, signals: list[Signal]) -> None:
        self.repository.save_all(signals)
