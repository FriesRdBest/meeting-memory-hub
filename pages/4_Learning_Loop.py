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
            st.session_state.reflections = get_reflection_service().list_reflections()
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
    signal = get_signal_for_id(action.signal_id)

    reflection = Reflection(
        id=f"LRN-{uuid4().hex[:8].upper()}",
        action_id=action.id,
        signal_id=action.signal_id,
        title=signal["title"] if signal else action.title,
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
        st.markdown(
            f"""
            <div class="mmc-action-feedback">
                <span class="mmc-action-feedback-check">✓</span>
                <span>
                    Learning recorded for {feedback["signal_id"]}.
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    st.markdown(
        f"""
        <div class="mmc-action-feedback mmc-action-feedback--warning">
            <span class="mmc-action-feedback-check">!</span>
            <span>
                Learning for {feedback["signal_id"]} was recorded for this
                session, but could not be saved permanently.
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_completed_action_card(action: object) -> None:
    signal = get_signal_for_id(action.signal_id)
    reflection = get_reflection_for_action(action.id)

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

    if reflection:
        st.success("Learning has been recorded for this completed action.")
        st.caption(format_relative_time(reflection.recorded_at))

        st.markdown("**Observed outcome**")
        st.write(reflection.outcome)

        st.markdown("**What the organization should remember**")
        st.write(reflection.learning)

        st.markdown("**Next step**")
        st.write(reflection.next_step)

        return

    st.markdown("### Record what the organization learned")

    with st.form(f"reflection_form_{action.id}"):
        outcome = st.text_area(
            "Observed outcome",
            placeholder=(
                "What happened after the work was completed? Keep this "
                "specific and observable."
            ),
        )

        learning = st.text_area(
            "What should the organization remember?",
            placeholder=(
                "Capture the reusable lesson that should inform similar "
                "situations in the future."
            ),
        )

        next_step = st.text_input(
            "Remaining next step",
            placeholder=("Optional. Record anything that still needs to happen."),
        )

        submitted = st.form_submit_button("Save Learning")

    if submitted:
        if not outcome.strip() or not learning.strip():
            st.warning("Observed outcome and organizational learning are required.")
            return

        reflection = add_reflection(
            action=action,
            outcome=outcome,
            learning=learning,
            next_step=next_step,
        )

        saved = save_reflections()

        st.session_state.learning_feedback = {
            "signal_id": reflection.signal_id,
            "saved": saved,
        }

        st.rerun()


def render_learning_history() -> None:
    st.markdown("## Learning retained")

    if not st.session_state.reflections:
        st.caption(
            "No learnings have been retained yet. Complete an action in "
            "Action Queue, then use this page to record what happened."
        )
        return

    for reflection in st.session_state.reflections:
        st.markdown(f"**{reflection.signal_id} · {reflection.title}**")
        render_badges(["Learning retained"])
        st.caption(format_relative_time(reflection.recorded_at))

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
        "Learning Loop makes completed work useful beyond one task. Record "
        "what happened, what the organization learned, and what should inform "
        "future decisions."
    ),
)

render_notice(
    "Learning is human-authored and evidence-aware. The system preserves what "
    "you record; it does not infer organizational conclusions automatically."
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
            get_reflection_for_action(action.id) is None for action in completed_actions
        ),
    )

render_divider()

render_learning_feedback()

st.markdown("## Complete the loop")

if not completed_actions:
    st.info(
        "No completed actions are available yet. Go to Action Queue, choose "
        "SIG-001, and use **Start work** followed by **Mark completed**."
    )
else:
    for action in completed_actions:
        render_completed_action_card(action)
        render_divider()

render_learning_history()

render_divider()

st.markdown("## Why this matters")

render_card(
    "Learning makes the next decision stronger",
    "A completed task only becomes organizational memory when someone records "
    "the observed result and the reusable lesson. The next person reviewing a "
    "similar signal can then start with context rather than rebuilding it "
    "from individual meetings.",
)

feedback = st.session_state.get("learning_feedback")

if feedback:
    sleep(0.8)
    st.session_state.learning_feedback = None
    st.rerun()
