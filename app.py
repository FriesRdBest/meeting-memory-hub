from __future__ import annotations

from datetime import datetime
from pathlib import Path

import streamlit as st

from repositories.signal_repository import SignalRepository
from services.signal_service import SignalService
from utils.ui import (
    configure_page,
    render_badges,
    render_card,
    render_divider,
    render_metric,
    render_page_header,
    render_sidebar_identity,
)

SIGNAL_FILE_PATH = Path("data/signals.json")


def get_signal_service() -> SignalService:
    return SignalService(SignalRepository(SIGNAL_FILE_PATH))


def initialise_state() -> None:
    if "signals" not in st.session_state:
        try:
            st.session_state.signals = get_signal_service().list_signals()
        except (OSError, ValueError):
            st.session_state.signals = []


configure_page("Overview | Meeting Memory Console")
render_sidebar_identity()
initialise_state()

signals = st.session_state.get("signals", [])

render_page_header(
    eyebrow="Meeting Memory Console",
    title="Your organization's intelligence layer",
    description=(
        "Meeting Memory Console turns meeting signals into patterns, "
        "actions, and learning. It helps you see what keeps happening, who "
        "owns the next move, and what the organization should remember."
    ),
)

st.info(
    "Demo journey: Start with **Signal Triage**, then explore **Pattern "
    "Library**, **Action Queue**, and **Learning Loop** to see the full "
    "workflow."
)

metric_columns = st.columns(4)

with metric_columns[0]:
    render_metric("Signals in view", len(signals))

with metric_columns[1]:
    render_metric(
        "Need review",
        sum(
            1
            for s in signals
            if isinstance(s, dict) and s.get("status") == "Needs review"
        ),
    )

with metric_columns[2]:
    render_metric(
        "Patterns identified",
        sum(
            1
            for s in signals
            if isinstance(s, dict) and s.get("pattern_hint")
        ),
    )

with metric_columns[3]:
    render_metric(
        "Actions created",
        sum(
            1
            for s in signals
            if isinstance(s, dict) and s.get("action_created")
        ),
    )

render_divider()

st.markdown("## The organization at a glance")

st.markdown(
    "This overview shows the current state of your organizational memory. "
    "Use the left sidebar to navigate between Signal Triage, Pattern Library, "
    "Action Queue, and Learning Loop."
)

render_card(
    "How the system works",
    "Signals are captured from meetings. Patterns reveal what keeps "
    "happening. Actions assign ownership and next steps. Learning captures "
    "what the organization should remember. Together, they form a complete "
    "intelligence workflow."
)

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
