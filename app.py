from __future__ import annotations

import streamlit as st

from utils.ui import (
    configure_page,
    render_divider,
    render_page_header,
    render_sidebar_identity,
)


def render_introduction() -> None:
    st.markdown(
        "Meeting Memory Console is a prototype that shows how organisations "
        "can turn conversation signals into structured, auditable workflow "
        "without treating any single conversation as a final conclusion."
    )

    st.markdown(
        "The console groups repeated evidence into patterns, routes signals "
        "to the right owners, records human decisions, and preserves the "
        "learning that the organisation carries forward."
    )

    st.markdown(
        "This demonstration uses simulated data to prove the workflow. "
        "The architecture is designed to support live data ingestion, "
        "integration with existing tools, and production controls in a "
        "future phase."
    )


def render_how_to_use() -> None:
    st.markdown("### How to use this demonstration")

    st.markdown(
        "Start in the **Signal Desk** to see the raw signals extracted from "
        "demonstration conversations. Filter by type, business area, impact, "
        "and confidence to understand what evidence is available."
    )

    st.markdown(
        "Move to the **Pattern Library** to see how repeated signals form "
        "themes across conversations. Inspect the supporting evidence behind "
        "each pattern and see where the pattern should go next."
    )

    st.markdown(
        "Use the **Action Queue** to review the route proposed for each signal, "
        "adjust ownership and destination, record a decision, and track "
        "progress through to completion."
    )

    st.markdown(
        "Visit the **Learning Loop** to see what the organisation has learned "
        "from completed signals. Review recorded outcomes, learning notes, "
        "and the workflow history that led to each conclusion."
    )

    st.markdown(
        "Read the **Prototype Context** page to understand what this "
        "demonstration shows, what it does not do, and how the design is "
        "intended to evolve toward production use."
    )


def render_design_principles() -> None:
    st.markdown("### Design principles")

    st.markdown(
        "**Evidence based** — Every signal and pattern is backed by concrete "
        "evidence from conversations. The console never presents an insight "
        "without showing where it came from."
    )

    st.markdown(
        "**Human in the loop** — Automated suggestions are always reviewed by "
        "a person before any action is taken. The console records who made "
        "each decision and why."
    )

    st.markdown(
        "**Auditable workflow** — Every change is recorded in the workflow "
        "history. The organisation can see how a signal moved from first "
        "observation to completed outcome."
    )

    st.markdown(
        "**Pattern aware** — Repeated evidence across conversations forms "
        "patterns that are visible and actionable. The console treats "
        "patterns as organisational observations, not individual judgments."
    )

    st.markdown(
        "**Learning oriented** — Completed signals record outcomes and "
        "learning so the organisation can carry forward what it has "
        "discovered through repeated evidence."
    )


def render_architecture_overview() -> None:
    st.markdown("### Architecture overview")

    st.markdown(
        "The console is built with a layered architecture: models define the "
        "domain, repositories isolate data access, services contain business "
        "logic, and the Streamlit pages present the user facing workspaces."
    )

    st.markdown(
        "This separation allows the demonstration to use simulated data now "
        "and replace it with live data sources later without rewriting the "
        "core workflow logic."
    )

    st.markdown(
        "The visual system is shared across pages so that metrics, badges, "
        "headers, and notices are consistent and the user experience feels "
        "cohesive."
    )


configure_page("Meeting Memory Console")
render_sidebar_identity()

render_page_header(
    eyebrow="Meeting Memory Console",
    title="Turn conversation signals into auditable workflow",
    description=(
        "A prototype that shows how organisations can preserve the memory "
        "of meetings without treating any single conversation as a final "
        "conclusion."
    ),
)

render_introduction()
render_divider()
render_how_to_use()
render_divider()
render_design_principles()
render_divider()
render_architecture_overview()
