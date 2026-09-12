from pathlib import Path

from services.signal_service import SignalService
from services.action_service import ActionService
from services.reflection_service import ReflectionService


def test_quality_checks_before_merge(tmp_path: Path) -> None:
    signals_file = tmp_path / "signals.json"
    actions_file = tmp_path / "actions.json"
    reflections_file = tmp_path / "reflections.json"

    signal_service = SignalService(signals_file)
    action_service = ActionService(actions_file)
    reflection_service = ReflectionService(reflections_file)

    signal = {
        "id": "SIG-001",
        "title": "Repeated onboarding friction is slowing adoption",
        "type": "Customer friction",
        "area": "Customer",
        "impact": "High",
        "confidence": "High",
        "status": "Needs review",
        "owner": "Customer Success",
        "destination": "Product discovery",
        "evidence": "New teams report that the first workflow feels hard.",
        "context": "Customer onboarding review",
    }

    action = {
        "id": "ACT-001",
        "signal_id": "SIG-001",
        "title": "Review onboarding evidence",
        "description": "Review recurring onboarding evidence with Product.",
        "owner": "Customer Success",
        "destination": "Product discovery",
        "status": "In progress",
        "due_date": "Oct 15, 2026",
        "created_at": "Sep 12, 2026 at 07:52 AM",
    }

    reflection = {
        "id": "LRN-001",
        "action_id": "ACT-001",
        "outcome": "A clearer first workflow guide was tested.",
        "learning": "New teams need guidance toward first success.",
        "next_step": "Review after the next onboarding cycle.",
        "recorded_at": "Sep 12, 2026 at 08:15 AM",
    }

    signal_service.save(signal)
    action_service.save(action)
    reflection_service.save(reflection)

    signals = signal_service.list_all()
    actions = action_service.list_all()
    reflections = reflection_service.list_all()

    assert len(signals) > 0, "At least one signal must exist"
    assert len(actions) > 0, "At least one action must exist"
    assert len(reflections) > 0, "At least one reflection must exist"

    for s in signals:
        assert "id" in s
        assert "title" in s
        assert "status" in s

    for a in actions:
        assert "id" in a
        assert "signal_id" in a
        assert "status" in a

    for r in reflections:
        assert "id" in r
        assert "action_id" in r
        assert "learning" in r
