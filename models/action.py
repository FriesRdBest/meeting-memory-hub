from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass
class Action:
    id: str
    signal_id: str
    title: str
    description: str
    owner: str
    destination: str
    status: str
    due_date: str
    created_at: str

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> "Action":
        return cls(
            id=data["id"],
            signal_id=data["signal_id"],
            title=data["title"],
            description=data["description"],
            owner=data["owner"],
            destination=data["destination"],
            status=data["status"],
            due_date=data["due_date"],
            created_at=data["created_at"],
        )

    def to_dict(self) -> dict[str, str]:
        return asdict(self)
