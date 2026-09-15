from __future__ import annotations

from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

from repositories.signal_repository import SignalRepository
from services.signal_service import SignalService
from utils.ui import (
    configure_page,
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


def get_signal_value(signal: object, field_name: str, default: object = None) -> object:
    if isinstance(signal, dict):
        return signal.get(field_name, default)

    return getattr(signal, field_name, default)


def count_by_status(signals: list[object], status: str) -> int:
    return sum(
        get_signal_value(signal, "status") == status
        for signal in signals
    )


def count_with_value(signals: list[object], field_name: str) -> int:
    return sum(
        bool(get_signal_value(signal, field_name))
        for signal in signals
    )


def render_journey_band() -> None:
    journey_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        :root {
            --mmc-blue: #2f35ff;
            --mmc-muted: #b7b7c6;
            --mmc-border: rgba(247, 247, 250, 0.12);
            --mmc-surface-start: rgba(28, 28, 35, 0.96);
            --mmc-surface-end: rgba(18, 18, 23, 0.92);
        }

        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            padding: 0;
            background: transparent;
            font-family:
                Inter,
                ui-sans-serif,
                system-ui,
                -apple-system,
                BlinkMacSystemFont,
                "Segoe UI",
                sans-serif;
        }

        .mmc-journey-band {
            width: 100%;
            min-height: 220px;
            padding: 2rem 1.5rem;
            overflow: hidden;
            border: 1px solid var(--mmc-border);
            border-radius: 1rem;
            background: linear-gradient(
                145deg,
                var(--mmc-surface-start),
                var(--mmc-surface-end)
            );
        }

        .mmc-journey-title {
            margin: 0 0 1.5rem;
            color: var(--mmc-muted);
            font-size: 0.78rem;
            font-weight: 800;
            letter-spacing: 0.13em;
            text-align: center;
            text-transform: uppercase;
        }

        .mmc-journey-track {
            position: relative;
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            gap: 0.75rem;
            width: 100%;
            padding: 0.6rem 0 0;
        }

        .mmc-journey-line {
            position: absolute;
            top: 1.95rem;
            right: 7%;
            left: 7%;
            z-index: 0;
            height: 2px;
            border-radius: 999px;
            background: linear-gradient(
                90deg,
                rgba(47, 53, 255, 0.15) 0%,
                rgba(47, 53, 255, 0.95) 20%,
                rgba(47, 53, 255, 0.95) 80%,
                rgba(47, 53, 255, 0.15) 100%
            );
            box-shadow: 0 0 10px rgba(47, 53, 255, 0.78);
        }

        .mmc-journey-step {
            position: relative;
            z-index: 1;
            display: flex;
            flex: 1;
            flex-direction: column;
            align-items: center;
            min-width: 0;
            gap: 0.6rem;
        }

        .mmc-journey-pill {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 0.45rem;
            min-height: 2.4rem;
            padding: 0.48rem 0.8rem;
            border: 1px solid rgba(47, 53, 255, 0.42);
            border-radius: 999px;
            background: rgba(21, 22, 42, 0.98);
            color: #f4f4ff;
            font-size: 0.82rem;
            font-weight: 750;
            line-height: 1;
            white-space: nowrap;
            box-shadow:
                0 0 0 4px rgba(18, 18, 23, 0.98),
                0 8px 18px rgba(0, 0, 0, 0.28);
        }

        .mmc-journey-icon {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 1.2rem;
            height: 1.2rem;
            border-radius: 50%;
            background: rgba(47, 53, 255, 0.38);
            color: #ffffff;
            font-size: 0.67rem;
            font-weight: 850;
        }

        .mmc-journey-label {
            max-width: 8.5rem;
            color: var(--mmc-muted);
            font-size: 0.73rem;
            font-weight: 600;
            line-height: 1.35;
            text-align: center;
        }

        @media (max-width: 640px) {
            .mmc-journey-band {
                min-height: 0;
                padding: 1.25rem 0.85rem;
            }

            .mmc-journey-track {
                flex-direction: column;
                align-items: stretch;
                gap: 0.9rem;
                padding: 0;
            }

            .mmc-journey-line {
                top: 1rem;
                bottom: 1rem;
                left: 1.2rem;
                right: auto;
                width: 2px;
                height: auto;
                background: linear-gradient(
                    180deg,
                    rgba(47, 53, 255, 0.15),
                    rgba(47, 53, 255, 0.95),
                    rgba(47, 53, 255, 0.15)
                );
            }

            .mmc-journey-step {
                flex-direction: row;
                align-items: center;
                justify-content: flex-start;
                gap: 0.75rem;
            }

            .mmc-journey-pill {
                min-width: 7.8rem;
            }

            .mmc-journey-label {
                max-width: none;
                text-align: left;
            }
        }
    </style>
</head>
<body>
    <section class="mmc-journey-band">
        <div class="mmc-journey-title">Your intelligence workflow</div>

        <div class="mmc-journey-track">
            <div class="mmc-journey-line"></div>

            <div class="mmc-journey-step">
                <div class="mmc-journey-pill">
                    <span class="mmc-journey-icon">S</span>
                    <span>Signal</span>
                </div>
                <div class="mmc-journey-label">
                    What deserves attention
                </div>
            </div>

            <div class="mmc-journey-step">
                <div class="mmc-journey-pill">
                    <span class="mmc-journey-icon">P</span>
                    <span>Pattern</span>
                </div>
                <div class="mmc-journey-label">
                    What keeps happening
                </div>
            </div>

            <div class="mmc-journey-step">
                <div class="mmc-journey-pill">
                    <span class="mmc-journey-icon">A</span>
                    <span>Action</span>
                </div>
                <div class="mmc-journey-label">
                    Who owns the next move
                </div>
            </div>

            <div class="mmc-journey-step">
                <div class="mmc-journey-pill">
                    <span class="mmc-journey-icon">L</span>
                    <span>Learning</span>
                </div>
                <div class="mmc-journey-label">
                    What we carry forward
                </div>
            </div>
        </div>
    </section>
</body>
</html>
'''

    components.html(journey_html, height=240, scrolling=False)


configure_page("Overview | Meeting Memory Console")
render_sidebar_identity()
initialise_state()

signals = st.session_state.get("signals", [])

render_page_header(
    eyebrow="Meeting Memory Console",
    title="Your organization's intelligence layer",
    description=(
        "Meeting Memory Console turns meeting signals into patterns, actions, "
        "and learning. It helps you see what keeps happening, who owns the "
        "next move, and what the organization should remember."
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
        count_by_status(signals, "Needs review"),
    )

with metric_columns[2]:
    render_metric(
        "Patterns identified",
        count_with_value(signals, "pattern_hint"),
    )

with metric_columns[3]:
    render_metric(
        "Actions created",
        count_with_value(signals, "action_created"),
    )

render_divider()

st.markdown("## The organization at a glance")

st.write(
    "This overview shows the current state of your organizational memory. "
    "Use the left sidebar to navigate between Signal Triage, Pattern Library, "
    "Action Queue, and Learning Loop."
)

render_card(
    "How the system works",
    "Signals are captured from meetings. Patterns reveal what keeps "
    "happening. Actions assign ownership and next steps. Learning captures "
    "what the organization should remember. Together, they form a complete "
    "intelligence workflow.",
)

render_divider()

render_journey_band()

render_divider()

st.markdown("## Start with one complete journey")

render_card(
    "From signal to learning",
    "Pick one signal and carry it through Pattern Library, Action Queue, and "
    "Learning Loop. That complete loop is how your organization builds memory "
    "that compounds over time.",
)
