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
        "destination": "Leadership follow-up",
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
            str(pattern["category"]),
            str(pattern["trend"]),
            str(pattern["status"]),
            f"{pattern['signals']} linked signals",
            f"{pattern['accounts']} affected accounts",
        ]
    )

    st.write(str(pattern["description"]))

    columns = st.columns(3)

    with columns[0]:
        st.caption("Proposed destination")
        st.write(str(pattern["destination"]))

    with columns[1]:
        st.caption("Proposed owner")
        st.write(str(pattern["owner"]))

    with columns[2]:
        st.caption("Pattern direction")
        st.write(str(pattern["trend"]))

    with st.expander("View supporting evidence"):
        for evidence in pattern["evidence"]:
            st.markdown(f"> {evidence}")

        st.caption(
            "Supporting evidence is illustrative and intended for human "
            "review rather than automatic conclusion."
        )


configure_page("Pattern Library | Meeting Memory Console")
render_sidebar_identity()

render_page_header(
    eyebrow="Pattern Library",
    title="What keeps happening",
    description=(
        "Review recurring themes across conversations, inspect the evidence "
        "behind them, and see where each pattern should go next."
    ),
)

render_notice(
    "Patterns group related demonstration signals across conversations. "
    "They make repeated evidence visible without treating an individual "
    "conversation as a complete conclusion."
)

st.markdown("## Filter patterns")

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
        placeholder="Search themes, owners, destinations, or evidence",
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
        "Needs attention",
        sum(pattern["status"] == "Needs attention" for pattern in filtered_patterns),
    )

with metric_columns[2]:
    render_metric(
        "Increasing",
        sum(pattern["trend"] == "Increasing" for pattern in filtered_patterns),
    )

with metric_columns[3]:
    render_metric(
        "Linked signals",
        sum(int(pattern["signals"]) for pattern in filtered_patterns),
    )

render_divider()

st.markdown(f"## {len(filtered_patterns)} patterns in view")

if not filtered_patterns:
    st.info("No patterns match the current filters. Adjust the filters and try again.")
else:
    for pattern in filtered_patterns:
        render_pattern(pattern)
        render_divider()

st.markdown("## Next layer")

render_card(
    "From patterns to action",
    "The next workspace lets a person review a proposed route, confirm "
    "ownership, record a decision, and preserve the workflow history.",
)
