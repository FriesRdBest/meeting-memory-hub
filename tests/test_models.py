from models.action import Action
from models.reflection import Reflection
from models.signal import Signal


def test_signal_round_trip() -> None:
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

    signal = Signal.from_dict(source)

    assert signal.id == "SIG-001"
    assert signal.title == source["title"]
    assert signal.to_dict() == source


def test_action_round_trip() -> None:
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

    action = Action.from_dict(source)

    assert action.signal_id == "SIG-001"
    assert action.status == "In progress"
    assert action.to_dict() == source


def test_reflection_round_trip() -> None:
    source = {
        "id": "LRN-001",
        "action_id": "ACT-001",
        "outcome": "A clearer first workflow guide was tested.",
        "learning": "New teams need guidance toward first success.",
        "next_step": "Review after the next onboarding cycle.",
        "recorded_at": "Sep 12, 2026 at 08:15 AM",
    }

    reflection = Reflection.from_dict(source)

    assert reflection.action_id == "ACT-001"
    assert reflection.learning == source["learning"]
    assert reflection.to_dict() == source
