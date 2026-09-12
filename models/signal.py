from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass
class Signal:
    id: str
    title: str
    type: str
    area: str
    impact: str
    confidence: str
    status: str
    owner: str
    destination: str
    evidence: str
    context: str

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> "Signal":
        return cls(
            id=data["id"],
            title=data["title"],
            type=data["type"],
            area=data["area"],
            impact=data["impact"],
            confidence=data["confidence"],
            status=data["status"],
            owner=data["owner"],
            destination=data["destination"],
            evidence=data["evidence"],
            context=data["context"],
        )

    def to_dict(self) -> dict[str, str]:
        return asdict(self)
