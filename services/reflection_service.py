from __future__ import annotations

from models.reflection import Reflection
from repositories.reflection_repository import ReflectionRepository


class ReflectionService:
    def __init__(self, repository: ReflectionRepository) -> None:
        self.repository = repository

    def list_reflections(self) -> list[Reflection]:
        return self.repository.list_all()

    def save_reflections(self, reflections: list[Reflection]) -> None:
        self.repository.save_all(reflections)
