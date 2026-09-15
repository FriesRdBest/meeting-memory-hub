from __future__ import annotations

from datetime import datetime
from pathlib import Path
from time import sleep
from uuid import uuid4

import streamlit as st

from models.reflection import Reflection
from repositories.reflection_repository import ReflectionRepository
from services.reflection_service import ReflectionService
from utils.ui import (
    configure_page,
    render_badges,
    render_card,
    render_divider,
    render_empty_state,
    render_metric,
    render_notice,
    render_page_header,
    render_sidebar_identity,
)

REFLECTION_FILE_PATH = Path("data/reflections.json")


def get_reflection_service() -> ReflectionService:
    return ReflectionService(ReflectionRepository(REFLECTION_FILE_PATH))


def initialise_state() -> None:
    if "reflections" not in st.session_state:
        try:
            st.session_state.reflections = (
                get_reflection_service().list_reflections()
            )
        except (OSError, ValueError):
            st.session_state.reflections = []

    if "learning_feedback" not in st.session_state:
        st.session_state.learning_feedback = None


def get_action_for_signal(signal_id: str) -> object | None:
    return next(
        (
            action
            for action in st.session_state.get("actions", [])
            if action.signal_id == signal_id
        ),
        None,
    )


def get_signal_for_id(signal_id: str) -> dict[str, str] | None:
    return next(
        (
            signal
            for signal in st.session_state.get("signals", [])
            if signal["id"] == signal_id
        ),
        None,
    )


def get_completed_actions() -> list[object]:
    return [
        action
        for action in st.session_state.get("actions", [])
        if action.status == "Completed"
    ]


def get_reflection_for_action(action_id: str) -> Reflection | None:
    return next(
        (
            reflection
            for reflection in st.session_state.reflections
            if reflection.action_id == action_id
        ),
        None,
    )


def save_reflections() -> bool:
    try:
        get_reflection_service().save_reflections(st.session_state.reflections)
        return True
    except OSError:
        return False


def format_relative_time(timestamp: str) -> str:
    try:
        recorded_at = datetime.strptime(
            timestamp,
            "%b %d, %Y at %I:%M %p",
        )
    except (TypeError, ValueError):
        return "Recorded recently"

    now = datetime.now()
    elapsed_seconds = max(0, int((now - recorded_at).total_seconds()))

    if elapsed_seconds < 60:
        return "Recorded just now"

    elapsed_minutes = elapsed_seconds // 60

    if elapsed_minutes < 60:
        unit = "minute" if elapsed_minutes == 1 else "minutes"
        return f"Recorded {elapsed_minutes} {unit} ago"

    elapsed_hours = elapsed_minutes // 60

    if elapsed_hours < 24:
        unit = "hour" if elapsed_hours == 1 else "hours"
        return f"Recorded {elapsed_hours} {unit} ago"

    elapsed_days = elapsed_hours // 24

    if elapsed_days == 1:
        return "Recorded yesterday"

    if elapsed_days < 7:
        return f"Recorded {elapsed_days} days ago"

    return f"Recorded {recorded_at.strftime('%b %d, %Y')}"


def add_reflection(
    action: object,
    outcome: str,
    learning: str,
    next_step: str,
) -> Reflection:
    reflection = Reflection(
        id=f"LRN-{uuid4().hex[:8].upper()}",
        action_id=action.id,
        outcome=outcome.strip(),
        learning=learning.strip(),
        next_step=next_step.strip() or "No further step recorded",
        recorded_at=datetime.now().strftime("%b %d, %Y at %I:%M %p"),
    )

    st.session_state.reflections.insert(0, reflection)

    return reflection


def render_learning_feedback() -> None:
    feedback = st.session_state.get("learning_feedback")

    if not feedback:
        return

    if feedback["saved"]:
        st.success(
            f"Learning recorded for {feedback['signal_id']}. It is now "
            "available as evidence for future pattern review."
        )
        return

    st.warning(
        f"Learning for {feedback['signal_id']} was recorded for this session, "
        "but could not be saved permanently."
    )


def render_completed_action_card(action: object) -> None:
    signal = get_signal_for_id(action.signal_id)
    existing_reflection = get_reflection_for_action(action.id)

    signal_title = signal["title"] if signal else action.title

    st.markdown(f"### {action.signal_id} · {signal_title}")

    render_badges(
        [
            "Completed",
            action.destination,
        ]
    )

    st.caption(
        f"Last activity: {format_relative_time(action.created_at)} · "
        f"Owner: {action.owner}"
    )

    if signal:
        st.caption(f"Original signal: {signal['id']} · {signal['title']}")

    if existing_reflection:
        st.success(
            "Learning has been retained for this completed action and can "
            "strengthen related emerging patterns."
        )

        st.caption(format_relative_time(existing_reflection.recorded_at))

        st.markdown("**Observed outcome**")
        st.write(existing_reflection.outcome)

        st.markdown("**Learning retained**")
        st.write(existing_reflection.learning)

        st.markdown("**Next step**")
        st.write(existing_reflection.next_step)

        return

    st.markdown("#### Record what the organization learned")

    st.caption(
        "A retained learning can later support an emerging pattern, but it "
        "does not automatically create or confirm one."
    )

    with st.form(f"reflection_form_{action.id}"):
        outcome = st.text_area(
            "Observed outcome",
            placeholder=(
                "Describe the observable result after this work was completed."
            ),
        )

        learning = st.text_area(
            "Learning retained",
            placeholder=(
                "Capture the reusable lesson that should inform a similar "
                "situation in the future."
            ),
        )

        next_step = st.text_input(
            "Remaining next step",
            placeholder=(
                "Optional. Record work that still needs to happen."
            ),
        )

        submitted = st.form_submit_button("Save Learning")

    if submitted:
        if not outcome.strip() or not learning.strip():
            st.warning(
                "Observed outcome and learning retained are both required."
            )
            return

        reflection = add_reflection(
            action=action,
            outcome=outcome,
            learning=learning,
            next_step=next_step,
        )

        saved = save_reflections()

        st.session_state.learning_feedback = {
            "signal_id": action.signal_id,
            "reflection_id": reflection.id,
            "saved": saved,
        }

        st.rerun()


def render_learning_history() -> None:
    st.markdown("## Learning retained")

    if not st.session_state.reflections:
        render_empty_state(
            title="No learning retained yet",
            description=(
                "Complete an action in Action Queue, then record the observed "
                "outcome and reusable lesson here. Retained learning will "
                "become visible evidence for future pattern review."
            ),
            symbol="·",
        )
        return

    for reflection in st.session_state.reflections:
        action = next(
            (
                item
                for item in st.session_state.get("actions", [])
                if item.id == reflection.action_id
            ),
            None,
        )

        signal = (
            get_signal_for_id(action.signal_id)
            if action
            else None
        )

        title = signal["title"] if signal else "Linked completed action"
        signal_id = signal["id"] if signal else "Signal unavailable"

        st.markdown(f"**{signal_id} · {title}**")

        render_badges(
            [
                "Learning retained",
                "Pattern evidence",
            ]
        )

        st.caption(format_relative_time(reflection.recorded_at))

        st.markdown("**Observed outcome**")
        st.write(reflection.outcome)

        st.markdown("**Learning retained**")
        st.write(reflection.learning)

        if reflection.next_step:
            st.caption(f"Next step: {reflection.next_step}")

        render_divider()


configure_page("Learning Loop | Meeting Memory Console")
render_sidebar_identity()
initialise_state()

completed_actions = get_completed_actions()
retained_learning = st.session_state.reflections

render_page_header(
    eyebrow="Learning Loop",
    title="What should the organization remember",
    description=(
        "Capture the observed outcome after work is completed and retain the "
        "reusable lesson. Learning strengthens future review without allowing "
        "the system to draw conclusions on its own."
    ),
)

render_notice(
    "Learning is human authored and evidence aware. Retained records can "
    "support emerging patterns, but a person must still review and confirm "
    "whether a pattern should become organizational memory."
)

metric_columns = st.columns(3)

with metric_columns[0]:
    render_metric("Completed actions", len(completed_actions))

with metric_columns[1]:
    render_metric("Learning retained", len(retained_learning))

with metric_columns[2]:
    render_metric(
        "Awaiting learning",
        sum(
            get_reflection_for_action(action.id) is None
            for action in completed_actions
        ),
    )

render_divider()

render_learning_feedback()

st.markdown("## Complete the loop")

if not completed_actions:
    render_empty_state(
        title="No completed actions yet",
        description=(
            "When work is marked completed in Action Queue, it will appear "
            "here for outcome and learning capture."
        ),
        symbol="✓",
    )
else:
    for action in completed_actions:
        render_completed_action_card(action)
        render_divider()

render_learning_history()

render_divider()

st.markdown("## Why this matters")

render_card(
    "Learning makes pattern review stronger",
    "A completed task becomes organizational memory when a person records "
    "what happened and what should be reused. Pattern Library can then show "
    "that retained learning as traceable evidence when a similar issue begins "
    "to emerge.",
)

feedback = st.session_state.get("learning_feedback")

if feedback:
    sleep(0.8)
    st.session_state.learning_feedback = None
    st.rerun()
