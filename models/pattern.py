from dataclasses import dataclass, field


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
    proposed_owner: str = ""
    proposed_destination: str = ""
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
