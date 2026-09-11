from __future__ import annotations

from datetime import datetime

import streamlit as st

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


ACTIONS = [
    {
        "id": "SIG-001",
        "title": "Repeated onboarding friction is slowing adoption",
        "type": "Customer friction",
        "impact": "High",
        "confidence": "High",
        "status": "Needs review",
        "owner": "Customer Success",
        "destination": "Product discovery",
        "next_step": "Review recurring onboarding evidence with Product.",
        "evidence": (
            "We keep hearing that the first workflow feels harder than it "
            "should, especially for new teams."
        ),
    },
    {
        "id": "SIG-002",
        "title": "Reporting requests are becoming a recurring product theme",
        "type": "Product insight",
        "impact": "Medium",
        "confidence": "High",
        "status": "Ready",
        "owner": "Product Operations",
        "destination": "Roadmap review",
        "next_step": "Bring the repeated reporting request to roadmap review.",
        "evidence": (
            "The reporting question came up again this week, and it sounds "
            "like more than a one-off request."
        ),
    },
    {
        "id": "SIG-003",
        "title": "A strategic commitment has no clear operational owner",
        "type": "Commitment",
        "impact": "High",
        "confidence": "Medium",
        "status": "Needs review",
        "owner": "Unassigned",
        "destination": "Leadership follow-up",
        "next_step": "Assign a named owner and confirm the next checkpoint.",
        "evidence": (
            "Everyone agreed that this matters, but I am not sure who is "
            "actually accountable for moving it forward."
        ),
    },
]


def initialise_state() -> None:
    if "action_records" not in st.session_state:
        st.session_state.action_records = {
            action["id"]: {
                "status": action["status"],
                "owner": action["owner"],
                "destination": action["destination"],
                "decision": None,
                "note": None,
                "updated_at": None,
            }
            for action in ACTIONS
        }

    if "action_history" not in st.session_state:
        st.session_state.action_history = []


def get_action(action_id: str) -> dict[str, str]:
    return next(action for action in ACTIONS if action["id"] == action_id)


def apply_decision(
    action_id: str,
    decision: str,
    owner: str,
    destination: str,
    note: str,
) -> None:
    record = st.session_state.action_records[action_id]

    status_by_decision = {
        "Accept route": "Ready",
        "Start work": "In progress",
        "Mark completed": "Completed",
        "Return for review": "Needs review",
    }

    new_status = status_by_decision[decision]

    record.update(
        {
            "status": new_status,
            "owner": owner.strip() or "Unassigned",
            "destination": destination.strip() or "Unassigned",
            "decision": decision,
            "note": note.strip() or None,
            "updated_at": datetime.now().strftime("%b %d, %Y at %I:%M %p"),
        }
    )

    st.session_state.action_history.insert(
        0,
        {
            "signal_id": action_id,
            "decision": decision,
            "owner": record["owner"],
            "destination": record["destination"],
            "note": record["note"],
            "updated_at": record["updated_at"],
        },
    )


def render_action_detail(action: dict[str, str]) -> None:
    record = st.session_state.action_records[action["id"]]

    st.markdown(f"## {action['id']} · {action['title']}")

    render_badges(
        [
            action["type"],
            f"{action['impact']} impact",
            f"{action['confidence']} confidence",
            record["status"],
        ]
    )

    st.markdown("### Evidence")
    st.markdown(f"> {action['evidence']}")

    st.markdown("### Proposed route")

    route_columns = st.columns(3)

    with route_columns[0]:
        st.caption("Destination")
        st.write(record["destination"])

    with route_columns[1]:
        st.caption("Owner")
        st.write(record["owner"])

    with route_columns[2]:
        st.caption("Next step")
        st.write(action["next_step"])

    if record["decision"]:
        st.markdown("### Latest decision")
        st.write(
            f"**{record['decision']}** — {record['updated_at']}"
        )

        if record["note"]:
            st.caption(record["note"])


def render_action_form(action: dict[str, str]) -> None:
    record = st.session_state.action_records[action["id"]]

    st.markdown("### Review and decide")

    with st.form(f"action_form_{action['id']}"):
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
            value=record["owner"],
            placeholder="Assign a person or team",
        )

        destination = st.text_input(
            "Destination",
            value=record["destination"],
            placeholder="Choose the destination for this signal",
        )

        note = st.text_area(
            "Decision note",
            placeholder=(
                "Record why this route was chosen, changed, or returned "
                "for review."
            ),
        )

        submitted = st.form_submit_button("Record decision")

    if submitted:
        apply_decision(
            action_id=action["id"],
            decision=decision,
            owner=owner,
            destination=destination,
            note=note,
        )
        st.success(
            f"{action['id']} was updated to “{decision}”. "
            "The decision is now visible in the session history."
        )
        st.rerun()


def render_history() -> None:
    st.markdown("## Decision history")

    if not st.session_state.action_history:
        st.caption(
            "No decisions have been recorded in this browser session yet."
        )
        return

    for event in st.session_state.action_history:
        st.markdown(
            f"**{event['signal_id']} · {event['decision']}**"
        )
        st.caption(
            f"{event['updated_at']} · {event['owner']} → "
            f"{event['destination']}"
        )

        if event["note"]:
            st.write(event["note"])

        render_divider()


configure_page("Action Queue | Meeting Memory Console")
render_sidebar_identity()
initialise_state()

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

records = st.session_state.action_records

metric_columns = st.columns(4)

with metric_columns[0]:
    render_metric("Open signals", len(ACTIONS))

with metric_columns[1]:
    render_metric(
        "Needs review",
        sum(record["status"] == "Needs review" for record in records.values()),
    )

with metric_columns[2]:
    render_metric(
        "In progress",
        sum(record["status"] == "In progress" for record in records.values()),
    )

with metric_columns[3]:
    render_metric(
        "Completed",
        sum(record["status"] == "Completed" for record in records.values()),
    )

render_divider()

st.markdown("## Signals awaiting a decision")

for action in ACTIONS:
    record = records[action["id"]]

    with st.expander(
        f"{action['id']} · {action['title']} · {record['status']}",
        expanded=False,
    ):
        render_badges(
            [
                action["type"],
                f"{action['impact']} impact",
                f"{action['confidence']} confidence",
                record["status"],
            ]
        )
        st.write(action["next_step"])
        st.caption(
            f"Owner: {record['owner']} · Destination: "
            f"{record['destination']}"
        )

render_divider()

st.markdown("## Inspect and decide")

selected_action_id = st.selectbox(
    "Choose a signal to review",
    options=[action["id"] for action in ACTIONS],
    format_func=lambda action_id: (
        f"{action_id} · {get_action(action_id)['title']}"
    ),
)

selected_action = get_action(selected_action_id)

render_action_detail(selected_action)
render_divider()
render_action_form(selected_action)
render_divider()
render_history()

st.markdown("## Next layer")

render_card(
    "From action to learning",
    "The next workspace will show completed work, observed outcomes, and the "
    "learning the organization has chosen to carry forward.",
)
