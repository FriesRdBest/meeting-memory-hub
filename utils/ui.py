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
                --mmc-blue-pale: #E2E2FE;
                --mmc-success: #2EAD72;
                --mmc-warning: #C78312;
                --mmc-danger: #D95050;
                --mmc-radius-card: 1.05rem;
                --mmc-radius-control: 0.72rem;
            }

            html,
            body,
            [class*="css"] {
                font-family:
                    Inter,
                    ui-sans-serif,
                    system-ui,
                    -apple-system,
                    BlinkMacSystemFont,
                    "Segoe UI",
                    sans-serif;
            }

            .stApp {
                background:
                    radial-gradient(
                        circle at 92% 2%,
                        rgba(47, 53, 255, 0.18),
                        transparent 29%
                    ),
                    radial-gradient(
                        circle at 8% 96%,
                        rgba(47, 53, 255, 0.10),
                        transparent 24%
                    ),
                    #0B0B0D;
                color: #F7F7FA;
            }

            [data-testid="stHeader"] {
                background: transparent;
            }

            [data-testid="stToolbar"] {
                right: 1rem;
            }

            [data-testid="stSidebar"] {
                background: rgba(12, 12, 16, 0.98);
                border-right: 1px solid rgba(247, 247, 250, 0.10);
            }

            [data-testid="stSidebar"] * {
                color: #F7F7FA;
            }

            [data-testid="stSidebarContent"] {
                padding-top: 0.75rem;
            }

            [data-testid="stSidebarNav"] {
                padding-top: 1rem;
            }

            [data-testid="stSidebarNav"] ul {
                gap: 0.2rem;
            }

            [data-testid="stSidebarNav"] a {
                border: 1px solid transparent;
                border-radius: 0.82rem;
                margin: 0.1rem 0.6rem;
                padding: 0.66rem 0.78rem;
                transition:
                    background 160ms ease,
                    border-color 160ms ease,
                    transform 160ms ease;
            }

            [data-testid="stSidebarNav"] a:hover {
                background: rgba(47, 53, 255, 0.16);
                border-color: rgba(117, 122, 255, 0.20);
                transform: translateX(2px);
            }

            [data-testid="stSidebarNav"] a[aria-current="page"] {
                background:
                    linear-gradient(
                        90deg,
                        rgba(47, 53, 255, 0.38),
                        rgba(47, 53, 255, 0.18)
                    );
                border-color: rgba(114, 119, 255, 0.40);
                box-shadow:
                    inset 3px 0 0 #2F35FF,
                    0 8px 24px rgba(19, 25, 182, 0.18);
                color: #FFFFFF;
                font-weight: 760;
            }

            .block-container {
                max-width: 1440px;
                padding: 3.25rem 2.75rem 4.75rem;
            }

            h1,
            h2,
            h3,
            h4 {
                color: #F7F7FA !important;
                letter-spacing: -0.04em;
            }

            h1 {
                font-size: clamp(2.65rem, 4.8vw, 4.7rem);
                font-weight: 780;
                line-height: 1.01;
                margin-bottom: 0.9rem;
            }

            h2 {
                font-size: clamp(1.55rem, 2.3vw, 2.15rem);
                font-weight: 740;
                line-height: 1.15;
                margin-top: 2.45rem;
            }

            h3 {
                font-size: 1.16rem;
                font-weight: 730;
                line-height: 1.3;
            }

            h4 {
                font-size: 0.96rem;
                font-weight: 730;
            }

            p,
            li,
            label,
            [data-testid="stMarkdownContainer"] {
                color: #B7B7C6;
            }

            [data-testid="stCaptionContainer"] {
                color: #858596;
            }

            [data-testid="stMarkdownContainer"] strong {
                color: #F7F7FA;
            }

            .mmc-eyebrow {
                color: #5D63FF;
                font-size: 0.73rem;
                font-weight: 840;
                letter-spacing: 0.14em;
                margin-bottom: 0.95rem;
                text-transform: uppercase;
            }

            .mmc-lede {
                color: #C5C5D3;
                font-size: clamp(1.05rem, 1.5vw, 1.2rem);
                line-height: 1.68;
                max-width: 810px;
            }

            .mmc-card {
                background:
                    linear-gradient(
                        145deg,
                        rgba(28, 28, 35, 0.96),
                        rgba(18, 18, 23, 0.92)
                    );
                border: 1px solid rgba(247, 247, 250, 0.12);
                border-radius: var(--mmc-radius-card);
                box-shadow:
                    0 18px 46px rgba(0, 0, 0, 0.20),
                    inset 0 1px 0 rgba(255, 255, 255, 0.025);
                min-height: 100%;
                padding: 1.42rem;
            }

            .mmc-card-title {
                color: #F7F7FA;
                font-size: 1.03rem;
                font-weight: 760;
                letter-spacing: -0.022em;
                margin-bottom: 0.55rem;
            }

            .mmc-card-copy {
                color: #B7B7C6;
                font-size: 0.95rem;
                line-height: 1.64;
                margin: 0;
            }

            .mmc-metric {
                background:
                    linear-gradient(
                        135deg,
                        rgba(47, 53, 255, 0.34),
                        rgba(25, 25, 34, 0.96)
                    );
                border: 1px solid rgba(111, 117, 255, 0.48);
                border-radius: var(--mmc-radius-card);
                box-shadow:
                    0 18px 46px rgba(0, 0, 0, 0.22),
                    inset 0 1px 0 rgba(255, 255, 255, 0.06);
                min-height: 9.2rem;
                overflow: hidden;
                padding: 1.32rem;
                position: relative;
            }

            .mmc-metric::after {
                background:
                    radial-gradient(
                        circle,
                        rgba(255, 255, 255, 0.14),
                        transparent 68%
                    );
                border-radius: 50%;
                content: "";
                height: 12rem;
                position: absolute;
                right: -4.5rem;
                top: -6.5rem;
                width: 12rem;
            }

            .mmc-metric-label {
                color: #B7B7C6;
                font-size: 0.74rem;
                font-weight: 760;
                letter-spacing: 0.08em;
                position: relative;
                text-transform: uppercase;
                z-index: 1;
            }

            .mmc-metric-value {
                color: #FFFFFF;
                font-size: 2.6rem;
                font-weight: 820;
                letter-spacing: -0.065em;
                line-height: 1.05;
                margin-top: 0.66rem;
                position: relative;
                z-index: 1;
            }

            .mmc-badge {
                background: rgba(47, 53, 255, 0.16);
                border: 1px solid rgba(105, 110, 255, 0.42);
                border-radius: 999px;
                color: #E9E9FF;
                display: inline-block;
                font-size: 0.73rem;
                font-weight: 720;
                letter-spacing: -0.01em;
                margin: 0 0.34rem 0.46rem 0;
                padding: 0.3rem 0.65rem;
            }

            .mmc-badge--success {
                background: rgba(46, 173, 114, 0.14);
                border-color: rgba(97, 208, 149, 0.52);
                color: #7AE4A9;
            }

            .mmc-badge--warning {
                background: rgba(199, 131, 18, 0.15);
                border-color: rgba(245, 190, 98, 0.54);
                color: #FFD183;
            }

            .mmc-badge--danger {
                background: rgba(217, 80, 80, 0.14);
                border-color: rgba(241, 123, 123, 0.54);
                color: #FFAAAA;
            }

            .mmc-divider {
                border-top: 1px solid rgba(247, 247, 250, 0.11);
                margin: 2.4rem 0;
            }

            .mmc-notice {
                background:
                    linear-gradient(
                        90deg,
                        rgba(47, 53, 255, 0.16),
                        rgba(47, 53, 255, 0.08)
                    );
                border: 1px solid rgba(101, 106, 255, 0.26);
                border-left: 3px solid #2F35FF;
                border-radius: 0.76rem;
                color: #C5C5D3;
                font-size: 0.94rem;
                line-height: 1.58;
                max-width: 100%;
                padding: 0.96rem 1.04rem;
            }

            .mmc-sidebar-identity {
                border-bottom: 1px solid rgba(247, 247, 250, 0.11);
                margin: 0.3rem 0.75rem 1.1rem;
                padding: 0.75rem 0 1.3rem;
            }

            .mmc-sidebar-tagline {
                color: #A4A4B5;
                font-size: 0.88rem;
                line-height: 1.5;
                margin: 0;
            }

            div[data-testid="stSelectbox"] > div > div,
            div[data-testid="stTextInput"] input,
            div[data-testid="stTextArea"] textarea {
                background: rgba(27, 27, 34, 0.96) !important;
                border-color: rgba(247, 247, 250, 0.13) !important;
                border-radius: var(--mmc-radius-control) !important;
                color: #F7F7FA !important;
            }

            div[data-testid="stTextInput"] input::placeholder,
            div[data-testid="stTextArea"] textarea::placeholder {
                color: #858596;
            }

            div[data-baseweb="select"] > div,
            div[data-baseweb="select"] * {
                color: #F7F7FA !important;
            }

            div[data-baseweb="popover"],
            [data-baseweb="menu"] {
                background: #1D1D24 !important;
            }

            [data-baseweb="menu"] li {
                color: #F7F7FA !important;
            }

            [data-baseweb="menu"] li:hover {
                background: rgba(47, 53, 255, 0.16) !important;
            }

            div[data-testid="stButton"] > button,
            div[data-testid="stFormSubmitButton"] > button {
                background: #2F35FF;
                border: 1px solid rgba(255, 255, 255, 0.16);
                border-radius: 0.72rem;
                box-shadow: 0 12px 28px rgba(47, 53, 255, 0.26);
                color: #FFFFFF !important;
                font-weight: 760;
                min-height: 2.68rem;
                transition:
                    background 160ms ease,
                    border-color 160ms ease,
                    box-shadow 160ms ease,
                    transform 160ms ease;
            }

            div[data-testid="stButton"] > button:hover,
            div[data-testid="stFormSubmitButton"] > button:hover {
                background: #4148FF;
                border-color: rgba(255, 255, 255, 0.32);
                box-shadow: 0 15px 32px rgba(47, 53, 255, 0.34);
                transform: translateY(-1px);
            }

            div[data-testid="stButton"] > button[kind="secondary"] {
                background: rgba(247, 247, 250, 0.07);
                border-color: rgba(247, 247, 250, 0.13);
                box-shadow: none;
                color: #F7F7FA !important;
            }

            div[data-testid="stButton"] > button[kind="secondary"]:hover {
                background: rgba(47, 53, 255, 0.14);
                border-color: rgba(111, 117, 255, 0.40);
                box-shadow: none;
            }

            [data-testid="stExpander"] {
                background: rgba(20, 20, 26, 0.84);
                border: 1px solid rgba(247, 247, 250, 0.13);
                border-radius: 0.84rem;
                overflow: hidden;
            }

            [data-testid="stExpander"] summary {
                color: #F7F7FA;
                font-weight: 670;
            }

            [data-testid="stAlert"] {
                border: 1px solid rgba(247, 247, 250, 0.13);
                border-radius: 0.78rem;
            }

            [data-testid="stAlert"] * {
                color: #F7F7FA;
            }

            blockquote {
                background: rgba(47, 53, 255, 0.10);
                border-left: 3px solid #2F35FF;
                border-radius: 0 0.62rem 0.62rem 0;
                color: #C5C5D3;
                line-height: 1.65;
                margin: 0.8rem 0 1rem;
                padding: 0.82rem 1rem;
            }

            button:focus-visible,
            input:focus-visible,
            textarea:focus-visible,
            [data-baseweb="select"] > div:focus-within {
                box-shadow: 0 0 0 3px rgba(100, 105, 255, 0.44) !important;
                outline: none !important;
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
