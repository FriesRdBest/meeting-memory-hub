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


def get_value(signal: object, field_name: str, default: object = None) -> object:
    """Read a value from either a dict-based or object-based signal."""
    if isinstance(signal, dict):
        return signal.get(field_name, default)

    return getattr(signal, field_name, default)


def count_signals_with_status(signals: list[object], status: str) -> int:
    return sum(get_value(signal, "status") == status for signal in signals)


def count_signals_with_value(signals: list[object], field_name: str) -> int:
    return sum(bool(get_value(signal, field_name)) for signal in signals)


def render_journey_band() -> None:
    journey_html = """
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
                min-height: 215px;
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
                transition:
                    transform 160ms ease,
                    border-color 160ms ease,
                    box-shadow 160ms ease;
            }

            .mmc-journey-pill:hover {
                border-color: rgba(47, 53, 255, 0.9);
                box-shadow:
                    0 0 0 4px rgba(18, 18, 23, 0.98),
                    0 0 18px rgba(47, 53, 255, 0.5),
                    0 10px 24px rgba(0, 0, 0, 0.34);
                transform: translateY(-2px);
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
