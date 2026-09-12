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


def matches_search(signal: dict[str, str], search_text: str) -> bool:
    if not search_text:
        return True

    searchable_text = " ".join(signal.values()).lower()
    return search_text.lower() in searchable_text


def render_signal(signal: dict[str, str]) -> None:
    st.markdown(f"### {signal['id']} · {signal['title']}")

    render_badges(
        [
            signal["type"],
            signal["area"],
            f"{signal['impact']} impact",
            f"{signal['confidence']} confidence",
            signal["status"],
        ]
    )

    st.write(signal["evidence"])

    columns = st.columns(3)

    with columns[0]:
        st.caption("Proposed destination")
        st.write(signal["destination"])

    with columns[1]:
        st.caption("Proposed owner")
        st.write(signal["owner"])

    with columns[2]:
        st.caption("Source context")
        st.write(signal["context"])

    with st.expander("View evidence context"):
        st.markdown(f"> {signal['evidence']}")
        st.caption(
            "Demonstration evidence only. This signal is intended for human "
            "review rather than automatic action."
        )


configure_page("Signal Desk | Meeting Memory Console")
render_sidebar_identity()

render_page_header(
    eyebrow="Signal Desk",
    title="What deserves attention",
    description=(
        "Review meaningful signals from conversations, inspect the evidence "
        "behind them, and see the proposed route for human consideration."
    ),
)

render_notice(
    "This workspace uses fictional demonstration signals. The proposed "
    "destination and owner are suggestions for review, not automated decisions."
)

signals = st.session_state.get("signals", [])

st.markdown("## Filter signals")

filter_columns = st.columns(4)

with filter_columns[0]:
    selected_type = st.selectbox(
        "Signal type",
        ["All"] + sorted({signal["type"] for signal in signals}),
    )

with filter_columns[1]:
    selected_impact = st.selectbox(
        "Impact",
        ["All"] + sorted({signal["impact"] for signal in signals}),
    )

with filter_columns[2]:
    selected_status = st.selectbox(
        "Status",
        ["All"] + sorted({signal["status"] for signal in signals}),
    )

with filter_columns[3]:
    search_text = st.text_input(
        "Search",
        placeholder="Search signals, owners, or evidence",
    )

filtered_signals = [
    signal
    for signal in signals
    if (
        selected_type == "All"
        or signal["type"] == selected_type
    )
    and (
        selected_impact == "All"
        or signal["impact"] == selected_impact
    )
    and (
        selected_status == "All"
        or signal["status"] == selected_status
    )
    and matches_search(signal, search_text)
]

render_divider()

metric_columns = st.columns(4)

with metric_columns[0]:
    render_metric("Signals in view", len(filtered_signals))

with metric_columns[1]:
    render_metric(
        "Needs review",
        sum(
            signal["status"] == "Needs review"
            for signal in filtered_signals
        ),
    )

with metric_columns[2]:
    render_metric(
        "High impact",
        sum(
            signal["impact"] == "High"
            for signal in filtered_signals
        ),
    )

with metric_columns[3]:
    render_metric(
        "Customer signals",
        sum(
            signal["area"] == "Customer"
            for signal in filtered_signals
        ),
    )

render_divider()

st.markdown(f"## {len(filtered_signals)} signals in view")

if not filtered_signals:
    st.info(
        "No signals match the current filters. Adjust the filters and try again."
    )
else:
    for signal in filtered_signals:
        render_signal(signal)
        render_divider()

st.markdown("## Next layer")

render_card(
    "From signals to patterns",
    "The next workspace groups repeated signals across conversations so "
    "recurring themes can be reviewed without treating one conversation as a "
    "complete conclusion.",
)
