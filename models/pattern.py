from __future__ import annotations

from dataclasses import asdict, dataclass, field


@dataclass
class Pattern:
    id: str
    title: str
    category: str
    trend: str
    status: str
    confidence: str
    source_signal_ids: list[str] = field(default_factory=list)
    source_action_ids: list[str] = field(default_factory=list)
    source_reflection_ids: list[str] = field(default_factory=list)
    affected_accounts: int = 0
    proposed_owner: str = "Unassigned"
    proposed_destination: str = "Unassigned"
    description: str = ""
    review_note: str = ""
    reviewed_by: str = ""
    reviewed_at: str = ""

    @property
    def evidence_count(self) -> int:
        return (
            len(self.source_signal_ids)
            + len(self.source_action_ids)
            + len(self.source_reflection_ids)
        )

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "Pattern":
        return cls(
            id=str(data["id"]),
            title=str(data["title"]),
            category=str(data["category"]),
            trend=str(data["trend"]),
            status=str(data["status"]),
            confidence=str(data["confidence"]),
            source_signal_ids=[
                str(signal_id)
                for signal_id in data.get("source_signal_ids", [])
            ],
            source_action_ids=[
                str(action_id)
                for action_id in data.get("source_action_ids", [])
            ],
            source_reflection_ids=[
                str(reflection_id)
                for reflection_id in data.get("source_reflection_ids", [])
            ],
            affected_accounts=int(data.get("affected_accounts", 0)),
            proposed_owner=str(
                data.get("proposed_owner", "Unassigned")
            ),
            proposed_destination=str(
                data.get("proposed_destination", "Unassigned")
            ),
            description=str(data.get("description", "")),
            review_note=str(data.get("review_note", "")),
            reviewed_by=str(data.get("reviewed_by", "")),
            reviewed_at=str(data.get("reviewed_at", "")),
        )

    def to_dict(self) -> dict[str, object]:
        return asdict(self)
