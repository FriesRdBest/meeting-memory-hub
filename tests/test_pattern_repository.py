from pathlib import Path

from models.pattern import Pattern
from repositories.pattern_repository import PatternRepository


def test_pattern_repository_returns_empty_list_when_file_does_not_exist(
    tmp_path: Path,
) -> None:
    repository = PatternRepository(tmp_path / "patterns.json")

    assert repository.list_all() == []


def test_pattern_repository_saves_and_loads_patterns(
    tmp_path: Path,
) -> None:
    file_path = tmp_path / "patterns.json"
    repository = PatternRepository(file_path)

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

    repository.save_all([source_pattern])

    restored_patterns = repository.list_all()

    assert restored_patterns == [source_pattern]
    assert file_path.exists()


def test_pattern_repository_preserves_review_information(
    tmp_path: Path,
) -> None:
    file_path = tmp_path / "patterns.json"
    repository = PatternRepository(file_path)

    source_pattern = Pattern(
        id="PAT-002",
        title="Reporting requests are recurring",
        category="Product insight",
        trend="Stable",
        status="Confirmed",
        confidence="High",
        source_signal_ids=["SIG-002", "SIG-005"],
        source_action_ids=[],
        source_reflection_ids=["LRN-002"],
        affected_accounts=3,
        proposed_owner="Product Operations",
        proposed_destination="Roadmap review",
        description="Reporting needs are recurring across conversations.",
        review_note="Evidence is consistent across customer conversations.",
        reviewed_by="Robin Sylvester",
        reviewed_at="Sep 15, 2026 at 02:00 PM",
    )

    repository.save_all([source_pattern])

    restored_pattern = repository.list_all()[0]

    assert restored_pattern.status == "Confirmed"
    assert restored_pattern.reviewed_by == "Robin Sylvester"
    assert (
        restored_pattern.review_note
        == "Evidence is consistent across customer conversations."
    )
    assert restored_pattern.reviewed_at == "Sep 15, 2026 at 02:00 PM"
