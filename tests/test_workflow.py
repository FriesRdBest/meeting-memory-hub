from pathlib import Path

from services.signal_service import SignalService
from services.action_service import ActionService
from services.reflection_service import ReflectionService


def test_signal_to_action_to_reflection_workflow(tmp_path: Path) -> None:
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

    assert len(signals) == 1
    assert len(actions) == 1
    assert len(reflections) == 1

    assert signals[0]["id"] == "SIG-001"
    assert actions[0]["signal_id"] == "SIG-001"
    assert reflections[0]["action_id"] == "ACT-001"
