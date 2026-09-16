import json
from pathlib import Path

from models.pattern import Pattern


class PatternRepository:
    def __init__(self, file_path: Path | str) -> None:
        self.file_path = Path(file_path)

    def list_all(self) -> list[Pattern]:
        if not self.file_path.exists():
            return []

        with self.file_path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        return [self._dict_to_pattern(item) for item in data]

    def save_all(self, patterns: list[Pattern]) -> None:
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        data = [self._pattern_to_dict(p) for p in patterns]

        with self.file_path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def _dict_to_pattern(self, data: dict) -> Pattern:
        return Pattern(
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

    def _pattern_to_dict(self, pattern: Pattern) -> dict:
        return {
            "id": pattern.id,
            "title": pattern.title,
            "category": pattern.category,
            "trend": pattern.trend,
            "status": pattern.status,
            "confidence": pattern.confidence,
            "source_signal_ids": pattern.source_signal_ids,
            "source_action_ids": pattern.source_action_ids,
            "source_reflection_ids": pattern.source_reflection_ids,
            "affected_accounts": pattern.affected_accounts,
            "proposed_owner": pattern.proposed_owner,
            "proposed_destination": pattern.proposed_destination,
            "description": pattern.description,
            "review_note": pattern.review_note,
            "reviewed_by": pattern.reviewed_by,
            "reviewed_at": pattern.reviewed_at,
        }
