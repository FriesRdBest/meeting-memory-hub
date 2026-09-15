from __future__ import annotations

from datetime import date, datetime
from pathlib import Path
from time import sleep
from uuid import uuid4

import streamlit as st

from models.action import Action
from models.pattern import Pattern
from repositories.action_repository import ActionRepository
from repositories.pattern_repository import PatternRepository
from services.action_service import ActionService
from services.pattern_service import PatternService
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

ACTION_FILE_PATH = Path("data/actions.json")
PATTERN_FILE_PATH = Path("data/patterns.json")
DATE_STORAGE_FORMAT = "%b %d, %Y"


def get_action_service() -> ActionService:
    return ActionService(ActionRepository(ACTION_FILE_PATH))


def get_pattern_service() -> PatternService:
    return PatternService(PatternRepository(PATTERN_FILE_PATH))


def initialise_state() -> None:
    if "actions" not in st.session_state:
        try:
            st.session_state.actions = get_action_service().list_actions()
        except (OSError, ValueError):
            st.session_state.actions = []

    if "patterns" not in st.session_state:
        try:
            st.session_state.patterns = get_pattern_service().list_patterns()
        except (OSError, ValueError, KeyError):
            st.session_state.patterns = []

    if "action_history" not in st.session_state:
        st.session_state.action_history = []

    if "action_feedback" not in st.session_state:
        st.session_state.action_feedback = None


def get_signal(signal_id: str) -> dict[str, str]:
    signals = st.session_state.get("signals", [])

    return next(
        signal
        for signal in signals
        if signal["id"] == signal_id
    )


def get_action_for_signal(signal_id: str) -> Action | None:
    return next(
        (
            action
            for action in st.session_state.actions
            if action.signal_id == signal_id
        ),
        None,
    )


def get_patterns_for_signal(signal_id: str) -> list[Pattern]:
    return [
        pattern
        for pattern in st.session_state.get("patterns", [])
        if signal_id in pattern.source_signal_ids
        and pattern.status != "Dismissed"
    ]


def get_or_create_action(signal: dict[str, str]) -> Action:
    existing_action = get_action_for_signal(signal["id"])

    if existing_action:
        return existing_action

    action = Action(
        id=f"ACT-{uuid4().hex[:8].upper()}",
        signal_id=signal["id"],
        title=signal["title"],
        description=(
            f"Review the evidence and agree the next move for "
            f"{signal['title'].lower()}."
        ),
        owner=signal["owner"],
        destination=signal["destination"],
        status=signal["status"],
        due_date="Not set",
        created_at=datetime.now().strftime("%b %d, %Y at %I:%M %p"),
    )

    st.session_state.actions.append(action)

    return action


def save_actions() -> bool:
    try:
        get_action_service().save_actions(st.session_state.actions)
        return True
    except OSError:
        return False


def parse_due_date(due_date: str) -> date | None:
    if not due_date or due_date == "Not set":
        return None

    try:
        return datetime.strptime(
            due_date,
            DATE_STORAGE_FORMAT,
        ).date()
    except ValueError:
        return None


def format_due_date(due_date: date | None) -> str:
    if due_date is None:
        return "Not set"

    return due_date.strftime(DATE_STORAGE_FORMAT)


def apply_decision(
    action: Action,
    decision: str,
    owner: str,
    destination: str,
    due_date: date | None,
    note: str,
) -> bool:
    status_by_decision = {
        "Accept route": "Ready",
        "Start work": "In progress",
        "Mark completed": "Completed",
        "Return for review": "Needs review",
    }

    action.status = status_by_decision[decision]
    action.owner = owner.strip() or "Unassigned"
    action.destination = destination.strip() or "Unassigned"
    action.due_date = format_due_date(due_date)

    updated_at = datetime.now().strftime("%b %d, %Y at %I:%M %p")

    st.session_state.action_history.insert(
        0,
        {
            "signal_id": action.signal_id,
            "action_id": action.id,
            "decision": decision,
            "owner": action.owner,
            "destination": action.destination,
            "due_date": action.due_date,
            "note": note.strip() or None,
            "updated_at": updated_at,
        },
    )

    return save_actions()


def render_pattern_context(signal_id: str) -> None:
    linked_patterns = get_patterns_for_signal(signal_id)

    st.markdown("### Pattern context")

    if not linked_patterns:
        st.caption(
            "No active emerging or confirmed patterns are linked to this "
            "signal yet. The decision can still proceed with the available "
            "signal evidence."
        )
        return

    for pattern in linked_patterns:
        st.markdown(f"**{pattern.id} · {pattern.title}**")

        render_badges(
            [
                pattern.status,
                f"{pattern.confidence} confidence",
                pattern.trend,
                f"{pattern.evidence_count} evidence sources",
            ]
        )

        st.write(pattern.description)

        if pattern.status == "Confirmed":
            st.success(
                "This is confirmed organizational memory. Consider it before "
                "recording the next action."
            )
        else:
            st.caption(
                "This is emerging evidence, not an automatic conclusion. "
                "Review Pattern Library if you need to inspect the sources."
            )


def render_action_detail(signal: dict[str, str], action: Action) -> None:
    st.markdown(f"## {signal['id']} · {signal['title']}")

    render_badges(
        [
            signal["type"],
            signal["area"],
            f"{signal['impact']} impact",
            f"{signal['confidence']} confidence",
            action.status,
        ]
    )

    st.markdown("### What the evidence says")
    st.markdown(f"> {signal['evidence']}")

    render_pattern_context(signal["id"])

    st.markdown("### Proposed route")

    route_columns = st.columns(3)

    with route_columns[0]:
        st.caption("Destination")
        st.write(action.destination)

    with route_columns[1]:
        st.caption("Accountable owner")
        st.write(action.owner)

    with route_columns[2]:
        st.caption("Due date")
        st.write(action.due_date)

    st.markdown("### What this action means")
    st.write(action.description)

    st.caption(
        "Pattern context informs human judgment. It does not automatically "
        "assign work, determine ownership, or make a decision."
    )


def render_action_feedback() -> None:
    feedback = st.session_state.get("action_feedback")

    if not feedback:
        return

    feedback_signal_id = feedback["signal_id"]
    feedback_decision = feedback["decision"]
    feedback_saved = feedback["saved"]

    if feedback_saved:
        st.success(
            f"{feedback_signal_id} decision recorded: {feedback_decision}."
        )
        return

    st.warning(
        f"{feedback_signal_id} was updated for this session, but it could not "
        "be saved permanently."
    )


def render_action_form(signal: dict[str, str], action: Action) -> None:
    st.markdown("### Confirm the next move")

    existing_due_date = parse_due_date(action.due_date)

    with st.form(f"action_form_{signal['id']}"):
        decision = st.selectbox(
            "Decision",
            [
                "Accept route",
                "Start work",
                "Mark completed",
                "Return for review",
            ],
            help=(
                "A decision records accountable human judgment. It does not "
                "automatically assign work or draw conclusions from evidence."
            ),
        )

        owner = st.text_input(
            "Accountable owner",
            value=action.owner,
            placeholder="Assign a person or team",
        )

        destination = st.text_input(
            "Destination",
            value=action.destination,
            placeholder="Choose where the work should be handled",
        )

        due_date = st.date_input(
            "Due date",
            value=existing_due_date,
            min_value=date.today(),
            format="MM/DD/YYYY",
            help=(
                "Select a due date from the calendar. Leave it blank when "
                "the action does not have a confirmed date yet."
            ),
        )

        note = st.text_area(
            "Decision note",
            placeholder=(
                "Capture why this route was chosen, changed, completed, or "
                "returned for review."
            ),
        )

        submitted = st.form_submit_button("Record Accountable Decision")

    if submitted:
        saved = apply_decision(
            action=action,
            decision=decision,
            owner=owner,
            destination=destination,
            due_date=due_date,
            note=note,
        )

        st.session_state.action_feedback = {
            "signal_id": signal["id"],
            "decision": decision,
            "saved": saved,
        }

        st.rerun()


def render_history() -> None:
    st.markdown("## Decision history")

    if not st.session_state.action_history:
        st.caption(
            "No decisions have been recorded in this browser session yet. "
            "The history will make the progression from signal to action visible."
        )
        return

    for event in st.session_state.action_history:
        st.markdown(f"**{event['signal_id']} · {event['decision']}**")

        st.caption(
            f"{event['updated_at']} · {event['owner']} → "
            f"{event['destination']} · Due: {event['due_date']}"
        )

        if event["note"]:
            st.write(event["note"])

        render_divider()


configure_page("Action Queue | Meeting Memory Console")
render_sidebar_identity()
initialise_state()

signals = st.session_state.get("signals", [])

render_page_header(
    eyebrow="Action Queue",
    title="Who owns the next move",
    description=(
        "Turn reviewed evidence into a clear human decision. Confirm who is "
        "responsible, where the work belongs, and what should happen next."
    ),
)

render_notice(
    "Action Queue is intentionally human controlled. Suggestions and pattern "
    "context may guide review, but a person must confirm ownership, "
    "destination, and the decision before work progresses."
)

st.info(
    "Demo journey: Choose **SIG-001**, review its pattern context, confirm "
    "the proposed route, then use **Start work** followed by **Mark "
    "completed**. Learning Loop will then let you record what the "
    "organization learned."
)

actions_by_signal = {
    action.signal_id: action
    for action in st.session_state.actions
}

metric_columns = st.columns(4)

with metric_columns[0]:
    render_metric("Signals in view", len(signals))

with metric_columns[1]:
    render_metric(
        "Need decision",
        sum(
            (
                actions_by_signal.get(signal["id"]).status
                if signal["id"] in actions_by_signal
                else signal["status"]
            )
            == "Needs review"
            for signal in signals
        ),
    )

with metric_columns[2]:
    render_metric(
        "Work in progress",
        sum(
            action.status == "In progress"
            for action in st.session_state.actions
        ),
    )

with metric_columns[3]:
    render_metric(
        "Completed",
        sum(
            action.status == "Completed"
            for action in st.session_state.actions
        ),
    )

render_divider()

render_action_feedback()

st.markdown("## What needs a decision")

for signal in signals:
    action = get_action_for_signal(signal["id"])
    status = action.status if action else signal["status"]
    linked_patterns = get_patterns_for_signal(signal["id"])

    with st.expander(
        f"{signal['id']} · {signal['title']} · {status}",
        expanded=False,
    ):
        render_badges(
            [
                signal["type"],
                signal["area"],
                f"{signal['impact']} impact",
                f"{signal['confidence']} confidence",
                status,
            ]
        )

        if linked_patterns:
            st.caption(
                f"Pattern context available: {len(linked_patterns)} linked "
                "emerging or confirmed pattern."
            )

        st.write(
            "Select this signal below to review the evidence, inspect its "
            "available pattern context, and record an accountable decision."
        )

        st.caption(
            f"Proposed owner: {action.owner if action else signal['owner']} · "
            f"Proposed destination: "
            f"{action.destination if action else signal['destination']}"
        )

render_divider()

st.markdown("## Inspect and decide")

if not signals:
    st.info("No signals are available in this session.")
else:
    selected_signal_id = st.selectbox(
        "Choose a signal to review",
        options=[signal["id"] for signal in signals],
        format_func=lambda signal_id: (
            f"{signal_id} · {get_signal(signal_id)['title']}"
        ),
    )

    selected_signal = get_signal(selected_signal_id)
    selected_action = get_or_create_action(selected_signal)

    render_action_detail(selected_signal, selected_action)

    render_divider()

    render_action_form(selected_signal, selected_action)

    render_divider()

    render_history()

st.markdown("## The learning layer")

render_card(
    "From action to organizational memory",
    "Completion is not the end of the workflow. Learning Loop captures what "
    "happened after the work, what the organization should remember, and any "
    "next step that remains. Retained learning can strengthen future pattern "
    "review without replacing human judgment.",
)

feedback = st.session_state.get("action_feedback")

if feedback:
    sleep(0.8)
    st.session_state.action_feedback = None
    st.rerun()
