import pytest

from models.pattern import Pattern


def create_valid_pattern() -> Pattern:
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


def test_pattern_requires_id() -> None:
    with pytest.raises(TypeError):
        Pattern(
            title="Missing id",
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


def test_pattern_requires_title() -> None:
    with pytest.raises(TypeError):
        Pattern(
            id="PAT-001",
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


def test_pattern_requires_category() -> None:
    with pytest.raises(TypeError):
        Pattern(
            id="PAT-001",
            title="Onboarding friction is recurring",
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


def test_pattern_requires_trend() -> None:
    with pytest.raises(TypeError):
        Pattern(
            id="PAT-001",
            title="Onboarding friction is recurring",
            category="Customer experience",
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


def test_pattern_requires_status() -> None:
    with pytest.raises(TypeError):
        Pattern(
            id="PAT-001",
            title="Onboarding friction is recurring",
            category="Customer experience",
            trend="Increasing",
            confidence="Early",
            source_signal_ids=["SIG-001"],
            source_action_ids=[],
            source_reflection_ids=[],
            affected_accounts=1,
            proposed_owner="Customer Success",
            proposed_destination="Product discovery",
            description="Early workflow friction is recurring for new teams.",
        )


def test_pattern_requires_confidence() -> None:
    with pytest.raises(TypeError):
        Pattern(
            id="PAT-001",
            title="Onboarding friction is recurring",
            category="Customer experience",
            trend="Increasing",
            status="Emerging",
            source_signal_ids=["SIG-001"],
            source_action_ids=[],
            source_reflection_ids=[],
            affected_accounts=1,
            proposed_owner="Customer Success",
            proposed_destination="Product discovery",
            description="Early workflow friction is recurring for new teams.",
        )


def test_pattern_requires_source_signal_ids() -> None:
    with pytest.raises(TypeError):
        Pattern(
            id="PAT-001",
            title="Onboarding friction is recurring",
            category="Customer experience",
            trend="Increasing",
            status="Emerging",
            confidence="Early",
            source_action_ids=[],
            source_reflection_ids=[],
            affected_accounts=1,
            proposed_owner="Customer Success",
            proposed_destination="Product discovery",
            description="Early workflow friction is recurring for new teams.",
        )


def test_pattern_requires_source_action_ids() -> None:
    with pytest.raises(TypeError):
        Pattern(
            id="PAT-001",
            title="Onboarding friction is recurring",
            category="Customer experience",
            trend="Increasing",
            status="Emerging",
            confidence="Early",
            source_signal_ids=["SIG-001"],
            source_reflection_ids=[],
            affected_accounts=1,
            proposed_owner="Customer Success",
            proposed_destination="Product discovery",
            description="Early workflow friction is recurring for new teams.",
        )


def test_pattern_requires_source_reflection_ids() -> None:
    with pytest.raises(TypeError):
        Pattern(
            id="PAT-001",
            title="Onboarding friction is recurring",
            category="Customer experience",
            trend="Increasing",
            status="Emerging",
            confidence="Early",
            source_signal_ids=["SIG-001"],
            source_action_ids=[],
            affected_accounts=1,
            proposed_owner="Customer Success",
            proposed_destination="Product discovery",
            description="Early workflow friction is recurring for new teams.",
        )


def test_pattern_requires_affected_accounts() -> None:
    with pytest.raises(TypeError):
        Pattern(
            id="PAT-001",
            title="Onboarding friction is recurring",
            category="Customer experience",
            trend="Increasing",
            status="Emerging",
            confidence="Early",
            source_signal_ids=["SIG-001"],
            source_action_ids=[],
            source_reflection_ids=[],
            proposed_owner="Customer Success",
            proposed_destination="Product discovery",
            description="Early workflow friction is recurring for new teams.",
        )


def test_pattern_requires_proposed_owner() -> None:
    with pytest.raises(TypeError):
        Pattern(
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
            proposed_destination="Product discovery",
            description="Early workflow friction is recurring for new teams.",
        )


def test_pattern_requires_proposed_destination() -> None:
    with pytest.raises(TypeError):
        Pattern(
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
            description="Early workflow friction is recurring for new teams.",
        )


def test_pattern_requires_description() -> None:
    with pytest.raises(TypeError):
        Pattern(
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
        )


def test_valid_pattern_instantiates_without_error() -> None:
    pattern = create_valid_pattern()

    assert pattern.id == "PAT-001"
    assert pattern.title == "Onboarding friction is recurring"
    assert pattern.category == "Customer experience"
    assert pattern.trend == "Increasing"
    assert pattern.status == "Emerging"
    assert pattern.confidence == "Early"
    assert pattern.source_signal_ids == ["SIG-001"]
    assert pattern.source_action_ids == []
    assert pattern.source_reflection_ids == []
    assert pattern.affected_accounts == 1
    assert pattern.proposed_owner == "Customer Success"
    assert pattern.proposed_destination == "Product discovery"
    assert (
        pattern.description
        == "Early workflow friction is recurring for new teams."
    )
