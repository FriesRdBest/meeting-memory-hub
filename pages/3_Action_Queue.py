from __future__ import annotations

from datetime import datetime
from pathlib import Path
from uuid import uuid4

import streamlit as st

from models.action import Action
from repositories.action_repository import ActionRepository
from services.action_service import ActionService
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


def get_action_service() -> ActionService:
    return ActionService(ActionRepository(ACTION_FILE_PATH))


def initialise_state() -> None:
    if "actions" not in st.session_state:
        try:
            st.session_state.actions = get_action_service().list_actions()
        except (OSError, ValueError):
            st.session_state.actions = []

    if "action_history" not in st.session_state:
        st.session_state.action_history = []


def get_signal(signal_id: str) -> dict[str, str]:
    signals = st.session_state.get("signals", [])
    return next(signal for signal in signals if signal["id"] == signal_id)


def get_action_for_signal(signal_id: str) -> Action | None:
    return next(
        (
            action
            for action in st.session_state.actions
            if action.signal_id == signal_id
        ),
        None,
    )


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


def apply_decision(
    action: Action,
    decision: str,
    owner: str,
    destination: str,
    due_date: str,
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
    action.due_date = due_date.strip() or "Not set"

    updated_at = datetime.now().strftime("%b %d, %Y at %I:%M %p")

    st.session_state.action_history.insert(
        0,
        {
            "signal_id": action.signal_id,
            "action_id": action.id,
            "decision": decision,
            "owner": action.owner,
            "destination": action.destination,
            "note": note.strip() or None,
            "updated_at": updated_at,
        },
    )

    return save_actions()


def render_action_detail(signal: dict[str, str], action: Action) -> None:
    st.markdown(f"## {signal['id']} · {signal['title']}")

    render_badges(
        [
            signal["type"],
            f"{signal['impact']} impact",
            f"{signal['confidence']} confidence",
            action.status,
        ]
    )

    st.markdown("### Evidence")
    st.markdown(f"> {signal['evidence']}")

    st.markdown("### Proposed route")

    route_columns = st.columns(3)

    with route_columns[0]:
        st.caption("Destination")
        st.write(action.destination)

    with route_columns[1]:
        st.caption("Owner")
        st.write(action.owner)

    with route_columns[2]:
        st.caption("Due date")
        st.write(action.due_date)

    st.markdown("### Action")
    st.write(action.description)


def render_action_form(signal: dict[str, str], action: Action) -> None:
    st.markdown("### Review and decide")

    with st.form(f"action_form_{signal['id']}"):
        decision = st.selectbox(
            "Decision",
            [
                "Accept route",
                "Start work",
                "Mark completed",
                "Return for review",
            ],
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

        due_date = st.text_input(
            "Due date",
            value=action.due_date,
            placeholder="For example, Oct 15, 2026",
        )

        note = st.text_area(
            "Decision note",
            placeholder=(
                "Record why this route was chosen, changed, or returned for review."
            ),
        )

        submitted = st.form_submit_button("Record decision")

    if submitted:
        saved = apply_decision(
            action=action,
            decision=decision,
            owner=owner,
            destination=destination,
            due_date=due_date,
            note=note,
        )

        if saved:
            st.success(f"{signal['id']} was updated to '{decision}' and saved.")
        else:
            st.warning(
                f"{signal['id']} was updated for this session, but the "
                "host could not save it permanently."
            )

        st.rerun()


def render_history() -> None:
    st.markdown("## Decision history")

    if not st.session_state.action_history:
        st.caption("No decisions have been recorded in this browser session yet.")
        return

    for event in st.session_state.action_history:
        st.markdown(f"**{event['signal_id']} · {event['decision']}**")
        st.caption(f"{event['updated_at']} · {event['owner']} → {event['destination']}")

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
        "Review suggested routes, inspect the supporting evidence, and record "
        "a human decision before a signal progresses through the workflow."
    ),
)

render_notice(
    "Suggested routes are not automatic conclusions. A person reviews the "
    "evidence, confirms or changes the proposed route, and records why."
)

# Demo banner for medium-build walkthrough
st.info(
    "Demo mode: For the walkthrough, choose **SIG-001**. "
    "Use Start work → Mark completed, then record a "
    "reflection in Learning Loop."
)

actions_by_signal = {action.signal_id: action for action in st.session_state.actions}

metric_columns = st.columns(4)

with metric_columns[0]:
    render_metric("Signals in view", len(signals))

with metric_columns[1]:
    render_metric(
        "Needs review",
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
        "In progress",
        sum(action.status == "In progress" for action in st.session_state.actions),
    )

with metric_columns[3]:
    render_metric(
        "Completed",
        sum(action.status == "Completed" for action in st.session_state.actions),
    )

render_divider()

st.markdown("## Signals awaiting a decision")

for signal in signals:
    action = get_action_for_signal(signal["id"])
    status = action.status if action else signal["status"]

    with st.expander(
        f"{signal['id']} · {signal['title']} · {status}",
        expanded=False,
    ):
        render_badges(
            [
                signal["type"],
                f"{signal['impact']} impact",
                f"{signal['confidence']} confidence",
                status,
            ]
        )
        st.write(
            "Select this signal below to review the evidence and record "
            "an accountable action."
        )
        st.caption(
            f"Owner: {action.owner if action else signal['owner']} · "
            f"Destination: "
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
        format_func=lambda signal_id: f"{signal_id} · {get_signal(signal_id)['title']}",
    )

    selected_signal = get_signal(selected_signal_id)
    selected_action = get_or_create_action(selected_signal)

    render_action_detail(selected_signal, selected_action)
    render_divider()
    render_action_form(selected_signal, selected_action)
    render_divider()
    render_history()

st.markdown("## Next layer")

render_card(
    "From action to learning",
    "The next workspace will show completed work, observed outcomes, and the "
    "learning the organization has chosen to carry forward.",
)
