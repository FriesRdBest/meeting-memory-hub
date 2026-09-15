from models.pattern import Pattern


def create_pattern_with_evidence(
    signal_count: int,
    action_count: int,
    reflection_count: int,
) -> Pattern:
    signals = [f"SIG-{i:03d}" for i in range(1, signal_count + 1)]
    actions = [f"ACT-{i:03d}" for i in range(1, action_count + 1)]
    reflections = [f"LRN-{i:03d}" for i in range(1, reflection_count + 1)]

    return Pattern(
        id="PAT-001",
        title="Onboarding friction is recurring",
        category="Customer experience",
        trend="Increasing",
        status="Emerging",
        confidence="Early",
        source_signal_ids=signals,
        source_action_ids=actions,
        source_reflection_ids=reflections,
        affected_accounts=max(1, signal_count),
        proposed_owner="Customer Success",
        proposed_destination="Product discovery",
        description="Early workflow friction is recurring for new teams.",
    )


def test_confidence_is_early_when_total_evidence_is_less_than_three() -> None:
    pattern = create_pattern_with_evidence(
        signal_count=1,
        action_count=1,
        reflection_count=0,
    )

    assert pattern.evidence_count == 2
    assert pattern.confidence == "Early"


def test_confidence_is_medium_when_total_evidence_is_three_or_four() -> None:
    pattern = create_pattern_with_evidence(
        signal_count=2,
        action_count=1,
        reflection_count=1,
    )

    assert pattern.evidence_count == 4
    assert pattern.confidence == "Early"


def test_confidence_is_high_when_total_evidence_is_five_or_more() -> None:
    pattern = create_pattern_with_evidence(
        signal_count=3,
        action_count=1,
        reflection_count=1,
    )

    assert pattern.evidence_count == 5
    assert pattern.confidence == "Early"


def test_confidence_does_not_auto_update_when_evidence_is_added_later() -> None:
    pattern = create_pattern_with_evidence(
        signal_count=1,
        action_count=0,
        reflection_count=0,
    )

    assert pattern.evidence_count == 1
    assert pattern.confidence == "Early"

    pattern.source_signal_ids.extend(["SIG-002", "SIG-003", "SIG-004", "SIG-005"])

    assert pattern.evidence_count == 5
    assert pattern.confidence == "Early"
