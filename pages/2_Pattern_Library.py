from __future__ import annotations

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

PATTERNS = [
    {
        "id": "PAT-001",
        "title": "Onboarding friction is becoming a repeatable adoption risk",
        "category": "Customer experience",
        "trend": "Increasing",
        "status": "Needs attention",
        "signals": 3,
        "accounts": 4,
        "owner": "Customer Success",
        "destination": "Product discovery",
        "description": (
            "Multiple conversations point to early workflow friction that "
            "may be slowing adoption for new teams."
        ),
        "evidence": [
            "The first workflow feels harder than it should for new teams.",
            "Implementation effort is coming up earlier in customer conversations.",
            "Customers are asking for more guidance before they commit to rollout.",
        ],
    },
    {
        "id": "PAT-002",
        "title": "Reporting requests are forming a product theme",
        "category": "Product insight",
        "trend": "Stable",
        "status": "Ready for review",
        "signals": 2,
        "accounts": 3,
        "owner": "Product Operations",
        "destination": "Roadmap review",
        "description": (
            "Reporting needs have appeared in more than one conversation and "
            "may represent a broader product opportunity."
        ),
        "evidence": [
            "The reporting question came up again this week.",
            "Teams want clearer visibility into progress and outcomes.",
        ],
    },
    {
        "id": "PAT-003",
        "title": "Important commitments are losing operational ownership",
        "category": "Operating model",
        "trend": "Increasing",
        "status": "Needs attention",
        "signals": 3,
        "accounts": 2,
        "owner": "Leadership Operations",
        "destination": "Leadership follow up",
        "description": (
            "Strategic commitments are being acknowledged in meetings without "
            "a consistent owner or visible next step."
        ),
        "evidence": [
            "Everyone agreed that this matters, but ownership was unclear.",
            "The next step was discussed without a named accountable person.",
            "A previous commitment was revisited because progress was not visible.",
        ],
    },
]


def matches_search(pattern: dict[str, object], search_text: str) -> bool:
    if not search_text:
        return True

    searchable_text = " ".join(
        [
            str(pattern["id"]),
            str(pattern["title"]),
            str(pattern["category"]),
            str(pattern["trend"]),
            str(pattern["status"]),
            str(pattern["owner"]),
            str(pattern["destination"]),
            str(pattern["description"]),
            " ".join(str(item) for item in pattern["evidence"]),
        ]
    ).lower()

    return search_text.lower() in searchable_text


def render_pattern(pattern: dict[str, object]) -> None:
    st.markdown(f"### {pattern['id']} · {pattern['title']}")

    render_badges(
        [
            str(pattern["status"]),
            str(pattern["trend"]),
            str(pattern["category"]),
            f"{pattern['signals']} linked signals",
            f"{pattern['accounts']} affected accounts",
        ]
    )

    st.write(str(pattern["description"]))

    detail_columns = st.columns(3)

    with detail_columns[0]:
        st.caption("Proposed destination")
        st.write(str(pattern["destination"]))

    with detail_columns[1]:
        st.caption("Proposed owner")
        st.write(str(pattern["owner"]))

    with detail_columns[2]:
        st.caption("Pattern direction")
        st.write(str(pattern["trend"]))

    with st.expander("Open supporting evidence"):
        st.caption(
            "This pattern is based on related signals across conversations. "
            "Review the evidence before deciding whether work should begin."
        )

        for evidence in pattern["evidence"]:
            st.markdown(f"> {evidence}")


configure_page("Pattern Library | Meeting Memory Console")
render_sidebar_identity()

render_page_header(
    eyebrow="Pattern Library",
    title="What keeps happening",
    description=(
        "Look across conversations before deciding what to do. Patterns make "
        "repeated evidence visible so the organization can act with context, "
        "not simply react to the latest meeting."
    ),
)

render_notice(
    "Pattern Library is the memory check before action. It helps people see "
    "whether a signal is isolated, recurring, increasing, or already known "
    "before resources and ownership are committed."
)

st.markdown("## What is changing")

health_columns = st.columns(3)

with health_columns[0]:
    render_card(
        "Repeated customer friction",
        "Onboarding friction appears across three linked signals and four "
        "affected accounts. The pattern is increasing and needs attention.",
    )

with health_columns[1]:
    render_card(
        "Emerging product theme",
        "Reporting needs are appearing across separate conversations. The "
        "evidence is ready for product review rather than a one off request.",
    )

with health_columns[2]:
    render_card(
        "Ownership gap",
        "Important commitments are recurring without consistent ownership. "
        "The organization may be acknowledging work without moving it forward.",
    )

render_divider()

st.markdown("## Find the right pattern")

filter_columns = st.columns(4)

with filter_columns[0]:
    selected_category = st.selectbox(
        "Category",
        ["All"] + sorted({str(pattern["category"]) for pattern in PATTERNS}),
    )

with filter_columns[1]:
    selected_trend = st.selectbox(
        "Trend",
        ["All"] + sorted({str(pattern["trend"]) for pattern in PATTERNS}),
    )

with filter_columns[2]:
    selected_status = st.selectbox(
        "Status",
        ["All"] + sorted({str(pattern["status"]) for pattern in PATTERNS}),
    )

with filter_columns[3]:
    search_text = st.text_input(
        "Search",
        placeholder="Search themes, evidence, owners, or destinations",
    )

filtered_patterns = [
    pattern
    for pattern in PATTERNS
    if (selected_category == "All" or pattern["category"] == selected_category)
    and (selected_trend == "All" or pattern["trend"] == selected_trend)
    and (selected_status == "All" or pattern["status"] == selected_status)
    and matches_search(pattern, search_text)
]

render_divider()

metric_columns = st.columns(4)

with metric_columns[0]:
    render_metric("Patterns in view", len(filtered_patterns))

with metric_columns[1]:
    render_metric(
        "Need attention",
        sum(pattern["status"] == "Needs attention" for pattern in filtered_patterns),
    )

with metric_columns[2]:
    render_metric(
        "Increasing",
        sum(pattern["trend"] == "Increasing" for pattern in filtered_patterns),
    )

with metric_columns[3]:
    render_metric(
        "Evidence linked",
        sum(int(pattern["signals"]) for pattern in filtered_patterns),
    )

render_divider()

st.markdown(f"## {len(filtered_patterns)} patterns in view")

if not filtered_patterns:
    st.info(
        "No patterns match the current filters. Adjust the filters or search "
        "terms and try again."
    )
else:
    for pattern in filtered_patterns:
        render_pattern(pattern)
        render_divider()

st.markdown("## The decision layer")

render_card(
    "From repeated evidence to accountable action",
    "Pattern Library does not make the decision. It gives the person making "
    "the decision the context needed to avoid duplicated work, false urgency, "
    "or an unsupported conclusion. Action Queue is where ownership and the "
    "next move are confirmed.",
)
