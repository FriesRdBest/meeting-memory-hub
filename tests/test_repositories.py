from pathlib import Path

from models.action import Action
from models.reflection import Reflection
from models.signal import Signal
from repositories.action_repository import ActionRepository
from repositories.reflection_repository import ReflectionRepository
from repositories.signal_repository import SignalRepository


def test_signal_repository_round_trip(tmp_path: Path) -> None:
    file_path = tmp_path / "signals.json"
    repository = SignalRepository(file_path)

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

    repository.save_all([signal])

    assert repository.list_all() == [signal]


def test_action_repository_round_trip(tmp_path: Path) -> None:
    file_path = tmp_path / "actions.json"
    repository = ActionRepository(file_path)

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

    repository.save_all([action])

    assert repository.list_all() == [action]


def test_reflection_repository_round_trip(tmp_path: Path) -> None:
    file_path = tmp_path / "reflections.json"
    repository = ReflectionRepository(file_path)

    reflection = Reflection(
        id="LRN-001",
        action_id="ACT-001",
        outcome="A clearer first workflow guide was tested.",
        learning="New teams need guidance toward first success.",
        next_step="Review after the next onboarding cycle.",
        recorded_at="Sep 12, 2026 at 08:15 AM",
    )

    repository.save_all([reflection])

    assert repository.list_all() == [reflection]
