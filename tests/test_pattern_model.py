from models.pattern import Pattern


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

    assert restored_pattern.id == source_pattern.id
    assert restored_pattern.title == source_pattern.title
    assert restored_pattern.category == source_pattern.category
    assert restored_pattern.trend == source_pattern.trend
    assert restored_pattern.status == source_pattern.status
    assert restored_pattern.confidence == source_pattern.confidence
    assert restored_pattern.source_signal_ids == source_pattern.source_signal_ids
    assert restored_pattern.source_action_ids == source_pattern.source_action_ids
    assert (
        restored_pattern.source_reflection_ids == source_pattern.source_reflection_ids
    )
    assert restored_pattern.affected_accounts == source_pattern.affected_accounts
    assert restored_pattern.proposed_owner == source_pattern.proposed_owner
    assert restored_pattern.proposed_destination == source_pattern.proposed_destination
    assert restored_pattern.description == source_pattern.description
    assert restored_pattern.review_note == source_pattern.review_note
    assert restored_pattern.reviewed_by == source_pattern.reviewed_by
    assert restored_pattern.reviewed_at == source_pattern.reviewed_at


def test_pattern_uses_safe_defaults_for_optional_review_fields() -> None:
    pattern = Pattern.from_dict(
        {
            "id": "PAT-002",
            "title": "Reporting requests are recurring",
            "category": "Product insight",
            "trend": "Stable",
            "status": "Emerging",
            "confidence": "Medium",
            "source_signal_ids": ["SIG-002"],
            "source_action_ids": [],
            "source_reflection_ids": [],
            "affected_accounts": 1,
            "proposed_owner": "",
            "proposed_destination": "",
            "description": "",
        }
    )

    assert pattern.review_note == ""
    assert pattern.reviewed_by == ""
    assert pattern.reviewed_at == ""
