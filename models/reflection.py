from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass
class Reflection:
    id: str
    action_id: str
    outcome: str
    learning: str
    next_step: str
    recorded_at: str

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> "Reflection":
        return cls(
            id=data["id"],
            action_id=data["action_id"],
            outcome=data["outcome"],
            learning=data["learning"],
            next_step=data["next_step"],
            recorded_at=data["recorded_at"],
        )

    def to_dict(self) -> dict[str, str]:
        return asdict(self)
