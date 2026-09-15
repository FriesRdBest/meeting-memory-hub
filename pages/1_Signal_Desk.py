from __future__ import annotations

import time

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
    render_signal_loader,
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

    detail_columns = st.columns(3)

    with detail_columns[0]:
        st.caption("Proposed destination")
        st.write(signal["destination"])

    with detail_columns[1]:
        st.caption("Proposed owner")
        st.write(signal["owner"])

    with detail_columns[2]:
        st.caption("Source context")
        st.write(signal["context"])

    with st.expander("Open evidence context"):
        st.markdown(f"> {signal['evidence']}")
        st.caption(
            "This is source material for human review. The signal is not an "
            "automatic conclusion or instruction to act."
        )


configure_page("Signal Desk | Meeting Memory Console")
render_sidebar_identity()

signals = st.session_state.get("signals", [])

# Artificial delay to make the loader visible (for demo / polish)
if "signals_loaded" not in st.session_state:
    render_signal_loader("Tuning into signals...")
    time.sleep(0.7)
    st.session_state.signals_loaded = True
    st.rerun()

render_page_header(
    eyebrow="Signal Desk",
    title="What deserves attention",
    description=(
        "Review meaningful signals from conversations, preserve the evidence "
        "behind them, and identify what needs human consideration next."
    ),
)

render_notice(
    "A signal is an observation, not a conclusion. Proposed ownership and "
    "destination are suggestions that require human review before action."
)

st.info(
    "Demo journey: Start with **SIG-001**. Review the evidence here, then "
    "open Pattern Library to see why repeated context matters before you "
    "record a decision in Action Queue."
)

st.markdown("## Find the right signal")

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
        placeholder="Search signals, evidence, owners, or context",
    )

filtered_signals = [
    signal
    for signal in signals
    if (selected_type == "All" or signal["type"] == selected_type)
    and (selected_impact == "All" or signal["impact"] == selected_impact)
    and (selected_status == "All" or signal["status"] == selected_status)
    and matches_search(signal, search_text)
]

render_divider()

metric_columns = st.columns(4)

with metric_columns[0]:
    render_metric("Signals in view", len(filtered_signals))

with metric_columns[1]:
    render_metric(
        "Needs review",
        sum(signal["status"] == "Needs review" for signal in filtered_signals),
    )

with metric_columns[2]:
    render_metric(
        "High impact",
        sum(signal["impact"] == "High" for signal in filtered_signals),
    )

with metric_columns[3]:
    render_metric(
        "Customer signals",
        sum(signal["area"] == "Customer" for signal in filtered_signals),
    )

render_divider()

st.markdown(f"## {len(filtered_signals)} signals in view")

if not filtered_signals:
    st.info(
        "No signals match the current filters. Adjust the filters or search "
        "terms and try again."
    )
else:
    for signal in filtered_signals:
        render_signal(signal)
        render_divider()

st.markdown("## The next review layer")

render_card(
    "From a signal to a pattern",
    "One conversation can reveal something important, but it is not always "
    "enough to justify a decision. Pattern Library groups related signals "
    "across conversations so the organization can distinguish a one off "
    "observation from a recurring issue before action is taken.",
)
