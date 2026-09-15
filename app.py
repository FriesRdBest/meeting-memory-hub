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
    render_metric,
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
        except (OSError, ValueError):
            st.session_state.patterns = []


def save_patterns() -> bool:
    try:
        get_pattern_service().save_patterns(st.session_state.patterns)
        return True
    except OSError:
        return False


def add_pattern(
    title: str,
    description: str,
    examples: str,
    implications: str,
    status: str,
) -> Pattern:
    pattern_id = f"PAT-{len(st.session_state.patterns) + 1:03d}"

    pattern = Pattern(
        id=pattern_id,
        title=title,
        description=description,
        examples=examples,
        implications=implications,
        status=status,
        created_at=datetime.now().strftime("%b %d, %Y at %I:%M %p"),
    )

    st.session_state.patterns.append(pattern)
    return pattern


def render_pattern_form() -> None:
    st.markdown("### Record a pattern")

    with st.form("pattern_form"):
        title = st.text_input(
            "Pattern title",
            placeholder="For example, Decisions stall without a named owner",
        )

        description = st.text_area(
            "What keeps happening",
            placeholder=(
                "Describe the recurring situation in plain language. "
                "Focus on what you observe, not why it happens."
            ),
            height=70,
        )

        examples = st.text_area(
            "Evidence from meetings",
            placeholder=(
                "List 2–4 concrete examples from reviewed meetings. "
                "For example: 'SIG-003, SIG-007, SIG-012 all show this.'"
            ),
            height=70,
        )

        implications = st.text_area(
            "Why this matters",
            placeholder=(
                "Explain the organizational impact if this pattern continues. "
                "For example: 'Work queues grow, owners stay unclear, and "
                "learning never compounds.'"
            ),
            height=70,
        )

        status = st.selectbox(
            "Status",
            ["Emerging", "Confirmed", "Addressed"],
            help=(
                "Emerging: early signs. "
                "Confirmed: repeated across meetings. "
                "Addressed: action has been taken and learning recorded."
            ),
        )

        submitted = st.form_submit_button("Save pattern")

        # Force button text to bold white for contrast on dark theme
        st.markdown(
            "<style>"
            "div[data-testid='stFormSubmitButton'] button {"
            "color: #FFFFFF !important;"
            "font-weight: 700 !important;"
            "}"
            "</style>",
            unsafe_allow_html=True,
        )

    if submitted:
        if not title or not description:
            st.warning("Title and description are required.")
        else:
            pattern = add_pattern(
                title=title,
                description=description,
                examples=examples,
                implications=implications,
                status=status,
            )

            if save_patterns():
                st.success(
                    f"{pattern.id} recorded. Pattern Library now includes this "
                    "signal for future review."
                )
            else:
                st.warning(
                    f"{pattern.id} was added for this session, but the host "
                    "could not save it permanently."
                )

            st.rerun()


def render_pattern_list() -> None:
    st.markdown("### Existing patterns")

    if not st.session_state.patterns:
        st.caption(
            "No patterns have been recorded yet. Use the form above to capture "
            "the first organizational pattern."
        )
        return

    for pattern in st.session_state.patterns:
        st.markdown(f"**{pattern.id} · {pattern.title}**")
        render_badges([pattern.status])
        st.write(pattern.description)

        if pattern.examples:
            st.caption(f"Evidence: {pattern.examples}")

        if pattern.implications:
            st.caption(f"Implications: {pattern.implications}")

        st.caption(f"Created {pattern.created_at}")

        render_divider()


configure_page("Pattern Library | Meeting Memory Console")
render_sidebar_identity()
initialise_state()

render_page_header(
    eyebrow="Pattern Library",
    title="What keeps happening",
    description=(
        "Patterns turn repeated signals into organizational knowledge. They "
        "help you see what to fix at the system level, not just in single "
        "meetings."
    ),
)

st.info(
    "Demo journey: After using Action Queue and Learning Loop, return here to "
    "record a pattern such as 'Decisions stall without a named owner'."
)

metric_columns = st.columns(3)

with metric_columns[0]:
    render_metric("Patterns recorded", len(st.session_state.patterns))

with metric_columns[1]:
    render_metric(
        "Confirmed",
        sum(p.status == "Confirmed" for p in st.session_state.patterns),
    )

with metric_columns[2]:
    render_metric(
        "Addressed",
        sum(p.status == "Addressed" for p in st.session_state.patterns),
    )

render_divider()

render_pattern_form()
render_divider()
render_pattern_list()

render_divider()

# ──────────────────────────────────────────────────────────────────────────────
# Journey band (full-width, near bottom, above "Start with one complete journey")
# ──────────────────────────────────────────────────────────────────────────────

st.markdown(
    """
    <style>
    .mmc-journey-band {
        width: 100%;
        max-width: 980px;
        margin: 2.5rem auto 1.5rem auto;
        background:
            linear-gradient(
                145deg,
                rgba(28, 28, 35, 0.96),
                rgba(18, 18, 23, 0.92)
            );
        border: 1px solid rgba(247, 247, 250, 0.12);
        border-radius: 1rem;
        padding: 2rem 1.5rem;
        position: relative;
        overflow: hidden;
    }

    .mmc-journey-title {
        color: #B7B7C6;
        font-size: 0.85rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin-bottom: 1.4rem;
        text-align: center;
    }

    .mmc-journey-track {
        position: relative;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.5rem 0;
    }

    .mmc-journey-line {
        position: absolute;
        left: 0;
        right: 0;
        top: 50%;
        height: 2px;
        background: linear-gradient(
            90deg,
            rgba(47, 53, 255, 0.15) 0%,
            rgba(47, 53, 255, 0.9) 45%,
            rgba(47, 53, 255, 0.9) 55%,
            rgba(47, 53, 255, 0.15) 100%
        );
        transform: translateY(-50%);
        z-index: 0;
        filter: drop-shadow(0 0 6px rgba(47, 53, 255, 0.7));
    }

    .mmc-journey-step {
        position: relative;
        z-index: 1;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.5rem;
    }

    .mmc-journey-pill {
        display: flex;
        align-items: center;
        gap: 0.45rem;
        padding: 0.45rem 0.7rem;
        border-radius: 999px;
        background: rgba(47, 53, 255, 0.12);
        border: 1px solid rgba(47, 53, 255, 0.35);
        color: #E9E9FF;
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 0.02em;
        box-shadow: 0 6px 18px rgba(0, 0, 0, 0.25);
        transition: transform 160ms ease, box-shadow 160ms ease;
    }

    .mmc-journey-pill:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 26px rgba(0, 0, 0, 0.32);
    }

    .mmc-journey-icon {
        width: 1.1rem;
        height: 1.1rem;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        border-radius: 50%;
        background: rgba(47, 53, 255, 0.25);
        color: #FFFFFF;
        font-size: 0.65rem;
        font-weight: 800;
    }

    .mmc-journey-label {
        color: #B7B7C6;
        font-size: 0.75rem;
        font-weight: 600;
        text-align: center;
        max-width: 6rem;
    }

    @media (max-width: 640px) {
        .mmc-journey-band {
            padding: 1.25rem 0.75rem;
        }

        .mmc-journey-pill {
            padding: 0.35rem 0.55rem;
            font-size: 0.7rem;
        }

        .mmc-journey-label {
            font-size: 0.65rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="mmc-journey-band">
        <div class="mmc-journey-title">Your intelligence workflow</div>
        <div class="mmc-journey-track">
            <div class="mmc-journey-line"></div>

            <div class="mmc-journey-step">
                <div class="mmc-journey-pill">
                    <span class="mmc-journey-icon">S</span>
                    <span>Signal</span>
                </div>
                <div class="mmc-journey-label">What deserves attention</div>
            </div>

            <div class="mmc-journey-step">
                <div class="mmc-journey-pill">
                    <span class="mmc-journey-icon">P</span>
                    <span>Pattern</span>
                </div>
                <div class="mmc-journey-label">What keeps happening</div>
            </div>

            <div class="mmc-journey-step">
                <div class="mmc-journey-pill">
                    <span class="mmc-journey-icon">A</span>
                    <span>Action</span>
                </div>
                <div class="mmc-journey-label">Who owns the next move</div>
            </div>

            <div class="mmc-journey-step">
                <div class="mmc-journey-pill">
                    <span class="mmc-journey-icon">L</span>
                    <span>Learning</span>
                </div>
                <div class="mmc-journey-label">What we carry forward</div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

render_divider()

st.markdown("## Start with one complete journey")

render_card(
    "From signal to learning",
    "Pick one signal and carry it through Pattern Library, Action Queue, and "
    "Learning Loop. That complete loop is how your organization builds memory "
    "that compounds over time.",
)
