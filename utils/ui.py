from __future__ import annotations

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
                --mmc-black: #0B0B0D;
                --mmc-surface: #15151A;
                --mmc-surface-raised: #1D1D24;
                --mmc-border: rgba(247, 247, 250, 0.12);
                --mmc-text: #F7F7FA;
                --mmc-muted: #B7B7C6;
                --mmc-success: #61D095;
                --mmc-warning: #F5BE62;
                --mmc-danger: #F17B7B;
            }

            .stApp {
                background:
                    radial-gradient(
                        circle at 88% 4%,
                        rgba(47, 53, 255, 0.18),
                        transparent 26%
                    ),
                    radial-gradient(
                        circle at 8% 98%,
                        rgba(47, 53, 255, 0.10),
                        transparent 24%
                    ),
                    var(--mmc-black);
                color: var(--mmc-text);
            }

            [data-testid="stHeader"] {
                background: transparent;
            }

            

            [data-testid="stSidebar"] {
                background: rgba(15, 15, 19, 0.95);
                border-right: 1px solid var(--mmc-border);
            }

            [data-testid="stSidebar"] * {
                color: var(--mmc-text);
            }

            [data-testid="stSidebarNav"] {
                padding-top: 2rem;
            }

            [data-testid="stSidebarNav"] a {
                border-radius: 0.65rem;
                margin: 0.15rem 0.6rem;
                padding: 0.5rem 0.75rem;
            }

            [data-testid="stSidebarNav"] a:hover {
                background: rgba(47, 53, 255, 0.18);
            }

            [data-testid="stSidebarNav"] a[aria-current="page"] {
                background: rgba(47, 53, 255, 0.30);
                color: var(--mmc-text);
                font-weight: 700;
            }

            .block-container {
    max-width: 1440px;
    padding: 3rem 2.5rem 4rem;
}

@media (max-width: 900px) {
    .block-container {
        padding: 2.25rem 1.5rem 3rem;
    }

    .mmc-lede {
        font-size: 1.02rem;
    }

    .mmc-card {
        padding: 1.1rem;
    }

    .mmc-metric {
        min-height: 7.5rem;
        padding: 1rem;
    }

    .mmc-metric-value {
        font-size: 2rem;
    }
}

@media (max-width: 640px) {
    .block-container {
        padding: 1.75rem 1rem 2.5rem;
    }

    h1 {
        font-size: 2.35rem;
    }

    h2 {
        font-size: 1.65rem;
    }

    .mmc-lede {
        font-size: 0.98rem;
        line-height: 1.55;
    }

    .mmc-card {
        margin-bottom: 0.85rem;
        padding: 1rem;
    }

    .mmc-metric {
        margin-bottom: 0.75rem;
        min-height: auto;
    }

    .mmc-metric-value {
        font-size: 1.85rem;
    }

    .mmc-divider {
        margin: 1.5rem 0;
    }
}

            h1,
            h2,
            h3 {
                color: var(--mmc-text);
                letter-spacing: -0.03em;
            }

            h1 {
                font-size: clamp(2.45rem, 5vw, 4.5rem);
                font-weight: 750;
                line-height: 1.02;
                margin-bottom: 0.8rem;
            }

            h2 {
                font-size: clamp(1.5rem, 2.5vw, 2.2rem);
                font-weight: 700;
                margin-top: 1.8rem;
            }

            h3 {
                font-size: 1.05rem;
                font-weight: 700;
            }

            p,
            li,
            label,
            [data-testid="stMarkdownContainer"] {
                color: var(--mmc-muted);
            }

            .mmc-eyebrow {
                color: var(--mmc-blue);
                font-size: 0.76rem;
                font-weight: 800;
                letter-spacing: 0.11em;
                margin-bottom: 0.85rem;
                text-transform: uppercase;
            }

            .mmc-lede {
                color: var(--mmc-muted);
                font-size: 1.15rem;
                line-height: 1.65;
                max-width: 760px;
            }

            .mmc-card {
                background: rgba(21, 21, 26, 0.82);
                border: 1px solid var(--mmc-border);
                border-radius: 1rem;
                box-shadow: 0 14px 40px rgba(0, 0, 0, 0.20);
                min-height: 100%;
                padding: 1.35rem;
            }

            .mmc-card-title {
                color: var(--mmc-text);
                font-size: 1.05rem;
                font-weight: 700;
                margin-bottom: 0.55rem;
            }

            .mmc-card-copy {
                color: var(--mmc-muted);
                font-size: 0.94rem;
                line-height: 1.55;
                margin: 0;
            }

            .mmc-metric {
                background: linear-gradient(
                    135deg,
                    rgba(47, 53, 255, 0.28),
                    rgba(21, 21, 26, 0.90)
                );
                border: 1px solid rgba(91, 97, 255, 0.42);
                border-radius: 1rem;
                min-height: 9rem;
                padding: 1.25rem;
            }

            .mmc-metric-label {
                color: var(--mmc-muted);
                font-size: 0.82rem;
                font-weight: 650;
                letter-spacing: 0.04em;
                text-transform: uppercase;
            }

            .mmc-metric-value {
                color: var(--mmc-text);
                font-size: 2.45rem;
                font-weight: 800;
                letter-spacing: -0.05em;
                line-height: 1.1;
                margin-top: 0.55rem;
            }

            .mmc-badge {
                background: rgba(47, 53, 255, 0.18);
                border: 1px solid rgba(91, 97, 255, 0.42);
                border-radius: 999px;
                color: var(--mmc-text);
                display: inline-block;
                font-size: 0.76rem;
                font-weight: 700;
                margin-right: 0.35rem;
                padding: 0.28rem 0.62rem;
            }

            .mmc-divider {
                border-top: 1px solid var(--mmc-border);
                margin: 2rem 0;
            }

            .mmc-notice {
                background: rgba(47, 53, 255, 0.12);
                border-left: 3px solid var(--mmc-blue);
                border-radius: 0.4rem;
                color: var(--mmc-muted);
                font-size: 0.92rem;
                line-height: 1.55;
                max-width: 100%;
                padding: 0.85rem 1rem;
            }

            div[data-testid="stButton"] > button {
                background: var(--mmc-blue);
                border: 1px solid rgba(255, 255, 255, 0.10);
                border-radius: 0.62rem;
                color: white;
                font-weight: 700;
                min-height: 2.55rem;
                transition: all 0.18s ease;
            }

            div[data-testid="stButton"] > button:hover {
                background: #4148FF;
                border-color: rgba(255, 255, 255, 0.28);
                box-shadow: 0 8px 22px rgba(47, 53, 255, 0.28);
                transform: translateY(-1px);
            }

            div[data-testid="stButton"] > button[kind="secondary"] {
                background: rgba(247, 247, 250, 0.08);
                border-color: var(--mmc-border);
                color: var(--mmc-text);
            }

            div[data-testid="stButton"] > button[kind="secondary"]:hover {
                background: rgba(247, 247, 250, 0.14);
                box-shadow: none;
            }

            [data-testid="stDataFrame"] {
                border: 1px solid var(--mmc-border);
                border-radius: 0.8rem;
                overflow: hidden;
            }

            [data-testid="stExpander"] {
                background: rgba(21, 21, 26, 0.70);
                border: 1px solid var(--mmc-border);
                border-radius: 0.75rem;
            }

            [data-testid="stAlert"] {
                border-radius: 0.75rem;
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
    st.markdown(f'<div class="mmc-eyebrow">{eyebrow}</div>', unsafe_allow_html=True)
    st.title(title)

    if description:
        st.markdown(
            f'<div class="mmc-lede">{description}</div>',
            unsafe_allow_html=True,
        )


def render_metric(label: str, value: int | str) -> None:
    st.markdown(
        f"""
        <div class="mmc-metric">
            <div class="mmc-metric-label">{label}</div>
            <div class="mmc-metric-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_card(title: str, copy: str) -> None:
    st.markdown(
        f"""
        <div class="mmc-card">
            <div class="mmc-card-title">{title}</div>
            <p class="mmc-card-copy">{copy}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_badges(labels: list[str]) -> None:
    badge_markup = "".join(
        f'<span class="mmc-badge">{label}</span>'
        for label in labels
        if label
    )
    st.markdown(badge_markup, unsafe_allow_html=True)


def render_notice(message: str) -> None:
    st.markdown(
        f'<div class="mmc-notice">{message}</div>',
        unsafe_allow_html=True,
    )


def render_divider() -> None:
    st.markdown('<div class="mmc-divider"></div>', unsafe_allow_html=True)


def render_sidebar_identity() -> None:
    with st.sidebar:
        st.markdown(
            f'<div class="mmc-eyebrow">{PROJECT_NAME}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<p class="mmc-card-copy">{PROJECT_TAGLINE}</p>',
            unsafe_allow_html=True,
        )
        st.markdown("---")
