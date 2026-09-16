from dataclasses import dataclass, field, asdict
from typing import Optional


@dataclass
class Pattern:
    id: str
    title: str
    category: str
    trend: str
    status: str
    confidence: str
    source_signal_ids: list[str]
    source_action_ids: list[str]
    source_reflection_ids: list[str]
    affected_accounts: int
    proposed_owner: str
    proposed_destination: str
    description: str = ""
    review_note: str = ""
    reviewed_by: str = ""
    reviewed_at: str = ""

    def __post_init__(self) -> None:
        # Ensure list fields are lists (defensive, in case mutable default was passed)
        if not isinstance(self.source_signal_ids, list):
            object.__setattr__(self, "source_signal_ids", list(self.source_signal_ids))
        if not isinstance(self.source_action_ids, list):
            object.__setattr__(self, "source_action_ids", list(self.source_action_ids))
        if not isinstance(self.source_reflection_ids, list):
            object.__setattr__(self, "source_reflection_ids", list(self.source_reflection_ids))

    @property
    def evidence_count(self) -> int:
        return (
            len(self.source_signal_ids)
            + len(self.source_action_ids)
            + len(self.source_reflection_ids)
        )

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Pattern":
        return cls(
            id=data["id"],
            title=data["title"],
            category=data["category"],
            trend=data["trend"],
            status=data["status"],
            confidence=data["confidence"],
            source_signal_ids=data.get("source_signal_ids", []),
            source_action_ids=data.get("source_action_ids", []),
            source_reflection_ids=data.get("source_reflection_ids", []),
            affected_accounts=data.get("affected_accounts", 0),
            proposed_owner=data.get("proposed_owner", ""),
            proposed_destination=data.get("proposed_destination", ""),
            description=data.get("description", ""),
            review_note=data.get("review_note", ""),
            reviewed_by=data.get("reviewed_by", ""),
            reviewed_at=data.get("reviewed_at", ""),
        )
