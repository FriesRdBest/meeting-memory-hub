from pathlib import Path

from models.action import Action
from models.reflection import Reflection
from models.signal import Signal
from repositories.action_repository import ActionRepository
from repositories.reflection_repository import ReflectionRepository
from repositories.signal_repository import SignalRepository
from services.action_service import ActionService
from services.reflection_service import ReflectionService
from services.signal_service import SignalService


def test_workflow_records_include_required_fields(tmp_path: Path) -> None:
    signal_service = SignalService(SignalRepository(tmp_path / "signals.json"))
    action_service = ActionService(ActionRepository(tmp_path / "actions.json"))
    reflection_service = ReflectionService(
        ReflectionRepository(tmp_path / "reflections.json")
    )

    signal = Signal(
        id="SIG-001",
        title="Repeated onboarding friction is slowing adoption",
        type="Customer friction",
        area="Customer",
        impact="High",
        confidence="High",
        status="Needs review",
        owner="Customer Success",
        destination="Product discovery",
        evidence="New teams report that the first workflow feels hard.",
        context="Customer onboarding review",
    )

    action = Action(
        id="ACT-001",
        signal_id=signal.id,
        title="Review onboarding evidence",
        description="Review recurring onboarding evidence with Product.",
        owner="Customer Success",
        destination="Product discovery",
        status="In progress",
        due_date="Oct 15, 2026",
        created_at="Sep 12, 2026 at 07:52 AM",
    )

    reflection = Reflection(
        id="LRN-001",
        action_id=action.id,
        outcome="A clearer first workflow guide was tested.",
        learning="New teams need guidance toward first success.",
        next_step="Review after the next onboarding cycle.",
        recorded_at="Sep 12, 2026 at 08:15 AM",
    )

    signal_service.save_signals([signal])
    action_service.save_actions([action])
    reflection_service.save_reflections([reflection])

    stored_signal = signal_service.list_signals()[0]
    stored_action = action_service.list_actions()[0]
    stored_reflection = reflection_service.list_reflections()[0]

    assert stored_signal.id
    assert stored_signal.title
    assert stored_signal.status

    assert stored_action.id
    assert stored_action.signal_id == stored_signal.id
    assert stored_action.status

    assert stored_reflection.id
    assert stored_reflection.action_id == stored_action.id
    assert stored_reflection.learning
