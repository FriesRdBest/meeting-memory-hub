from pathlib import Path

from models.pattern import Pattern
from repositories.pattern_repository import PatternRepository
from services.pattern_service import PatternService


def test_pattern_service_lists_saved_patterns(tmp_path: Path) -> None:
    repository = PatternRepository(tmp_path / "patterns.json")
    service = PatternService(repository)

    source_pattern = Pattern(
        id="PAT-001",
        title="Onboarding friction is recurring",
        category="Customer experience",
        trend="Increasing",
        status="Emerging",
        confidence="High",
        source_signal_ids=["SIG-001", "SIG-004"],
        source_action_ids=["ACT-001"],
        source_reflection_ids=["LRN-001"],
        affected_accounts=4,
        proposed_owner="Customer Success",
        proposed_destination="Product discovery",
        description="Early workflow friction is recurring for new teams.",
    )

    service.save_patterns([source_pattern])

    assert service.list_patterns() == [source_pattern]


def test_pattern_service_saves_human_review_decision(tmp_path: Path) -> None:
    repository = PatternRepository(tmp_path / "patterns.json")
    service = PatternService(repository)

    reviewed_pattern = Pattern(
        id="PAT-002",
        title="Reporting requests are recurring",
        category="Product insight",
        trend="Stable",
        status="Confirmed",
        confidence="High",
        source_signal_ids=["SIG-002", "SIG-005"],
        source_action_ids=["ACT-002"],
        source_reflection_ids=["LRN-002"],
        affected_accounts=3,
        proposed_owner="Product Operations",
        proposed_destination="Roadmap review",
        description="Reporting needs are recurring across conversations.",
        review_note="The evidence supports roadmap discovery.",
        reviewed_by="Robin Sylvester",
        reviewed_at="Sep 15, 2026 at 02:10 PM",
    )

    service.save_patterns([reviewed_pattern])

    restored_pattern = service.list_patterns()[0]

    assert restored_pattern.status == "Confirmed"
    assert restored_pattern.reviewed_by == "Robin Sylvester"
    assert restored_pattern.review_note == "The evidence supports roadmap discovery."
