from models.pattern import Pattern


def create_minimal_pattern() -> Pattern:
    return Pattern(
        id="PAT-001",
        title="Onboarding friction is recurring",
        category="Customer experience",
        trend="Increasing",
        status="Emerging",
        confidence="Early",
        source_signal_ids=["SIG-001", "SIG-004"],
        source_action_ids=["ACT-001"],
        source_reflection_ids=["LRN-001"],
        affected_accounts=4,
        proposed_owner="Customer Success",
        proposed_destination="Product discovery",
        description="Early workflow friction is recurring for new teams.",
    )


def test_pattern_requires_at_least_one_signal() -> None:
    pattern = create_minimal_pattern()
    pattern.source_signal_ids = []

    assert pattern.evidence_count == 0


def test_pattern_evidence_count_includes_signals_actions_and_reflections() -> None:
    pattern = create_minimal_pattern()

    assert pattern.evidence_count == 4  # 2 signals + 1 action + 1 reflection


def test_pattern_preserves_linked_evidence_when_status_changes() -> None:
    pattern = create_minimal_pattern()

    original_signals = list(pattern.source_signal_ids)
    original_actions = list(pattern.source_action_ids)
    original_reflections = list(pattern.source_reflection_ids)

    pattern.status = "Confirmed"

    assert pattern.source_signal_ids == original_signals
    assert pattern.source_action_ids == original_actions
    assert pattern.source_reflection_ids == original_reflections


def test_pattern_supports_multiple_signals_actions_and_reflections() -> None:
    pattern = create_minimal_pattern()

    pattern.source_signal_ids.extend(["SIG-007", "SIG-008"])
    pattern.source_action_ids.append("ACT-005")
    pattern.source_reflection_ids.append("LRN-003")

    assert pattern.source_signal_ids == ["SIG-001", "SIG-004", "SIG-007", "SIG-008"]
    assert pattern.source_action_ids == ["ACT-001", "ACT-005"]
    assert pattern.source_reflection_ids == ["LRN-001", "LRN-003"]
    assert pattern.evidence_count == 7  # 4 signals + 2 actions + 1 reflection
