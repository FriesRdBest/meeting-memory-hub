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


def test_signal_service_round_trip(tmp_path: Path) -> None:
    repository = SignalRepository(tmp_path / "signals.json")
    service = SignalService(repository)

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

    service.save_signals([signal])

    assert service.list_signals() == [signal]


def test_action_service_round_trip(tmp_path: Path) -> None:
    repository = ActionRepository(tmp_path / "actions.json")
    service = ActionService(repository)

    action = Action(
        id="ACT-001",
        signal_id="SIG-001",
        title="Review onboarding evidence",
        description="Review recurring onboarding evidence with Product.",
        owner="Customer Success",
        destination="Product discovery",
        status="In progress",
        due_date="Oct 15, 2026",
        created_at="Sep 12, 2026 at 07:52 AM",
    )

    service.save_actions([action])

    assert service.list_actions() == [action]


def test_reflection_service_round_trip(tmp_path: Path) -> None:
    repository = ReflectionRepository(tmp_path / "reflections.json")
    service = ReflectionService(repository)

    reflection = Reflection(
        id="LRN-001",
        action_id="ACT-001",
        outcome="A clearer first workflow guide was tested.",
        learning="New teams need guidance toward first success.",
        next_step="Review after the next onboarding cycle.",
        recorded_at="Sep 12, 2026 at 08:15 AM",
    )

    service.save_reflections([reflection])

    assert service.list_reflections() == [reflection]
