from __future__ import annotations

import streamlit as st

from utils.ui import (
    configure_page,
    render_card,
    render_divider,
    render_notice,
    render_page_header,
    render_sidebar_identity,
)


def render_overview() -> None:
    render_sidebar_identity()

    render_page_header(
        eyebrow="Meeting Memory Console",
        title="From conversation to consequence",
        description=(
            "A working prototype for turning meeting signals into trusted "
            "memory, accountable action, and visible learning."
        ),
    )

    render_notice(
        "This first deployment is intentionally lightweight. It proves the "
        "application shell and visual system before the deeper workspaces "
        "are connected."
    )

    st.markdown("## Start here")

    st.write(
        "You can explore the prototype in either direction. Start with the "
        "workflow if you want to see the product in action, or start with "
        "Prototype Context if you want to understand the intended scope, "
        "boundaries, and operating model first."
    )

    review_columns = st.columns(2)

    with review_columns[0]:
        render_card(
            "Explore the workflow",
            "Open Signal Desk, then Pattern Library, Action Queue, and "
            "Learning Loop to follow the journey from evidence to action "
            "and retained organizational learning.",
        )

    with review_columns[1]:
        render_card(
            "Understand the concept",
            "Open Prototype Context first to review the demonstration scope, "
            "privacy boundaries, limitations, and production considerations "
            "before exploring the workspaces.",
        )

    render_divider()

    st.markdown("## What this prototype is designed to do")

    st.write(
        "Meeting Memory Console focuses on what happens after a useful signal "
        "appears in a meeting. It makes the signal visible, preserves the "
        "evidence behind it, proposes an accountable route, and creates a "
        "clear path toward action and learning."
    )

    render_divider()

    columns = st.columns(3)

    with columns[0]:
        render_card(
            "Preserve the signal",
            "Make meaningful observations visible instead of allowing them "
            "to disappear when the meeting ends.",
        )

    with columns[1]:
        render_card(
            "Create accountability",
            "Give each useful signal a proposed destination, owner, and next "
            "step for human review.",
        )

    with columns[2]:
        render_card(
            "Carry learning forward",
            "Record outcomes and learning so repeated evidence can improve "
            "what happens next.",
        )

    render_divider()

    st.markdown("## Workspace map")

    workspace_columns = st.columns(5)

    workspaces = [
        (
            workspace_columns[0],
            "Signal Desk",
            "Review meaningful signals that need attention.",
        ),
        (
            workspace_columns[1],
            "Pattern Library",
            "Discover themes that repeat across conversations.",
        ),
        (
            workspace_columns[2],
            "Action Queue",
            "Confirm destination, ownership, action, and status.",
        ),
        (
            workspace_columns[3],
            "Learning Loop",
            "Review outcomes and recorded organizational learning.",
        ),
        (
            workspace_columns[4],
            "Prototype Context",
            "Review scope, boundaries, and the path toward production.",
        ),
    ]

    for column, title, description in workspaces:
        with column:
            render_card(title, description)

    render_divider()

    st.markdown("## Current scope")

    st.write(
        "This deployment uses demonstration data and focuses on proving the "
        "workflow concept. Authentication, live integrations, multi-user "
        "collaboration, production security, and background processing remain "
        "future work."
    )


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
