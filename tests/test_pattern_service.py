from pathlib import Path

from models.action import Action
from models.pattern import Pattern
from models.reflection import Reflection
from models.signal import Signal
from repositories.action_repository import ActionRepository
from repositories.pattern_repository import PatternRepository
from repositories.reflection_repository import ReflectionRepository
from repositories.signal_repository import SignalRepository
from services.action_service import ActionService
from services.pattern_service import PatternService, PatternWithEvidence
from services.reflection_service import ReflectionService
from services.signal_service import SignalService


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


def test_pattern_service_confirm_pattern_updates_status_and_review_fields(
    tmp_path: Path,
) -> None:
    pattern_repo = PatternRepository(tmp_path / "patterns.json")
    service = PatternService(pattern_repo)

    emerging_pattern = Pattern(
        id="PAT-003",
        title="Escalations are recurring",
        category="Support",
        trend="Increasing",
        status="Emerging",
        confidence="Medium",
        source_signal_ids=["SIG-006"],
        source_action_ids=[],
        source_reflection_ids=[],
        affected_accounts=2,
        proposed_owner="Support",
        proposed_destination="Incident review",
        description="Escalation reasons are recurring.",
    )

    service.save_patterns([emerging_pattern])

    confirmed = service.confirm_pattern(
        pattern_id="PAT-003",
        review_note="Consistent evidence across multiple conversations.",
        reviewed_by="Robin Sylvester",
        reviewed_at="Sep 16, 2026 at 01:00 PM",
        proposed_owner="Support Operations",
        proposed_destination="Process review",
    )

    assert confirmed.id == "PAT-003"
    assert confirmed.status == "Confirmed"
    assert confirmed.review_note == "Consistent evidence across multiple conversations."
    assert confirmed.reviewed_by == "Robin Sylvester"
    assert confirmed.reviewed_at == "Sep 16, 2026 at 01:00 PM"
    assert confirmed.proposed_owner == "Support Operations"
    assert confirmed.proposed_destination == "Process review"

    # Ensure persisted
    reloaded = service.list_patterns()[0]
    assert reloaded.status == "Confirmed"
    assert reloaded.reviewed_by == "Robin Sylvester"


def test_pattern_service_get_pattern_with_evidence_resolves_links(
    tmp_path: Path,
) -> None:
    # Set up repositories
    pattern_repo = PatternRepository(tmp_path / "patterns.json")
    signal_repo = SignalRepository(tmp_path / "signals.json")
    action_repo = ActionRepository(tmp_path / "actions.json")
    reflection_repo = ReflectionRepository(tmp_path / "reflections.json")

    # Set up services
    signal_service = SignalService(signal_repo)
    action_service = ActionService(action_repo)
    reflection_service = ReflectionService(reflection_repo)
    pattern_service = PatternService(
        pattern_repo,
        signal_service=signal_service,
        action_service=action_service,
        reflection_service=reflection_service,
    )

    # Create signals
    signals = [
        Signal(
            id="SIG-001",
            title="Onboarding friction",
            type="Interview",
            area="Onboarding",
            impact="Medium",
            confidence="Medium",
            status="Open",
            owner="CS",
            destination="Product",
            evidence="Multiple new teams report early friction.",
            context="Q3 customer interviews",
        ),
        Signal(
            id="SIG-004",
            title="Setup confusion",
            type="Support ticket",
            area="Onboarding",
            impact="Medium",
            confidence="Medium",
            status="Open",
            owner="CS",
            destination="Product",
            evidence="Tickets about initial setup steps.",
            context="Support logs",
        ),
    ]
    signal_service.save_signals(signals)

    # Create action
    actions = [
        Action(
            id="ACT-001",
            signal_id="SIG-001",
            title="Improve onboarding checklist",
            description="Clarify first-week steps for new teams.",
            owner="Product",
            destination="Onboarding flow",
            status="In progress",
            due_date="2026-10-15",
            created_at="2026-09-01",
        ),
    ]
    action_service.save_actions(actions)

    # Create reflection
    reflections = [
        Reflection(
            id="LRN-001",
            action_id="ACT-001",
            outcome="Checklist updated and deployed.",
            learning="Early clarity reduces support load.",
            next_step="Monitor onboarding tickets for change.",
            recorded_at="2026-09-10",
        ),
    ]
    reflection_service.save_reflections(reflections)

    # Create pattern linking all of the above
    pattern = Pattern(
        id="PAT-004",
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
    pattern_service.save_patterns([pattern])

    # Resolve evidence
    evidence = pattern_service.get_pattern_with_evidence("PAT-004")

    assert isinstance(evidence, PatternWithEvidence)
    assert evidence.pattern.id == "PAT-004"
    assert {s.id for s in evidence.signals} == {"SIG-001", "SIG-004"}
    assert {a.id for a in evidence.actions} == {"ACT-001"}
    assert {r.id for r in evidence.reflections} == {"LRN-001"}

    assert evidence.missing_signal_ids == []
    assert evidence.missing_action_ids == []
    assert evidence.missing_reflection_ids == []


def test_pattern_service_get_pattern_with_evidence_reports_missing_links(
    tmp_path: Path,
) -> None:
    pattern_repo = PatternRepository(tmp_path / "patterns.json")
    signal_repo = SignalRepository(tmp_path / "signals.json")
    action_repo = ActionRepository(tmp_path / "actions.json")
    reflection_repo = ReflectionRepository(tmp_path / "reflections.json")

    signal_service = SignalService(signal_repo)
    action_service = ActionService(action_repo)
    reflection_service = ReflectionService(reflection_repo)
    pattern_service = PatternService(
        pattern_repo,
        signal_service=signal_service,
        action_service=action_service,
        reflection_service=reflection_service,
    )

    # Only save one of the two signals; leave action and reflection missing
    signals = [
        Signal(
            id="SIG-002",
            title="Reporting requests",
            type="Interview",
            area="Analytics",
            impact="Medium",
            confidence="Medium",
            status="Open",
            owner="Product",
            destination="Roadmap",
            evidence="Customers repeatedly ask for reports.",
            context="Q3 interviews",
        ),
    ]
    signal_service.save_signals(signals)

    pattern = Pattern(
        id="PAT-005",
        title="Reporting requests are recurring",
        category="Product insight",
        trend="Stable",
        status="Emerging",
        confidence="Medium",
        source_signal_ids=["SIG-002", "SIG-005"],  # SIG-005 does not exist
        source_action_ids=["ACT-002"],  # does not exist
        source_reflection_ids=["LRN-002"],  # does not exist
        affected_accounts=3,
        proposed_owner="Product Operations",
        proposed_destination="Roadmap review",
        description="Reporting needs are recurring across conversations.",
    )
    pattern_service.save_patterns([pattern])

    evidence = pattern_service.get_pattern_with_evidence("PAT-005")

    assert evidence.pattern.id == "PAT-005"
    assert {s.id for s in evidence.signals} == {"SIG-002"}
    assert evidence.actions == []
    assert evidence.reflections == []

    assert set(evidence.missing_signal_ids) == {"SIG-005"}
    assert set(evidence.missing_action_ids) == {"ACT-002"}
    assert set(evidence.missing_reflection_ids) == {"LRN-002"}
