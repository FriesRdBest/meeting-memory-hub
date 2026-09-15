from __future__ import annotations

from models.pattern import Pattern
from repositories.pattern_repository import PatternRepository


class PatternService:
    def __init__(self, repository: PatternRepository) -> None:
        self.repository = repository

    def list_patterns(self) -> list[Pattern]:
        return self.repository.list_all()

    def save_patterns(self, patterns: list[Pattern]) -> None:
        self.repository.save_all(patterns)
