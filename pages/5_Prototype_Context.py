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
        "Understand the intended scope, limitations, privacy boundaries, and "
        "next steps for the Meeting Memory Console prototype."
    ),
)

render_notice(
    "This page explains what the demonstration shows, what it does not do, "
    "and how the design could evolve toward production use."
)

st.markdown("## What this prototype demonstrates")

st.write(
    "Meeting Memory Console demonstrates how organizations can turn useful "
    "conversation signals into structured, reviewable workflow without "
    "treating any single conversation as a final conclusion."
)

st.write(
    "The prototype makes signals visible, groups repeated signals into "
    "patterns, proposes destinations and owners, records human decisions, "
    "and preserves outcomes and learning."
)

st.write(
    "The current build uses fictional demonstration data. Its purpose is to "
    "make the intended operating model tangible and inspectable."
)

render_divider()

st.markdown("## What this prototype does not do")

limitations = [
    (
        "No live meeting ingestion",
        "The current build does not connect to meeting recordings, transcripts, "
        "calendars, or external conversation platforms.",
    ),
    (
        "No automated decisions",
        "Suggested routes and owners are illustrative. A person must review "
        "evidence before action is taken.",
    ),
    (
        "No production security controls",
        "Authentication, access controls, tenancy, audit infrastructure, and "
        "retention policies would be required before production use.",
    ),
    (
        "No replacement of existing systems",
        "The concept is intended to sit alongside CRM, project, communication, "
        "and data systems rather than replace them.",
    ),
]

for title, description in limitations:
    render_card(title, description)

render_divider()

st.markdown("## Privacy and intended boundaries")

st.write(
    "The demonstration data is fictional and contains no real company data, "
    "customer data, meeting recordings, transcripts, personal information, "
    "or internal information."
)

st.write(
    "In a production system, meeting-derived information would require clear "
    "rules for consent, access, retention, deletion, and approved use. Signals "
    "should describe organizational observations rather than serve as "
    "individual performance judgments."
)

st.write(
    "The human review step is an intentional product boundary. The system "
    "should support better organizational memory and accountability without "
    "turning conversation signals into unreviewed conclusions about people."
)

render_divider()

st.markdown("## Design principles")

principle_columns = st.columns(3)

with principle_columns[0]:
    render_card(
        "Evidence before automation",
        "Every signal or pattern should expose the evidence that supports it.",
    )

with principle_columns[1]:
    render_card(
        "Human review before action",
        "Consequential workflow changes should require a person to review "
        "and confirm the route.",
    )

with principle_columns[2]:
    render_card(
        "Learning after completion",
        "Outcomes and learning should remain visible after the immediate "
        "action is complete.",
    )

render_divider()

st.markdown("## Next steps toward production")

st.write(
    "A production implementation would require stakeholder requirements, user "
    "research, security review, privacy assessment, data governance, "
    "integration design, engineering collaboration, and measured rollout."
)

st.write(
    "The next technical phase would replace the demonstration records with "
    "validated domain models, persistent storage, repository abstractions, "
    "service-layer workflows, automated tests, and controlled integrations."
)

st.write(
    "The prototype is intentionally focused on proving the operating model "
    "before adding the complexity of live infrastructure."
)
