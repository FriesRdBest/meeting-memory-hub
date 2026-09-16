from datetime import datetime

from models.pattern import Pattern


def calculate_confidence(pattern: Pattern) -> str:
    if pattern.evidence_count >= 5:
        return "High"

    if pattern.evidence_count >= 3:
        return "Medium"

    return "Early"


def apply_review(
    pattern: Pattern,
    decision: str,
    reviewer: str,
    review_note: str,
) -> None:
    status_by_decision = {
        "Confirm pattern": "Confirmed",
        "Keep watching": "Emerging",
        "Dismiss for now": "Dismissed",
    }

    pattern.status = status_by_decision[decision]
    pattern.confidence = calculate_confidence(pattern)
    pattern.reviewed_by = reviewer.strip() or "Unassigned reviewer"
    pattern.review_note = review_note.strip()
    pattern.reviewed_at = datetime.now().strftime("%b %d, %Y at %I:%M %p")


def create_emerging_pattern() -> Pattern:
    return Pattern(
        id="PAT-001",
        title="Onboarding friction is recurring",
        category="Customer experience",
        trend="Increasing",
        status="Emerging",
        confidence="Early",
        source_signal_ids=["SIG-001", "SIG-004", "SIG-006"],
        source_action_ids=["ACT-DEMO-001"],
        source_reflection_ids=["LRN-001"],
        affected_accounts=4,
        proposed_owner="Customer Success",
        proposed_destination="Product discovery",
        description="Early workflow friction is recurring for new teams.",
    )


def test_confirm_pattern_records_human_review() -> None:
    pattern = create_emerging_pattern()

    apply_review(
        pattern=pattern,
        decision="Confirm pattern",
        reviewer="Robin Sylvester",
        review_note="The linked evidence supports a repeatable onboarding risk.",
    )

    assert pattern.status == "Confirmed"
    assert pattern.confidence == "High"
    assert pattern.reviewed_by == "Robin Sylvester"
    assert (
        pattern.review_note
        == "The linked evidence supports a repeatable onboarding risk."
    )
    assert pattern.reviewed_at


def test_keep_watching_preserves_emerging_status() -> None:
    pattern = create_emerging_pattern()

    apply_review(
        pattern=pattern,
        decision="Keep watching",
        reviewer="Robin Sylvester",
        review_note="Wait for another completed outcome before confirming.",
    )

    assert pattern.status == "Emerging"
    assert pattern.confidence == "High"
    assert pattern.reviewed_by == "Robin Sylvester"
    assert (
        pattern.review_note == "Wait for another completed outcome before confirming."
    )


def test_dismiss_for_now_preserves_evidence_for_future_review() -> None:
    pattern = create_emerging_pattern()

    apply_review(
        pattern=pattern,
        decision="Dismiss for now",
        reviewer="Robin Sylvester",
        review_note="Current evidence is related but not consistent enough.",
    )

    assert pattern.status == "Dismissed"
    assert pattern.evidence_count == 5
    assert pattern.source_signal_ids == ["SIG-001", "SIG-004", "SIG-006"]
    assert pattern.source_action_ids == ["ACT-DEMO-001"]
    assert pattern.source_reflection_ids == ["LRN-001"]
    assert pattern.reviewed_by == "Robin Sylvester"


def test_blank_reviewer_uses_accountable_placeholder() -> None:
    pattern = create_emerging_pattern()

    apply_review(
        pattern=pattern,
        decision="Keep watching",
        reviewer="   ",
        review_note="",
    )

    assert pattern.reviewed_by == "Unassigned reviewer"
    assert pattern.review_note == ""
    assert pattern.reviewed_at
