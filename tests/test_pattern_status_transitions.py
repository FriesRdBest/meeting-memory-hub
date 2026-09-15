from models.pattern import Pattern


def create_emerging_pattern() -> Pattern:
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


def test_pattern_can_transition_from_emerging_to_confirmed() -> None:
    pattern = create_emerging_pattern()
    pattern.status = "Confirmed"

    assert pattern.status == "Confirmed"


def test_pattern_can_transition_from_emerging_to_dismissed() -> None:
    pattern = create_emerging_pattern()
    pattern.status = "Dismissed"

    assert pattern.status == "Dismissed"


def test_pattern_can_transition_from_confirmed_to_dismissed() -> None:
    pattern = create_emerging_pattern()
    pattern.status = "Confirmed"
    pattern.status = "Dismissed"

    assert pattern.status == "Dismissed"


def test_pattern_can_transition_from_dismissed_back_to_emerging() -> None:
    pattern = create_emerging_pattern()
    pattern.status = "Dismissed"
    pattern.status = "Emerging"

    assert pattern.status == "Emerging"


def test_pattern_status_change_does_not_clear_review_metadata() -> None:
    pattern = create_emerging_pattern()
    pattern.review_note = "Initial review note"
    pattern.reviewed_by = "Robin Sylvester"
    pattern.reviewed_at = "Sep 15, 2026 at 02:00 PM"

    pattern.status = "Confirmed"

    assert pattern.review_note == "Initial review note"
    assert pattern.reviewed_by == "Robin Sylvester"
    assert pattern.reviewed_at == "Sep 15, 2026 at 02:00 PM"


def test_pattern_status_change_does_not_drop_linked_evidence() -> None:
    pattern = create_emerging_pattern()
    pattern.source_signal_ids.append("SIG-002")
    pattern.source_action_ids.append("ACT-001")
    pattern.source_reflection_ids.append("LRN-001")

    original_signals = list(pattern.source_signal_ids)
    original_actions = list(pattern.source_action_ids)
    original_reflections = list(pattern.source_reflection_ids)

    pattern.status = "Confirmed"

    assert pattern.source_signal_ids == original_signals
    assert pattern.source_action_ids == original_actions
    assert pattern.source_reflection_ids == original_reflections
