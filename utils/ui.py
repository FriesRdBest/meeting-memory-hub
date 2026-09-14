from __future__ import annotations

from html import escape

import streamlit as st

from config import APP_ICON, PROJECT_NAME, PROJECT_TAGLINE


def configure_page(page_title: str | None = None) -> None:
    resolved_title = page_title or PROJECT_NAME

    st.set_page_config(
        page_title=resolved_title,
        page_icon=APP_ICON,
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            "Get help": None,
            "Report a bug": None,
            "About": (
                "Meeting Memory Console is a working prototype for turning "
                "meeting intelligence into trusted memory, accountable action, "
                "and visible learning."
            ),
        },
    )

    inject_global_styles()


def inject_global_styles() -> None:
    st.markdown(
        """
        <style>
            :root {
                --mmc-blue: #2F35FF;
                --mmc-blue-deep: #1D239D;
                --mmc-success: #61D095;
                --mmc-warning: #F5BE62;
                --mmc-danger: #F17B7B;
                --mmc-radius: 1rem;
                --mmc-radius-small: 0.72rem;
            }

            .stApp {
                background:
                    radial-gradient(
                        circle at 88% 4%,
                        rgba(47, 53, 255, 0.18),
                        transparent 27%
                    ),
                    radial-gradient(
                        circle at 8% 98%,
                        rgba(47, 53, 255, 0.10),
                        transparent 25%
                    ),
                    var(--background-color);
                color: var(--text-color);
            }

            [data-testid="stHeader"] {
                background: transparent;
            }

            [data-testid="stToolbar"] {
                right: 1rem;
            }

            [data-testid="stSidebar"] {
                background: var(--secondary-background-color);
                border-right: 1px solid color-mix(
                    in srgb,
                    var(--text-color) 12%,
                    transparent
                );
            }

            [data-testid="stSidebar"] * {
                color: var(--text-color);
            }

            [data-testid="stSidebarContent"] {
                padding-top: 0.7rem;
            }

            [data-testid="stSidebarNav"] {
                padding-top: 1.15rem;
            }

            [data-testid="stSidebarNav"] ul {
                gap: 0.22rem;
            }

            [data-testid="stSidebarNav"] a {
                border: 1px solid transparent;
                border-radius: 0.8rem;
                margin: 0.08rem 0.6rem;
                padding: 0.62rem 0.75rem;
                transition:
                    background 160ms ease,
                    border-color 160ms ease,
                    transform 160ms ease;
            }

            [data-testid="stSidebarNav"] a:hover {
                background: color-mix(
                    in srgb,
                    var(--mmc-blue) 14%,
                    transparent
                );
                border-color: color-mix(
                    in srgb,
                    var(--text-color) 12%,
                    transparent
                );
                transform: translateX(2px);
            }

            [data-testid="stSidebarNav"] a[aria-current="page"] {
                background:
                    linear-gradient(
                        90deg,
                        rgba(47, 53, 255, 0.34),
                        rgba(47, 53, 255, 0.18)
                    );
                border-color: rgba(110, 115, 255, 0.38);
                box-shadow: inset 3px 0 0 var(--mmc-blue);
                color: var(--text-color);
                font-weight: 750;
            }

            .block-container {
                max-width: 1440px;
                padding: 3.25rem 2.75rem 4.5rem;
            }

            h1,
            h2,
            h3,
            h4 {
                color: var(--text-color) !important;
                letter-spacing: -0.035em;
            }

            h1 {
                font-size: clamp(2.55rem, 4.6vw, 4.6rem);
                font-weight: 760;
                line-height: 1.02;
                margin-bottom: 0.9rem;
            }

            h2 {
                font-size: clamp(1.55rem, 2.4vw, 2.15rem);
                font-weight: 730;
                line-height: 1.15;
                margin-top: 2.35rem;
            }

            h3 {
                font-size: 1.17rem;
                font-weight: 720;
                line-height: 1.25;
            }

            h4 {
                font-size: 0.95rem;
                font-weight: 720;
            }

            p,
            li,
            label,
            [data-testid="stMarkdownContainer"] {
                color: color-mix(
                    in srgb,
                    var(--text-color) 73%,
                    var(--background-color)
                );
            }

            [data-testid="stCaptionContainer"] {
                color: color-mix(
                    in srgb,
                    var(--text-color) 56%,
                    var(--background-color)
                );
            }

            [data-testid="stMarkdownContainer"] strong {
                color: var(--text-color);
            }

            .mmc-eyebrow {
                color: var(--mmc-blue);
                font-size: 0.74rem;
                font-weight: 830;
                letter-spacing: 0.13em;
                margin-bottom: 0.9rem;
                text-transform: uppercase;
            }

            .mmc-lede {
                color: color-mix(
                    in srgb,
                    var(--text-color) 73%,
                    var(--background-color)
                );
                font-size: clamp(1.05rem, 1.5vw, 1.18rem);
                line-height: 1.68;
                max-width: 800px;
            }

            .mmc-card {
                background:
                    linear-gradient(
                        145deg,
                        var(--secondary-background-color),
                        color-mix(
                            in srgb,
                            var(--secondary-background-color) 86%,
                            var(--background-color)
                        )
                    );
                border: 1px solid color-mix(
                    in srgb,
                    var(--text-color) 12%,
                    transparent
                );
                border-radius: var(--mmc-radius);
                box-shadow: 0 9px 26px rgba(0, 0, 0, 0.11);
                min-height: 100%;
                padding: 1.4rem;
            }

            .mmc-card-title {
                color: var(--text-color);
                font-size: 1.02rem;
                font-weight: 760;
                letter-spacing: -0.018em;
                margin-bottom: 0.55rem;
            }

            .mmc-card-copy {
                color: color-mix(
                    in srgb,
                    var(--text-color) 73%,
                    var(--background-color)
                );
                font-size: 0.95rem;
                line-height: 1.62;
                margin: 0;
            }

            .mmc-metric {
                background:
                    linear-gradient(
                        135deg,
                        rgba(47, 53, 255, 0.28),
                        var(--secondary-background-color)
                    );
                border: 1px solid rgba(104, 109, 255, 0.42);
                border-radius: var(--mmc-radius);
                box-shadow: 0 9px 26px rgba(0, 0, 0, 0.11);
                min-height: 9.1rem;
                overflow: hidden;
                padding: 1.3rem;
                position: relative;
            }

            .mmc-metric::after {
                background: rgba(255, 255, 255, 0.10);
                border-radius: 50%;
                content: "";
                height: 9rem;
                position: absolute;
                right: -4rem;
                top: -5rem;
                width: 9rem;
            }

            .mmc-metric-label {
                color: color-mix(
                    in srgb,
                    var(--text-color) 70%,
                    var(--background-color)
                );
                font-size: 0.75rem;
                font-weight: 750;
                letter-spacing: 0.075em;
                position: relative;
                text-transform: uppercase;
                z-index: 1;
            }

            .mmc-metric-value {
                color: var(--text-color);
                font-size: 2.55rem;
                font-weight: 810;
                letter-spacing: -0.06em;
                line-height: 1.1;
                margin-top: 0.62rem;
                position: relative;
                z-index: 1;
            }

            .mmc-badge {
                background: color-mix(
                    in srgb,
                    var(--mmc-blue) 13%,
                    transparent
                );
                border: 1px solid rgba(100, 105, 255, 0.40);
                border-radius: 999px;
                color: var(--text-color);
                display: inline-block;
                font-size: 0.73rem;
                font-weight: 720;
                letter-spacing: -0.01em;
                margin: 0 0.32rem 0.45rem 0;
                padding: 0.3rem 0.64rem;
            }

            .mmc-badge--success {
                background: color-mix(
                    in srgb,
                    var(--mmc-success) 14%,
                    transparent
                );
                border-color: color-mix(
                    in srgb,
                    var(--mmc-success) 62%,
                    transparent
                );
                color: var(--mmc-success);
            }

            .mmc-badge--warning {
                background: color-mix(
                    in srgb,
                    var(--mmc-warning) 14%,
                    transparent
                );
                border-color: color-mix(
                    in srgb,
                    var(--mmc-warning) 62%,
                    transparent
                );
                color: var(--mmc-warning);
            }

            .mmc-badge--danger {
                background: color-mix(
                    in srgb,
                    var(--mmc-danger) 14%,
                    transparent
                );
                border-color: color-mix(
                    in srgb,
                    var(--mmc-danger) 62%,
                    transparent
                );
                color: var(--mmc-danger);
            }

            .mmc-divider {
                border-top: 1px solid color-mix(
                    in srgb,
                    var(--text-color) 12%,
                    transparent
                );
                margin: 2.35rem 0;
            }

            .mmc-notice {
                background: color-mix(
                    in srgb,
                    var(--mmc-blue) 12%,
                    transparent
                );
                border: 1px solid rgba(100, 105, 255, 0.28);
                border-left: 3px solid var(--mmc-blue);
                border-radius: 0.75rem;
                color: color-mix(
                    in srgb,
                    var(--text-color) 73%,
                    var(--background-color)
                );
                font-size: 0.94rem;
                line-height: 1.58;
                max-width: 100%;
                padding: 0.95rem 1rem;
            }

            .mmc-sidebar-identity {
                border-bottom: 1px solid color-mix(
                    in srgb,
                    var(--text-color) 12%,
                    transparent
                );
                margin: 0.3rem 0.75rem 1.1rem;
                padding: 0.75rem 0 1.3rem;
            }

            .mmc-sidebar-tagline {
                color: color-mix(
                    in srgb,
                    var(--text-color) 70%,
                    var(--background-color)
                );
                font-size: 0.88rem;
                line-height: 1.5;
                margin: 0;
            }

            div[data-testid="stSelectbox"] > div > div,
            div[data-testid="stTextInput"] input,
            div[data-testid="stTextArea"] textarea {
                background: var(--secondary-background-color) !important;
                border-color: color-mix(
                    in srgb,
                    var(--text-color) 15%,
                    transparent
                ) !important;
                border-radius: var(--mmc-radius-small) !important;
                color: var(--text-color) !important;
            }

            div[data-testid="stTextInput"] input,
            div[data-testid="stTextArea"] textarea {
                caret-color: var(--mmc-blue);
            }

            div[data-testid="stTextInput"] input::placeholder,
            div[data-testid="stTextArea"] textarea::placeholder {
                color: color-mix(
                    in srgb,
                    var(--text-color) 50%,
                    var(--background-color)
                );
            }

            div[data-baseweb="select"] > div,
            div[data-baseweb="select"] * {
                color: var(--text-color) !important;
            }

            div[data-baseweb="popover"],
            [data-baseweb="menu"] {
                background: var(--secondary-background-color) !important;
            }

            [data-baseweb="menu"] li {
                color: var(--text-color) !important;
            }

            [data-baseweb="menu"] li:hover {
                background: color-mix(
                    in srgb,
                    var(--mmc-blue) 13%,
                    transparent
                ) !important;
            }

            div[data-testid="stButton"] > button,
            div[data-testid="stFormSubmitButton"] > button {
                background: var(--mmc-blue);
                border: 1px solid rgba(255, 255, 255, 0.16);
                border-radius: 0.7rem;
                box-shadow: 0 10px 26px rgba(47, 53, 255, 0.22);
                color: #FFFFFF !important;
                font-weight: 750;
                min-height: 2.65rem;
                transition:
                    background 160ms ease,
                    border-color 160ms ease,
                    box-shadow 160ms ease,
                    transform 160ms ease;
            }

            div[data-testid="stButton"] > button:hover,
            div[data-testid="stFormSubmitButton"] > button:hover {
                background: #4148FF;
                border-color: rgba(255, 255, 255, 0.30);
                box-shadow: 0 12px 30px rgba(47, 53, 255, 0.32);
                transform: translateY(-1px);
            }

            div[data-testid="stButton"] > button[kind="secondary"] {
                background: var(--secondary-background-color);
                border-color: color-mix(
                    in srgb,
                    var(--text-color) 15%,
                    transparent
                );
                box-shadow: none;
                color: var(--text-color) !important;
            }

            div[data-testid="stButton"] > button[kind="secondary"]:hover {
                background: color-mix(
                    in srgb,
                    var(--mmc-blue) 13%,
                    var(--secondary-background-color)
                );
                border-color: rgba(100, 105, 255, 0.48);
                box-shadow: none;
            }

            [data-testid="stExpander"] {
                background: var(--secondary-background-color);
                border: 1px solid color-mix(
                    in srgb,
                    var(--text-color) 12%,
                    transparent
                );
                border-radius: 0.82rem;
                overflow: hidden;
            }

            [data-testid="stExpander"] summary {
                color: var(--text-color);
                font-weight: 650;
            }

            [data-testid="stAlert"] {
                border: 1px solid color-mix(
                    in srgb,
                    var(--text-color) 12%,
                    transparent
                );
                border-radius: 0.78rem;
            }

            [data-testid="stAlert"] * {
                color: var(--text-color);
            }

            [data-testid="stDataFrame"] {
                border: 1px solid color-mix(
                    in srgb,
                    var(--text-color) 12%,
                    transparent
                );
                border-radius: 0.9rem;
                overflow: hidden;
            }

            blockquote {
                background: color-mix(
                    in srgb,
                    var(--mmc-blue) 10%,
                    transparent
                );
                border-left: 3px solid var(--mmc-blue);
                border-radius: 0 0.6rem 0.6rem 0;
                color: color-mix(
                    in srgb,
                    var(--text-color) 73%,
                    var(--background-color)
                );
                line-height: 1.65;
                margin: 0.8rem 0 1rem;
                padding: 0.8rem 1rem;
            }

            button:focus-visible,
            input:focus-visible,
            textarea:focus-visible,
            [data-baseweb="select"] > div:focus-within {
                box-shadow: 0 0 0 3px rgba(47, 53, 255, 0.34) !important;
                outline: none !important;
            }

            @media (prefers-reduced-motion: reduce) {
                *,
                *::before,
                *::after {
                    scroll-behavior: auto !important;
                    transition-duration: 0.01ms !important;
                }
            }

            @media (max-width: 900px) {
                .block-container {
                    padding: 2.5rem 1.6rem 3.5rem;
                }

                .mmc-card {
                    padding: 1.15rem;
                }

                .mmc-metric {
                    min-height: 7.8rem;
                    padding: 1.1rem;
                }

                .mmc-metric-value {
                    font-size: 2.15rem;
                }
            }

            @media (max-width: 640px) {
                .block-container {
                    padding: 1.9rem 1rem 2.75rem;
                }

                h1 {
                    font-size: 2.35rem;
                }

                h2 {
                    font-size: 1.62rem;
                }

                .mmc-lede {
                    font-size: 1rem;
                    line-height: 1.6;
                }

                .mmc-card {
                    margin-bottom: 0.85rem;
                    padding: 1rem;
                }

                .mmc-metric {
                    margin-bottom: 0.75rem;
                    min-height: auto;
                }

                .mmc-divider {
                    margin: 1.65rem 0;
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_page_header(
    eyebrow: str,
    title: str,
    description: str | None = None,
) -> None:
    safe_eyebrow = escape(eyebrow)
    st.markdown(
        f'<div class="mmc-eyebrow">{safe_eyebrow}</div>',
        unsafe_allow_html=True,
    )
    st.title(title)

    if description:
        st.markdown(
            f'<div class="mmc-lede">{escape(description)}</div>',
            unsafe_allow_html=True,
        )


def render_metric(label: str, value: int | str) -> None:
    st.markdown(
        f"""
        <div class="mmc-metric">
            <div class="mmc-metric-label">{escape(str(label))}</div>
            <div class="mmc-metric-value">{escape(str(value))}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_card(title: str, copy: str) -> None:
    st.markdown(
        f"""
        <div class="mmc-card">
            <div class="mmc-card-title">{escape(title)}</div>
            <p class="mmc-card-copy">{escape(copy)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def get_badge_class(label: str) -> str:
    normalized = label.lower()

    success_keywords = (
        "completed",
        "ready",
        "stable",
        "high confidence",
        "success",
    )
    warning_keywords = (
        "needs attention",
        "needs review",
        "increasing",
        "high impact",
        "watching",
    )
    danger_keywords = ("declined", "blocked", "risk", "error")

    if any(keyword in normalized for keyword in success_keywords):
        return "mmc-badge mmc-badge--success"

    if any(keyword in normalized for keyword in warning_keywords):
        return "mmc-badge mmc-badge--warning"

    if any(keyword in normalized for keyword in danger_keywords):
        return "mmc-badge mmc-badge--danger"

    return "mmc-badge"


def render_badges(labels: list[str]) -> None:
    badge_markup = "".join(
        (
            f'<span class="{get_badge_class(label)}">'
            f"{escape(label)}</span>"
        )
        for label in labels
        if label
    )
    st.markdown(badge_markup, unsafe_allow_html=True)


def render_notice(message: str) -> None:
    st.markdown(
        f'<div class="mmc-notice">{escape(message)}</div>',
        unsafe_allow_html=True,
    )


def render_divider() -> None:
    st.markdown('<div class="mmc-divider"></div>', unsafe_allow_html=True)


def render_sidebar_identity() -> None:
    with st.sidebar:
        st.markdown(
            f"""
            <div class="mmc-sidebar-identity">
                <div class="mmc-eyebrow">{escape(PROJECT_NAME)}</div>
                <p class="mmc-sidebar-tagline">{escape(PROJECT_TAGLINE)}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
