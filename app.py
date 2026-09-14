from __future__ import annotations

import streamlit as st

from data.demo_signals import DEMO_SIGNALS
from utils.ui import (
    configure_page,
    render_card,
    render_divider,
    render_metric,
    render_notice,
    render_page_header,
    render_sidebar_identity,
)


def initialise_workflow_state() -> None:
    if "signals" not in st.session_state:
        st.session_state.signals = [signal.copy() for signal in DEMO_SIGNALS]

    if "actions" not in st.session_state:
        st.session_state.actions = []

    if "reflections" not in st.session_state:
        st.session_state.reflections = []


def render_overview() -> None:
    render_sidebar_identity()

    signals = st.session_state.get("signals", [])
    actions = st.session_state.get("actions", [])
    reflections = st.session_state.get("reflections", [])

    signals_needing_review = sum(
        signal["status"] == "Needs review" for signal in signals
    )
    patterns_in_motion = sum(
        signal["status"] in {"Needs review", "Watching"} for signal in signals
    )
    actions_in_progress = sum(
        action.status == "In progress" for action in actions
    )

    render_page_header(
        eyebrow="Meeting Memory Console",
        title="From conversation to consequence",
        description=(
            "A working organizational intelligence system that makes important "
            "signals visible, checks what the organization already knows, "
            "creates accountable action, and preserves learning."
        ),
    )

    render_notice(
        "This demonstration uses fictional data. It proves the operating "
        "model: a useful signal can become an accountable action and a "
        "recorded learning outcome within one workspace session."
    )

    st.markdown("## The organization at a glance")

    metric_columns = st.columns(4)

    with metric_columns[0]:
        render_metric("Signals needing review", signals_needing_review)

    with metric_columns[1]:
        render_metric("Patterns in motion", patterns_in_motion)

    with metric_columns[2]:
        render_metric("Work in progress", actions_in_progress)

    with metric_columns[3]:
        render_metric("Learning retained", len(reflections))

    render_divider()

    st.markdown("## How the system works")

    workflow_columns = st.columns(4)

    workflow = [
        (
            workflow_columns[0],
            "1. Signal Desk",
            "Useful observations from conversations become visible with their "
            "original evidence and a proposed route for human review.",
        ),
        (
            workflow_columns[1],
            "2. Pattern Library",
            "Related signals are examined together so the organization can "
            "check what keeps happening before it commits resources.",
        ),
        (
            workflow_columns[2],
            "3. Action Queue",
            "A person confirms ownership, destination, and the next move. "
            "The system records the decision rather than making it automatically.",
        ),
        (
            workflow_columns[3],
            "4. Learning Loop",
            "Completed work is connected to an observed outcome and retained "
            "learning, making the next decision more informed.",
        ),
    ]

    for column, title, description in workflow:
        with column:
            render_card(title, description)

    render_divider()

    st.markdown("## Start with one complete journey")

    journey_columns = st.columns(2)

    with journey_columns[0]:
        render_card(
            "Explore the workflow",
            "Begin in Signal Desk with SIG-001, the onboarding friction signal. "
            "Review the evidence, inspect Pattern Library for repeated context, "
            "then move to Action Queue to start and complete the work. Finish "
            "in Learning Loop by recording what the organization learned.",
        )

    with journey_columns[1]:
        render_card(
            "Understand the concept",
            "Open Prototype Context to understand the product philosophy, "
            "boundaries, privacy principles, and what a production "
            "implementation would require.",
        )

    render_divider()

    st.markdown("## Why Pattern Library comes before action")

    render_card(
        "Memory before momentum",
        "Organizations often repeat work because important context stays inside "
        "individual meetings, teams, or people. Pattern Library sits between "
        "Signal Desk and Action Queue so a human can see whether the company "
        "has encountered the issue before deciding what to do next.",
    )

    render_divider()

    st.markdown("## Current scope")

    st.write(
        "This prototype focuses on the workflow from signal to action to "
        "learning. It uses fictional demonstration data and session based "
        "records. Authentication, live integrations, multi user collaboration, "
        "production security, durable cloud storage, and advanced intelligence "
        "features remain future work."
    )


initialise_workflow_state()
configure_page("Meeting Memory Console")

pages = [
    st.Page(
        render_overview,
        title="Overview",
        icon=":material/home:",
        url_path="overview",
    ),
    st.Page(
        "pages/1_Signal_Desk.py",
        title="Signal Desk",
        icon=":material/search_insights:",
        url_path="signal-desk",
    ),
    st.Page(
        "pages/2_Pattern_Library.py",
        title="Pattern Library",
        icon=":material/hub:",
        url_path="pattern-library",
    ),
    st.Page(
        "pages/3_Action_Queue.py",
        title="Action Queue",
        icon=":material/task_alt:",
        url_path="action-queue",
    ),
    st.Page(
        "pages/4_Learning_Loop.py",
        title="Learning Loop",
        icon=":material/school:",
        url_path="learning-loop",
    ),
    st.Page(
        "pages/5_Prototype_Context.py",
        title="Prototype Context",
        icon=":material/info:",
        url_path="prototype-context",
    ),
]

current_page = st.navigation(pages, position="sidebar")
current_page.run()
