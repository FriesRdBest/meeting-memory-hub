from models.pattern import Pattern


def test_pattern_evidence_count_includes_all_linked_sources() -> None:
    pattern = Pattern(
        id="PAT-001",
        title="Ownership is unclear",
        category="Operating model",
        trend="Increasing",
        status="Emerging",
        confidence="Medium",
        source_signal_ids=["SIG-001", "SIG-002"],
        source_action_ids=["ACT-001"],
        source_reflection_ids=["LRN-001", "LRN-002"],
    )

    assert pattern.evidence_count == 5


def test_pattern_can_round_trip_through_dict_data() -> None:
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
        review_note="Keep watching for another completed outcome.",
        reviewed_by="Robin Sylvester",
        reviewed_at="Sep 15, 2026 at 02:00 PM",
    )

    restored_pattern = Pattern.from_dict(source_pattern.to_dict())

    assert restored_pattern == source_pattern


def test_pattern_uses_safe_defaults_for_optional_review_fields() -> None:
    pattern = Pattern.from_dict(
        {
            "id": "PAT-002",
            "title": "Reporting requests are recurring",
            "category": "Product insight",
            "trend": "Stable",
            "status": "Emerging",
            "confidence": "Medium",
        }
    )

    assert pattern.source_signal_ids == []
    assert pattern.source_action_ids == []
    assert pattern.source_reflection_ids == []
    assert pattern.affected_accounts == 0
    assert pattern.proposed_owner == "Unassigned"
    assert pattern.proposed_destination == "Unassigned"
    assert pattern.review_note == ""
    assert pattern.reviewed_by == ""
    assert pattern.reviewed_at == ""
