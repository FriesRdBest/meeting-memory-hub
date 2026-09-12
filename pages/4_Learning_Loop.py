from __future__ import annotations

from datetime import datetime
from pathlib import Path
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

LEARNING_RECORDS = [
    {
        "id": "SIG-014",
        "title": "Implementation guidance reduced early-stage hesitation",
        "type": "Customer friction",
        "area": "Customer",
        "impact": "High",
        "outcome": (
            "Customer Success introduced a structured first-workflow guide "
            "and added an implementation checkpoint during onboarding."
        ),
        "learning": (
            "Early product friction was not only a usability issue. Teams "
            "needed clearer guidance about the first successful outcome."
        ),
        "owner": "Customer Success",
        "completed": "May 14, 2026",
        "evidence": (
            "New teams were asking the same setup questions before they "
            "reached their first useful workflow."
        ),
    },
    {
        "id": "SIG-018",
        "title": "A recurring reporting need informed roadmap discovery",
        "type": "Product insight",
        "area": "Product",
        "impact": "Medium",
        "outcome": (
            "Product Operations created a discovery brief using repeated "
            "customer requests and reviewed it during roadmap planning."
        ),
        "learning": (
            "Repeated reporting questions carried more strategic value when "
            "they were grouped by use case rather than logged as isolated "
            "feature requests."
        ),
        "owner": "Product Operations",
        "completed": "May 21, 2026",
        "evidence": (
            "Several teams wanted the same progress view, but described it "
            "through different reporting requests."
        ),
    },
    {
        "id": "SIG-022",
        "title": "Named ownership made a cross-functional commitment visible",
        "type": "Commitment",
        "area": "Operations",
        "impact": "High",
        "outcome": (
            "Leadership Operations assigned a named owner, scheduled a "
            "checkpoint, and made progress visible in the operating review."
        ),
        "learning": (
            "A commitment becomes actionable only when ownership, destination, "
            "and the next review point are explicit."
        ),
        "owner": "Leadership Operations",
        "completed": "May 28, 2026",
        "evidence": (
            "The commitment had appeared in multiple meetings, but no "
            "accountable owner or checkpoint had been recorded."
        ),
    },
]


def get_reflection_service() -> ReflectionService:
    return ReflectionService(ReflectionRepository(REFLECTION_FILE_PATH))


def initialise_state() -> None:
    if "reflections" not in st.session_state:
        try:
            st.session_state.reflections = get_reflection_service().list_reflections()
        except (OSError, ValueError):
            st.session_state.reflections = []


def matches_search(record: dict[str, str], search_text: str) -> bool:
    if not search_text:
        return True

    searchable_text = " ".join(record.values()).lower()
    return search_text.lower() in searchable_text


def get_signal(signal_id: str) -> dict[str, str] | None:
    return next(
        (
            signal
            for signal in st.session_state.get("signals", [])
            if signal["id"] == signal_id
        ),
        None,
    )


def get_action(action_id: str):
    return next(
        (
            action
            for action in st.session_state.get("actions", [])
            if action.id == action_id
        ),
        None,
    )


def get_completed_actions():
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


def create_reflection(
    action_id: str,
    outcome: str,
    learning: str,
    next_step: str,
) -> bool:
    existing_reflection = get_reflection_for_action(action_id)

    if existing_reflection:
        existing_reflection.outcome = outcome.strip()
        existing_reflection.learning = learning.strip()
        existing_reflection.next_step = next_step.strip()
        existing_reflection.recorded_at = datetime.now().strftime(
            "%b %d, %Y at %I:%M %p"
        )
    else:
        reflection = Reflection(
            id=f"LRN-{uuid4().hex[:8].upper()}",
            action_id=action_id,
            outcome=outcome.strip(),
            learning=learning.strip(),
            next_step=next_step.strip(),
            recorded_at=datetime.now().strftime("%b %d, %Y at %I:%M %p"),
        )
        st.session_state.reflections.append(reflection)

    return save_reflections()


def build_reflection_record(reflection: Reflection) -> dict[str, str] | None:
    action = get_action(reflection.action_id)

    if action is None:
        return None

    signal = get_signal(action.signal_id)

    if signal is None:
        return None

    return {
        "id": signal["id"],
        "title": signal["title"],
        "type": signal["type"],
        "area": signal["area"],
        "impact": signal["impact"],
        "outcome": reflection.outcome,
        "learning": reflection.learning,
        "owner": action.owner,
        "completed": reflection.recorded_at,
        "evidence": signal["evidence"],
        "next_step": reflection.next_step,
    }


def render_learning_record(record: dict[str, str]) -> None:
    st.markdown(f"### {record['id']} · {record['title']}")

    render_badges(
        [
            record["type"],
            record["area"],
            f"{record['impact']} impact",
            "Completed",
        ]
    )

    columns = st.columns(2)

    with columns[0]:
        st.markdown("#### Observed outcome")
        st.write(record["outcome"])

    with columns[1]:
        st.markdown("#### Learning retained")
        st.write(record["learning"])

    detail_columns = st.columns(2)

    with detail_columns[0]:
        st.caption("Accountable owner")
        st.write(record["owner"])

    with detail_columns[1]:
        st.caption("Completed")
        st.write(record["completed"])

    if record.get("next_step"):
        st.caption(f"Next step: {record['next_step']}")

    with st.expander("View original evidence"):
        st.markdown(f"> {record['evidence']}")
        st.caption(
            "Demonstration evidence only. The record illustrates how a signal "
            "can progress through review, action, outcome, and learning."
        )


def render_reflection_form() -> None:
    completed_actions = get_completed_actions()

    st.markdown("## Record learning from completed work")

    if not completed_actions:
        st.caption(
            "Complete an action in Action Queue before recording its observed "
            "outcome and retained learning."
        )
        return

    selected_action_id = st.selectbox(
        "Choose a completed action",
        options=[action.id for action in completed_actions],
        format_func=lambda action_id: (
            f"{get_signal(get_action(action_id).signal_id)['id']} · "
            f"{get_action(action_id).title}"
        ),
    )

    existing_reflection = get_reflection_for_action(selected_action_id)

    if existing_reflection:
        st.caption(
            "A learning record already exists for this action. Saving the "
            "form will update it."
        )

    with st.form(f"reflection_form_{selected_action_id}"):
        outcome = st.text_area(
            "Observed outcome",
            value=(existing_reflection.outcome if existing_reflection else ""),
            placeholder="What happened after the action was completed?",
        )

        learning = st.text_area(
            "Learning retained",
            value=(existing_reflection.learning if existing_reflection else ""),
            placeholder="What should the organisation carry forward?",
        )

        next_step = st.text_input(
            "Next step",
            value=(existing_reflection.next_step if existing_reflection else ""),
            placeholder="What should happen next, if anything?",
        )

        submitted = st.form_submit_button("Save learning record")

    if submitted:
        if not outcome.strip() or not learning.strip():
            st.error(
                "Add both an observed outcome and retained learning before "
                "saving the record."
            )
            return

        saved = create_reflection(
            action_id=selected_action_id,
            outcome=outcome,
            learning=learning,
            next_step=next_step,
        )

        if saved:
            st.success("The learning record was saved.")
        else:
            st.warning(
                "The learning record is available in this session, but the "
                "host could not save it permanently."
            )

        st.rerun()


configure_page("Learning Loop | Meeting Memory Console")
render_sidebar_identity()
initialise_state()

render_page_header(
    eyebrow="Learning Loop",
    title="What the organisation carries forward",
    description=(
        "Review completed signals, observed outcomes, and the lessons the "
        "organisation has chosen to preserve from repeated meeting evidence."
    ),
)

render_notice(
    "Learning is recorded after human review and an observed outcome. These "
    "records are organizational memory, not automated conclusions or "
    "individual performance judgments."
)

render_reflection_form()

connected_records = [
    record
    for reflection in st.session_state.reflections
    if (record := build_reflection_record(reflection)) is not None
]

all_records = LEARNING_RECORDS + connected_records

render_divider()

st.markdown("## Search completed learning")

filter_columns = st.columns(3)

with filter_columns[0]:
    selected_area = st.selectbox(
        "Business area",
        ["All"] + sorted({record["area"] for record in all_records}),
    )

with filter_columns[1]:
    selected_impact = st.selectbox(
        "Impact",
        ["All"] + sorted({record["impact"] for record in all_records}),
    )

with filter_columns[2]:
    search_text = st.text_input(
        "Search",
        placeholder="Search outcomes, learning, owners, or evidence",
    )

filtered_records = [
    record
    for record in all_records
    if (selected_area == "All" or record["area"] == selected_area)
    and (selected_impact == "All" or record["impact"] == selected_impact)
    and matches_search(record, search_text)
]

render_divider()

metric_columns = st.columns(4)

with metric_columns[0]:
    render_metric("Completed signals", len(filtered_records))

with metric_columns[1]:
    render_metric(
        "High impact learning",
        sum(record["impact"] == "High" for record in filtered_records),
    )

with metric_columns[2]:
    render_metric(
        "Business areas",
        len({record["area"] for record in filtered_records}),
    )

with metric_columns[3]:
    render_metric(
        "Owners represented",
        len({record["owner"] for record in filtered_records}),
    )

render_divider()

st.markdown(f"## {len(filtered_records)} completed records in view")

if not filtered_records:
    st.info(
        "No completed learning records match the current filters. Adjust the "
        "filters and try again."
    )
else:
    for record in filtered_records:
        render_learning_record(record)
        render_divider()

st.markdown("## What this proves")

proof_columns = st.columns(3)

with proof_columns[0]:
    render_card(
        "Memory with evidence",
        "The original meeting observation remains available alongside the "
        "resulting outcome and retained learning.",
    )

with proof_columns[1]:
    render_card(
        "Accountability through action",
        "Each completed record makes the responsible owner and progression "
        "from signal to outcome visible.",
    )

with proof_columns[2]:
    render_card(
        "Learning beyond one meeting",
        "The organization can retain lessons from repeated evidence rather "
        "than treating meetings as isolated events.",
    )
