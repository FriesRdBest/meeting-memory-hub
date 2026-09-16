from __future__ import annotations

from datetime import datetime
from pathlib import Path

import streamlit as st

from models.pattern import Pattern
from repositories.pattern_repository import PatternRepository
from services.pattern_service import PatternService
from utils.ui import (
    configure_page,
    render_badges,
    render_card,
    render_divider,
    render_empty_state,
    render_metric,
    render_notice,
    render_page_header,
    render_sidebar_identity,
)

PATTERN_FILE_PATH = Path("data/patterns.json")


def get_pattern_service() -> PatternService:
    return PatternService(PatternRepository(PATTERN_FILE_PATH))


def initialise_state() -> None:
    if "patterns" not in st.session_state:
        try:
            st.session_state.patterns = get_pattern_service().list_patterns()
        except (OSError, ValueError, KeyError):
            st.session_state.patterns = []

    if "pattern_review_feedback" not in st.session_state:
        st.session_state.pattern_review_feedback = None


def save_patterns() -> bool:
    try:
        get_pattern_service().save_patterns(st.session_state.patterns)
        return True
    except OSError:
        return False


def get_signal(signal_id: str) -> dict[str, str] | None:
    return next(
        (
            signal
            for signal in st.session_state.get("signals", [])
            if signal["id"] == signal_id
        ),
        None,
    )


def get_action(action_id: str) -> object | None:
    return next(
        (
            action
            for action in st.session_state.get("actions", [])
            if action.id == action_id
        ),
        None,
    )


def get_reflection(reflection_id: str) -> object | None:
    return next(
        (
            reflection
            for reflection in st.session_state.get("reflections", [])
            if reflection.id == reflection_id
        ),
        None,
    )


def get_pattern_confidence(pattern: Pattern) -> str:
    evidence_count = pattern.evidence_count

    if evidence_count >= 5:
        return "High"

    if evidence_count >= 3:
        return "Medium"

    return "Early"


def get_source_summary(pattern: Pattern) -> str:
    parts = []

    if pattern.source_signal_ids:
        parts.append(f"{len(pattern.source_signal_ids)} signals")

    if pattern.source_action_ids:
        parts.append(f"{len(pattern.source_action_ids)} actions")

    if pattern.source_reflection_ids:
        parts.append(f"{len(pattern.source_reflection_ids)} learnings")

    if not parts:
        return "No linked evidence"

    return " · ".join(parts)


def matches_search(pattern: Pattern, search_text: str) -> bool:
    if not search_text:
        return True

    searchable_text = " ".join(
        [
            pattern.id,
            pattern.title,
            pattern.category,
            pattern.trend,
            pattern.status,
            pattern.confidence,
            pattern.proposed_owner,
            pattern.proposed_destination,
            pattern.description,
            pattern.review_note,
            pattern.reviewed_by,
        ]
    ).lower()

    return search_text.lower() in searchable_text


def update_pattern_review(
    pattern: Pattern,
    decision: str,
    reviewer: str,
    review_note: str,
) -> bool:
    status_by_decision = {
        "Confirm pattern": "Confirmed",
        "Keep watching": "Emerging",
        "Dismiss for now": "Dismissed",
    }

    pattern.status = status_by_decision[decision]
    pattern.confidence = get_pattern_confidence(pattern)
    pattern.reviewed_by = reviewer.strip() or "Unassigned reviewer"
    pattern.review_note = review_note.strip()
    pattern.reviewed_at = datetime.now().strftime("%b %d, %Y at %I:%M %p")

    return save_patterns()


def render_review_feedback() -> None:
    feedback = st.session_state.get("pattern_review_feedback")

    if not feedback:
        return

    if feedback["saved"]:
        st.success(
            f"{feedback['pattern_id']} is now recorded as '{feedback['decision']}'."
        )
        return

    st.warning(
        f"{feedback['pattern_id']} was updated for this session, but the host "
        "could not save the review permanently."
    )


def render_signal_evidence(pattern: Pattern) -> None:
    st.markdown("#### Linked signals")

    if not pattern.source_signal_ids:
        st.caption("No signal evidence is linked to this emerging pattern.")
        return

    for signal_id in pattern.source_signal_ids:
        signal = get_signal(signal_id)

        if not signal:
            st.caption(f"{signal_id} · Signal is not available in this session.")
            continue

        st.markdown(f"**{signal['id']} · {signal['title']}**")

        render_badges(
            [
                signal["type"],
                signal["area"],
                f"{signal['impact']} impact",
                f"{signal['confidence']} confidence",
                signal["status"],
            ]
        )

        st.markdown(f"> {signal['evidence']}")

        if signal.get("context"):
            st.caption(f"Context: {signal['context']}")

        render_divider()


def render_action_evidence(pattern: Pattern) -> None:
    st.markdown("#### Linked actions")

    if not pattern.source_action_ids:
        st.caption(
            "No completed or in progress actions are linked to this pattern yet."
        )
        return

    for action_id in pattern.source_action_ids:
        action = get_action(action_id)

        if not action:
            st.caption(f"{action_id} · Action is not available in this session.")
            continue

        st.markdown(f"**{action.id} · {action.title}**")

        render_badges(
            [
                action.status,
                action.destination,
            ]
        )

        st.caption(
            f"Owner: {action.owner} · Due: {action.due_date} · "
            f"Created: {action.created_at}"
        )

        render_divider()


def render_learning_evidence(pattern: Pattern) -> None:
    st.markdown("#### Linked learning")

    if not pattern.source_reflection_ids:
        st.caption(
            "No retained learning has contributed to this pattern yet. "
            "Completed work can strengthen the evidence over time."
        )
        return

    for reflection_id in pattern.source_reflection_ids:
        reflection = get_reflection(reflection_id)

        if not reflection:
            st.caption(
                f"{reflection_id} · Learning record is not available in this session."
            )
            continue

        st.markdown(f"**{reflection.id} · Linked learning record**")
        st.caption(f"Recorded: {reflection.recorded_at}")

        st.markdown("**Observed outcome**")
        st.write(reflection.outcome)

        st.markdown("**Learning retained**")
        st.write(reflection.learning)

        render_divider()


def render_pattern_review(pattern: Pattern) -> None:
    if pattern.status == "Dismissed":
        st.caption(
            "This pattern was dismissed for now. Its evidence remains visible "
            "so a future reviewer can reconsider it if more support appears."
        )
        return

    if pattern.status == "Confirmed":
        st.success(
            "Confirmed organizational memory. This pattern has been reviewed "
            "and is ready to inform future decisions."
        )

        if pattern.reviewed_at:
            st.caption(f"Confirmed by {pattern.reviewed_by} · {pattern.reviewed_at}")

        if pattern.review_note:
            st.markdown("**Review note**")
            st.write(pattern.review_note)

        return

    st.markdown("#### Review this emerging pattern")

    st.caption(
        "The system surfaces related evidence. A person decides whether this "
        "should become trusted organizational memory."
    )

    with st.form(f"pattern_review_form_{pattern.id}"):
        decision = st.selectbox(
            "Review decision",
            [
                "Confirm pattern",
                "Keep watching",
                "Dismiss for now",
            ],
            help=(
                "Confirm pattern: make it trusted organizational memory. "
                "Keep watching: preserve it as a hypothesis. "
                "Dismiss for now: retain the evidence without presenting it "
                "as an active pattern."
            ),
        )

        reviewer = st.text_input(
            "Reviewed by",
            value=pattern.reviewed_by,
            placeholder="Name the accountable reviewer",
        )

        review_note = st.text_area(
            "Review note",
            value=pattern.review_note,
            placeholder=(
                "Record why this evidence was confirmed, kept under review, "
                "or dismissed for now."
            ),
        )

        submitted = st.form_submit_button("Record Pattern Review")

    if submitted:
        saved = update_pattern_review(
            pattern=pattern,
            decision=decision,
            reviewer=reviewer,
            review_note=review_note,
        )

        st.session_state.pattern_review_feedback = {
            "pattern_id": pattern.id,
            "decision": decision,
            "saved": saved,
        }

        st.rerun()


def render_pattern(pattern: Pattern) -> None:
    st.markdown(f"### {pattern.id} · {pattern.title}")

    current_confidence = get_pattern_confidence(pattern)

    render_badges(
        [
            pattern.status,
            f"{current_confidence} confidence",
            pattern.trend,
            pattern.category,
            f"{pattern.evidence_count} evidence sources",
            f"{pattern.affected_accounts} affected accounts",
        ]
    )

    st.write(pattern.description)

    detail_columns = st.columns(3)

    with detail_columns[0]:
        st.caption("Proposed destination")
        st.write(pattern.proposed_destination)

    with detail_columns[1]:
        st.caption("Proposed owner")
        st.write(pattern.proposed_owner)

    with detail_columns[2]:
        st.caption("Evidence support")
        st.write(get_source_summary(pattern))

    with st.expander("Inspect evidence before review"):
        st.caption(
            "Evidence is visible before a person confirms a pattern. This "
            "keeps organizational memory traceable and prevents the system "
            "from turning repeated mentions into automatic conclusions."
        )

        render_signal_evidence(pattern)
        render_action_evidence(pattern)
        render_learning_evidence(pattern)

    render_pattern_review(pattern)


configure_page("Pattern Library | Meeting Memory Console")
render_sidebar_identity()
initialise_state()

patterns = st.session_state.get("patterns", [])

render_page_header(
    eyebrow="Pattern Library",
    title="What keeps happening",
    description=(
        "Review emerging evidence before deciding what the organization should "
        "remember. Patterns are suggested from related signals and learning, "
        "then confirmed by a person."
    ),
)

render_notice(
    "Pattern Library is the memory check before action. The system may surface "
    "an emerging pattern, but it does not decide what is true. A person reviews "
    "the linked evidence before confirming organizational memory."
)

render_review_feedback()

st.markdown("## What is emerging")

health_columns = st.columns(3)

with health_columns[0]:
    render_card(
        "Evidence before conclusions",
        "Each emerging pattern shows the signals, actions, and learning that "
        "support it. Repetition alone does not make something organizational "
        "truth.",
    )

with health_columns[1]:
    render_card(
        "Human review remains essential",
        "A reviewer can confirm a pattern, keep it under observation, or "
        "dismiss it for now. The evidence remains traceable in every case.",
    )

with health_columns[2]:
    render_card(
        "Learning makes memory stronger",
        "As completed actions produce retained learning, related patterns can "
        "gain evidence and become more useful for future decisions.",
    )

render_divider()

st.markdown("## Find the right pattern")

filter_columns = st.columns(4)

with filter_columns[0]:
    selected_category = st.selectbox(
        "Category",
        ["All"] + sorted({pattern.category for pattern in patterns}),
    )

with filter_columns[1]:
    selected_trend = st.selectbox(
        "Trend",
        ["All"] + sorted({pattern.trend for pattern in patterns}),
    )

with filter_columns[2]:
    selected_status = st.selectbox(
        "Status",
        ["All"] + sorted({pattern.status for pattern in patterns}),
    )

with filter_columns[3]:
    search_text = st.text_input(
        "Search",
        placeholder="Search themes, evidence, owners, or destinations",
    )

filtered_patterns = [
    pattern
    for pattern in patterns
    if (selected_category == "All" or pattern.category == selected_category)
    and (selected_trend == "All" or pattern.trend == selected_trend)
    and (selected_status == "All" or pattern.status == selected_status)
    and matches_search(pattern, search_text)
]

render_divider()

metric_columns = st.columns(4)

with metric_columns[0]:
    render_metric("Patterns in view", len(filtered_patterns))

with metric_columns[1]:
    render_metric(
        "Emerging",
        sum(pattern.status == "Emerging" for pattern in filtered_patterns),
    )

with metric_columns[2]:
    render_metric(
        "Confirmed",
        sum(pattern.status == "Confirmed" for pattern in filtered_patterns),
    )

with metric_columns[3]:
    render_metric(
        "Evidence linked",
        sum(pattern.evidence_count for pattern in filtered_patterns),
    )

render_divider()

st.markdown(f"## {len(filtered_patterns)} patterns in view")

if not patterns:
    render_empty_state(
        title="No emerging patterns yet",
        description=(
            "Emerging patterns will appear when related signals and retained "
            "learning provide enough evidence for human review."
        ),
        symbol="·",
    )
elif not filtered_patterns:
    render_empty_state(
        title="No patterns match these filters",
        description=(
            "Adjust the current filters or search terms to review a different "
            "set of emerging or confirmed patterns."
        ),
        symbol="⌕",
    )
else:
    for pattern in filtered_patterns:
        render_pattern(pattern)
        render_divider()

st.markdown("## The decision layer")

render_card(
    "From evidence to accountable action",
    "Pattern Library does not make the decision. It gives the person making "
    "the decision enough context to avoid duplicated work, false urgency, or "
    "an unsupported conclusion. Action Queue is where ownership and the next "
    "move are confirmed.",
)
