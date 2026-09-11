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


def matches_search(record: dict[str, str], search_text: str) -> bool:
    if not search_text:
        return True

    searchable_text = " ".join(record.values()).lower()
    return search_text.lower() in searchable_text


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

    with st.expander("View original evidence"):
        st.markdown(f"> {record['evidence']}")
        st.caption(
            "Demonstration evidence only. The record illustrates how a signal "
            "can progress through review, action, outcome, and learning."
        )


configure_page("Learning Loop | Meeting Memory Console")
render_sidebar_identity()

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

metric_columns = st.columns(4)

with metric_columns[0]:
    render_metric("Completed signals", len(LEARNING_RECORDS))

with metric_columns[1]:
    render_metric(
        "High impact learning",
        sum(record["impact"] == "High" for record in LEARNING_RECORDS),
    )

with metric_columns[2]:
    render_metric(
        "Business areas",
        len({record["area"] for record in LEARNING_RECORDS}),
    )

with metric_columns[3]:
    render_metric(
        "Owners represented",
        len({record["owner"] for record in LEARNING_RECORDS}),
    )

render_divider()

st.markdown("## Search completed learning")

filter_columns = st.columns(3)

with filter_columns[0]:
    selected_area = st.selectbox(
        "Business area",
        ["All"] + sorted({record["area"] for record in LEARNING_RECORDS}),
    )

with filter_columns[1]:
    selected_impact = st.selectbox(
        "Impact",
        ["All"] + sorted({record["impact"] for record in LEARNING_RECORDS}),
    )

with filter_columns[2]:
    search_text = st.text_input(
        "Search",
        placeholder="Search outcomes, learning, owners, or evidence",
    )

filtered_records = [
    record
    for record in LEARNING_RECORDS
    if (
        selected_area == "All"
        or record["area"] == selected_area
    )
    and (
        selected_impact == "All"
        or record["impact"] == selected_impact
    )
    and matches_search(record, search_text)
]

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
