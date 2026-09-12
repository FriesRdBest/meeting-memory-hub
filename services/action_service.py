from __future__ import annotations

from models.action import Action
from repositories.action_repository import ActionRepository


class ActionService:
    def __init__(self, repository: ActionRepository) -> None:
        self.repository = repository

    def list_actions(self) -> list[Action]:
        return self.repository.list_all()

    def save_actions(self, actions: list[Action]) -> None:
        self.repository.save_all(actions)
