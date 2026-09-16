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
from services.pattern_service import PatternService
from services.reflection_service import ReflectionService
from services.signal_service import SignalService


def main() -> None:
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)

    # Repositories
    pattern_repo = PatternRepository(data_dir / "patterns.json")
    signal_repo = SignalRepository(data_dir / "signals.json")
    action_repo = ActionRepository(data_dir / "actions.json")
    reflection_repo = ReflectionRepository(data_dir / "reflections.json")

    # Services
    signal_service = SignalService(signal_repo)
    action_service = ActionService(action_repo)
    reflection_service = ReflectionService(reflection_repo)
    pattern_service = PatternService(
        pattern_repo,
        signal_service=signal_service,
        action_service=action_service,
        reflection_service=reflection_service,
    )

    # --- Create sample signals ---
    signals = [
        Signal(
            id="SIG-001",
            title="Onboarding friction in week 1",
            type="Interview",
            area="Onboarding",
            impact="Medium",
            confidence="Medium",
            status="Open",
            owner="Customer Success",
            destination="Product",
            evidence="3 new teams reported confusion in first week.",
            context="Q3 customer interviews",
        ),
        Signal(
            id="SIG-004",
            title="Setup steps unclear",
            type="Support ticket",
            area="Onboarding",
            impact="Medium",
            confidence="Medium",
            status="Open",
            owner="Customer Success",
            destination="Product",
            evidence="Multiple tickets about initial setup.",
            context="Support logs",
        ),
    ]
    signal_service.save_signals(signals)

    # --- Create sample action ---
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

    # --- Create sample reflection ---
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

    # --- Create pattern linking them ---
    pattern = Pattern(
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
    pattern_service.save_patterns([pattern])

    print("=== Pattern before confirmation ===")
    print(f"ID: {pattern.id}")
    print(f"Title: {pattern.title}")
    print(f"Status: {pattern.status}")
    print(f"Evidence count: {pattern.evidence_count}")
    print()

    # --- Confirm the pattern ---
    confirmed = pattern_service.confirm_pattern(
        pattern_id="PAT-001",
        review_note="Consistent evidence across interviews and support tickets.",
        reviewed_by="Robin Sylvester",
        reviewed_at="Sep 16, 2026 at 02:30 PM",
        proposed_owner="Product Operations",
        proposed_destination="Onboarding roadmap",
    )

    print("=== Pattern after confirmation ===")
    print(f"ID: {confirmed.id}")
    print(f"Title: {confirmed.title}")
    print(f"Status: {confirmed.status}")
    print(f"Proposed owner: {confirmed.proposed_owner}")
    print(f"Proposed destination: {confirmed.proposed_destination}")
    print(f"Review note: {confirmed.review_note}")
    print(f"Reviewed by: {confirmed.reviewed_by}")
    print(f"Reviewed at: {confirmed.reviewed_at}")
    print()

    # --- Resolve and print evidence ---
    evidence = pattern_service.get_pattern_with_evidence("PAT-001")

    print("=== Evidence summary ===")
    print(f"Signals linked: {len(evidence.signals)}")
    for s in evidence.signals:
        print(f"  - [{s.id}] {s.title} ({s.type})")

    print(f"Actions linked: {len(evidence.actions)}")
    for a in evidence.actions:
        print(f"  - [{a.id}] {a.title} (owner: {a.owner})")

    print(f"Reflections linked: {len(evidence.reflections)}")
    for r in evidence.reflections:
        print(f"  - [{r.id}] {r.outcome} (learning: {r.learning[:50]}...)")

    if evidence.missing_signal_ids:
        print("Missing signals:", evidence.missing_signal_ids)
    if evidence.missing_action_ids:
        print("Missing actions:", evidence.missing_action_ids)
    if evidence.missing_reflection_ids:
        print("Missing reflections:", evidence.missing_reflection_ids)

    print()
    print("Traceable workflow demo complete.")


if __name__ == "__main__":
    main()
