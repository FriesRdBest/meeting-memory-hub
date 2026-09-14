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

configure_page("Prototype Context | Meeting Memory Console")
render_sidebar_identity()

render_page_header(
    eyebrow="Prototype Context",
    title="What this demonstration proves",
    description=(
        "This prototype makes an operating model tangible: conversations can "
        "become evidence, evidence can inform accountable action, and completed "
        "work can become organizational learning."
    ),
)

render_notice(
    "This page explains the intended product boundaries. The demonstration "
    "uses fictional data to make the workflow visible and inspectable without "
    "making claims about live organizational activity."
)

st.markdown("## The operating model")

flow_columns = st.columns(4)

flow = [
    (
        flow_columns[0],
        "Signal Desk",
        "A useful observation from a conversation becomes visible with its "
        "source context and proposed route.",
    ),
    (
        flow_columns[1],
        "Pattern Library",
        "Related signals are reviewed together so repeated evidence can inform "
        "a decision before work begins.",
    ),
    (
        flow_columns[2],
        "Action Queue",
        "A person confirms ownership, destination, and the next move. The "
        "system records the decision instead of making it automatically.",
    ),
    (
        flow_columns[3],
        "Learning Loop",
        "Completed work is connected to its outcome and a lesson the "
        "organization chooses to retain.",
    ),
]

for column, title, description in flow:
    with column:
        render_card(title, description)

render_divider()

st.markdown("## What this prototype demonstrates")

demonstration_columns = st.columns(3)

with demonstration_columns[0]:
    render_card(
        "Signals remain visible",
        "Meaningful observations no longer disappear when a conversation ends. "
        "Their supporting evidence remains available for review.",
    )

with demonstration_columns[1]:
    render_card(
        "People remain accountable",
        "Suggested routes do not become action automatically. A human reviews "
        "the evidence, confirms the route, and records the decision.",
    )

with demonstration_columns[2]:
    render_card(
        "Learning compounds",
        "Outcomes and retained learning stay connected to the original signal, "
        "strengthening the organizational memory available next time.",
    )

render_divider()

st.markdown("## Why Pattern Library comes before Action Queue")

render_card(
    "Memory before commitment",
    "Organizations often revisit the same problem because the relevant "
    "context lives across separate meetings, teams, and people. Pattern "
    "Library belongs between Signal Desk and Action Queue because it gives "
    "the person making a decision a chance to see repeated evidence before "
    "resources, ownership, and urgency are committed.",
)

render_divider()

st.markdown("## What this prototype does not do")

limitations = [
    (
        "No live meeting ingestion",
        "The current build does not connect to recordings, transcripts, "
        "calendars, or external conversation platforms.",
    ),
    (
        "No automated decisions",
        "Proposed routes and owners are illustrative. A person must review "
        "evidence before consequential work progresses.",
    ),
    (
        "No production security controls",
        "Authentication, access controls, tenancy, audit infrastructure, "
        "retention policies, and governance would be needed before production use.",
    ),
    (
        "No replacement for existing systems",
        "The concept is designed to work alongside CRM, project, communication, "
        "and data systems rather than replace them.",
    ),
]

limitation_columns = st.columns(2)

for index, (title, description) in enumerate(limitations):
    with limitation_columns[index % 2]:
        render_card(title, description)

render_divider()

st.markdown("## Privacy and intended boundaries")

st.write(
    "The demonstration data is fictional. It contains no real customer data, "
    "meeting recordings, transcripts, personal information, or internal "
    "organizational information."
)

st.write(
    "A production system would require clear rules for consent, access, "
    "retention, deletion, security, and approved use. Signals should describe "
    "organizational observations, not become unreviewed judgments about people."
)

st.write(
    "Human review is an intentional product boundary. The system is designed "
    "to improve organizational memory and accountability without turning "
    "meeting signals into automatic conclusions."
)

render_divider()

st.markdown("## Principles that guide the product")

principle_columns = st.columns(3)

with principle_columns[0]:
    render_card(
        "Evidence before automation",
        "Every signal and pattern should expose the evidence that supports it.",
    )

with principle_columns[1]:
    render_card(
        "Human review before action",
        "Consequential workflow changes require a person to review and confirm "
        "the appropriate route.",
    )

with principle_columns[2]:
    render_card(
        "Learning after completion",
        "Outcomes and retained learning remain visible after immediate work "
        "has ended, improving the next decision.",
    )

render_divider()

st.markdown("## Path toward production")

st.write(
    "A production implementation would begin with stakeholder requirements, "
    "user research, privacy assessment, data governance, security review, "
    "integration design, engineering collaboration, and a measured rollout."
)

st.write(
    "The next technical stage would replace demonstration records with live "
    "data pipelines, durable storage, validated access control, multi user "
    "collaboration, auditability, and carefully controlled intelligence "
    "features."
)

st.write(
    "The prototype remains intentionally focused. It proves the operating "
    "model before adding the complexity of production infrastructure."
)
