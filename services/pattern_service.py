from __future__ import annotations

from dataclasses import dataclass

from models.action import Action
from models.pattern import Pattern
from models.reflection import Reflection
from models.signal import Signal
from repositories.pattern_repository import PatternRepository
from services.action_service import ActionService
from services.reflection_service import ReflectionService
from services.signal_service import SignalService


@dataclass
class PatternWithEvidence:
    """A pattern together with its linked signals, actions, and reflections."""

    pattern: Pattern
    signals: list[Signal]
    actions: list[Action]
    reflections: list[Reflection]

    @property
    def missing_signal_ids(self) -> list[str]:
        return [
            sid
            for sid in self.pattern.source_signal_ids
            if sid not in {s.id for s in self.signals}
        ]

    @property
    def missing_action_ids(self) -> list[str]:
        return [
            aid
            for aid in self.pattern.source_action_ids
            if aid not in {a.id for a in self.actions}
        ]

    @property
    def missing_reflection_ids(self) -> list[str]:
        return [
            rid
            for rid in self.pattern.source_reflection_ids
            if rid not in {r.id for r in self.reflections}
        ]


class PatternService:
    def __init__(
        self,
        repository: PatternRepository,
        signal_service: SignalService | None = None,
        action_service: ActionService | None = None,
        reflection_service: ReflectionService | None = None,
    ) -> None:
        self.repository = repository
        self._signal_service = signal_service
        self._action_service = action_service
        self._reflection_service = reflection_service

    def list_patterns(self) -> list[Pattern]:
        return self.repository.list_all()

    def save_patterns(self, patterns: list[Pattern]) -> None:
        self.repository.save_all(patterns)

    def confirm_pattern(
        self,
        pattern_id: str,
        review_note: str,
        reviewed_by: str,
        reviewed_at: str,
        proposed_owner: str | None = None,
        proposed_destination: str | None = None,
    ) -> Pattern:
        """
        Mark a pattern as Confirmed with review metadata.

        - Updates status to 'Confirmed'.
        - Sets review_note, reviewed_by, reviewed_at.
        - Optionally updates proposed_owner / proposed_destination.
        - Saves all patterns back to the repository.
        """
        patterns = self.list_patterns()

        target = None
        for p in patterns:
            if p.id == pattern_id:
                target = p
                break

        if target is None:
            raise ValueError(f"Pattern {pattern_id} not found.")

        # Update review fields
        target.status = "Confirmed"
        target.review_note = review_note
        target.reviewed_by = reviewed_by
        target.reviewed_at = reviewed_at

        if proposed_owner is not None:
            target.proposed_owner = proposed_owner
        if proposed_destination is not None:
            target.proposed_destination = proposed_destination

        self.save_patterns(patterns)
        return target

    def get_pattern_with_evidence(self, pattern_id: str) -> PatternWithEvidence:
        """
        Resolve a pattern's linked signals, actions, and reflections.

        Returns a PatternWithEvidence object containing:
        - The pattern
        - All linked Signal records that exist
        - All linked Action records that exist
        - All linked Reflection records that exist
        - Helpers to see which IDs are missing
        """
        patterns = self.list_patterns()

        pattern = None
        for p in patterns:
            if p.id == pattern_id:
                pattern = p
                break

        if pattern is None:
            raise ValueError(f"Pattern {pattern_id} not found.")

        signals: list[Signal] = []
        actions: list[Action] = []
        reflections: list[Reflection] = []

        if self._signal_service is not None:
            all_signals = self._signal_service.list_signals()
            signals = [s for s in all_signals if s.id in pattern.source_signal_ids]

        if self._action_service is not None:
            all_actions = self._action_service.list_actions()
            actions = [a for a in all_actions if a.id in pattern.source_action_ids]

        if self._reflection_service is not None:
            all_reflections = self._reflection_service.list_reflections()
            reflections = [
                r for r in all_reflections if r.id in pattern.source_reflection_ids
            ]

        return PatternWithEvidence(
            pattern=pattern,
            signals=signals,
            actions=actions,
            reflections=reflections,
        )
