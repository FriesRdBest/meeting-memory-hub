from models.pattern import Pattern


def create_base_pattern() -> Pattern:
    return Pattern(
        id="PAT-001",
        title="Onboarding friction is recurring",
        category="Customer experience",
        trend="Increasing",
        status="Emerging",
        confidence="Early",
        source_signal_ids=["SIG-001"],
        source_action_ids=[],
        source_reflection_ids=[],
        affected_accounts=1,
        proposed_owner="Customer Success",
        proposed_destination="Product discovery",
        description="Early workflow friction is recurring for new teams.",
    )


def test_pattern_proposed_owner_can_be_updated() -> None:
    pattern = create_base_pattern()
    pattern.proposed_owner = "Product Operations"

    assert pattern.proposed_owner == "Product Operations"


def test_pattern_proposed_destination_can_be_updated() -> None:
    pattern = create_base_pattern()
    pattern.proposed_destination = "Roadmap review"

    assert pattern.proposed_destination == "Roadmap review"


def test_pattern_owner_and_destination_changes_do_not_affect_evidence() -> None:
    pattern = create_base_pattern()
    pattern.source_signal_ids.extend(["SIG-002", "SIG-003"])
    pattern.source_action_ids.append("ACT-001")
    pattern.source_reflection_ids.append("LRN-001")

    original_signals = list(pattern.source_signal_ids)
    original_actions = list(pattern.source_action_ids)
    original_reflections = list(pattern.source_reflection_ids)

    pattern.proposed_owner = "Product Operations"
    pattern.proposed_destination = "Roadmap review"

    assert pattern.source_signal_ids == original_signals
    assert pattern.source_action_ids == original_actions
    assert pattern.source_reflection_ids == original_reflections


def test_pattern_owner_and_destination_changes_do_not_affect_review_metadata() -> None:
    pattern = create_base_pattern()
    pattern.review_note = "Initial review"
    pattern.reviewed_by = "Robin Sylvester"
    pattern.reviewed_at = "Sep 15, 2026 at 02:00 PM"

    pattern.proposed_owner = "Product Operations"
    pattern.proposed_destination = "Roadmap review"

    assert pattern.review_note == "Initial review"
    assert pattern.reviewed_by == "Robin Sylvester"
    assert pattern.reviewed_at == "Sep 15, 2026 at 02:00 PM"


def test_pattern_supports_various_owner_and_destination_values() -> None:
    pattern = create_base_pattern()

    pattern.proposed_owner = "Engineering"
    pattern.proposed_destination = "Sprint planning"
    assert pattern.proposed_owner == "Engineering"
    assert pattern.proposed_destination == "Sprint planning"

    pattern.proposed_owner = "Design"
    pattern.proposed_destination = "Design system backlog"
    assert pattern.proposed_owner == "Design"
    assert pattern.proposed_destination == "Design system backlog"

    pattern.proposed_owner = "Unassigned"
    pattern.proposed_destination = "Triage queue"
    assert pattern.proposed_owner == "Unassigned"
    assert pattern.proposed_destination == "Triage queue"
