from pathlib import Path

from services.signal_service import SignalService
from services.action_service import ActionService
from services.reflection_service import ReflectionService


def test_signal_service_round_trip(tmp_path: Path) -> None:
    file_path = tmp_path / "signals.json"
    service = SignalService(file_path)

    source = {
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

    service.save(source)
    records = service.list_all()

    assert len(records) == 1
    assert records[0] == source


def test_action_service_round_trip(tmp_path: Path) -> None:
    file_path = tmp_path / "actions.json"
    service = ActionService(file_path)

    source = {
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

    service.save(source)
    records = service.list_all()

    assert len(records) == 1
    assert records[0] == source


def test_reflection_service_round_trip(tmp_path: Path) -> None:
    file_path = tmp_path / "reflections.json"
    service = ReflectionService(file_path)

    source = {
        "id": "LRN-001",
        "action_id": "ACT-001",
        "outcome": "A clearer first workflow guide was tested.",
        "learning": "New teams need guidance toward first success.",
        "next_step": "Review after the next onboarding cycle.",
        "recorded_at": "Sep 12, 2026 at 08:15 AM",
    }

    service.save(source)
    records = service.list_all()

    assert len(records) == 1
    assert records[0] == source
