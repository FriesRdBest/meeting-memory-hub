from __future__ import annotations

from html import escape

import streamlit as st

from config import APP_ICON, PROJECT_NAME, PROJECT_TAGLINE


DREAM = "Dream"
REALITY = "Reality"


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

    if "appearance" not in st.session_state:
        st.session_state.appearance = DREAM

    inject_global_styles(st.session_state.appearance)


def inject_global_styles(appearance: str) -> None:
    if appearance == REALITY:
        theme_variables = """
            --mmc-blue: #2F35FF;
            --mmc-blue-deep: #1D239D;
            --mmc-blue-soft: #E2E2FE;
            --mmc-black: #F7F7FF;
            --mmc-surface: #FFFFFF;
            --mmc-surface-raised: #F0F0FF;
            --mmc-surface-soft: #E2E2FE;
            --mmc-border: #D5D5EA;
            --mmc-border-strong: #B9B9DE;
            --mmc-text: #15151A;
            --mmc-muted: #56566C;
            --mmc-subtle: #76768A;
            --mmc-success: #16834B;
            --mmc-success-soft: #E4F7EC;
            --mmc-warning: #A86200;
            --mmc-warning-soft: #FFF2DA;
            --mmc-danger: #BD3030;
            --mmc-danger-soft: #FDE9E9;
            --mmc-shadow-soft: 0 8px 24px rgba(30, 30, 75, 0.07);
            --mmc-focus: rgba(47, 53, 255, 0.34);
            --mmc-app-background:
                radial-gradient(
                    circle at 88% 3%,
                    rgba(47, 53, 255, 0.11),
                    transparent 27%
                ),
                radial-gradient(
                    circle at 7% 96%,
                    rgba(226, 226, 254, 0.95),
                    transparent 25%
                ),
                #F7F7FF;
        """
    else:
        theme_variables = """
            --mmc-blue: #2F35FF;
            --mmc-blue-deep: #1D239D;
            --mmc-blue-soft: rgba(47, 53, 255, 0.18);
            --mmc-black: #0B0B0D;
            --mmc-surface: #15151A;
            --mmc-surface-raised: #1D1D24;
            --mmc-surface-soft: rgba(47, 53, 255, 0.10);
            --mmc-border: rgba(247, 247, 250, 0.12);
            --mmc-border-strong: rgba(123, 128, 255, 0.46);
            --mmc-text: #F7F7FA;
            --mmc-muted: #B7B7C6;
            --mmc-subtle: #858596;
            --mmc-success: #61D095;
            --mmc-success-soft: rgba(97, 208, 149, 0.12);
            --mmc-warning: #F5BE62;
            --mmc-warning-soft: rgba(245, 190, 98, 0.12);
            --mmc-danger: #F17B7B;
            --mmc-danger-soft: rgba(241, 123, 123, 0.12);
            --mmc-shadow-soft: 0 9px 26px rgba(0, 0, 0, 0.16);
            --mmc-focus: rgba(123, 128, 255, 0.48);
            --mmc-app-background:
                radial-gradient(
                    circle at 88% 4%,
                    rgba(47, 53, 255, 0.20),
                    transparent 27%
                ),
                radial-gradient(
                    circle at 8% 98%,
                    rgba(47, 53, 255, 0.10),
                    transparent 25%
                ),
                #0B0B0D;
        """

    st.markdown(
        f"""
        <style>
            :root {{
                {theme_variables}
            }}

            html,
            body,
            [class*="css"] {{
                font-family:
                    Inter,
                    ui-sans-serif,
                    system-ui,
                    -apple-system,
                    BlinkMacSystemFont,
                    "Segoe UI",
                    sans-serif;
            }}

            .stApp {{
                background: var(--mmc-app-background);
                color: var(--mmc-text);
            }}

            [data-testid="stHeader"] {{
                background: transparent;
            }}

            [data-testid="stToolbar"] {{
                right: 1rem;
            }}

            [data-testid="stSidebar"] {{
                background: var(--mmc-black);
                border-right: 1px solid var(--mmc-border);
            }}

            [data-testid="stSidebar"] * {{
                color: var(--mmc-text);
            }}

            [data-testid="stSidebarContent"] {{
                padding-top: 0.7rem;
            }}

            [data-testid="stSidebarNav"] {{
                padding-top: 1.15rem;
            }}

            [data-testid="stSidebarNav"] ul {{
                gap: 0.22rem;
            }}

            [data-testid="stSidebarNav"] a {{
                border: 1px solid transparent;
                border-radius: 0.8rem;
                margin: 0.08rem 0.6rem;
                padding: 0.62rem 0.75rem;
                transition:
                    background 160ms ease,
                    border-color 160ms ease,
                    transform 160ms ease;
            }}

            [data-testid="stSidebarNav"] a:hover {{
                background: var(--mmc-blue-soft);
                border-color: var(--mmc-border);
                transform: translateX(2px);
            }}

            [data-testid="stSidebarNav"] a[aria-current="page"] {{
                background:
                    linear-gradient(
                        90deg,
                        rgba(47, 53, 255, 0.34),
                        rgba(47, 53, 255, 0.18)
                    );
                border-color: rgba(110, 115, 255, 0.38);
                box-shadow: inset 3px 0 0 var(--mmc-blue);
                color: var(--mmc-text);
                font-weight: 750;
            }}

            .block-container {{
                max-width: 1440px;
                padding: 3.25rem 2.75rem 4.5rem;
            }}

            h1,
            h2,
            h3,
            h4 {{
                color: var(--mmc-text) !important;
                letter-spacing: -0.035em;
            }}

            h1 {{
                font-size: clamp(2.55rem, 4.6vw, 4.6rem);
                font-weight: 760;
                line-height: 1.02;
                margin-bottom: 0.9rem;
            }}

            h2 {{
                font-size: clamp(1.55rem, 2.4vw, 2.15rem);
                font-weight: 730;
                line-height: 1.15;
                margin-top: 2.35rem;
            }}

            h3 {{
                font-size: 1.17rem;
                font-weight: 720;
                line-height: 1.25;
            }}

            h4 {{
                font-size: 0.95rem;
                font-weight: 720;
            }}

            p,
            li,
            label,
            [data-testid="stMarkdownContainer"] {{
                color: var(--mmc-muted);
            }}

            [data-testid="stCaptionContainer"] {{
                color: var(--mmc-subtle);
            }}

            [data-testid="stMarkdownContainer"] strong {{
                color: var(--mmc-text);
            }}

            .mmc-eyebrow {{
                color: var(--mmc-blue);
                font-size: 0.74rem;
                font-weight: 830;
                letter-spacing: 0.13em;
                margin-bottom: 0.9rem;
                text-transform: uppercase;
            }}

            .mmc-lede {{
                color: var(--mmc-muted);
                font-size: clamp(1.05rem, 1.5vw, 1.18rem);
                line-height: 1.68;
                max-width: 800px;
            }}

            .mmc-card {{
                background:
                    linear-gradient(
                        145deg,
                        var(--mmc-surface),
                        var(--mmc-surface-raised)
                    );
                border: 1px solid var(--mmc-border);
                border-radius: 1rem;
                box-shadow: var(--mmc-shadow-soft);
                min-height: 100%;
                padding: 1.4rem;
            }}

            .mmc-card-title {{
                color: var(--mmc-text);
                font-size: 1.02rem;
                font-weight: 760;
                letter-spacing: -0.018em;
                margin-bottom: 0.55rem;
            }}

            .mmc-card-copy {{
                color: var(--mmc-muted);
                font-size: 0.95rem;
                line-height: 1.62;
                margin: 0;
            }}

            .mmc-metric {{
                background:
                    linear-gradient(
                        135deg,
                        rgba(47, 53, 255, 0.30),
                        var(--mmc-surface)
                    );
                border: 1px solid rgba(104, 109, 255, 0.42);
                border-radius: 1rem;
                box-shadow: var(--mmc-shadow-soft);
                min-height: 9.1rem;
                overflow: hidden;
                padding: 1.3rem;
                position: relative;
            }}

            .mmc-metric::after {{
                background: rgba(255, 255, 255, 0.10);
                border-radius: 50%;
                content: "";
                height: 9rem;
                position: absolute;
                right: -4rem;
                top: -5rem;
                width: 9rem;
            }}

            .mmc-metric-label {{
                color: var(--mmc-muted);
                font-size: 0.75rem;
                font-weight: 750;
                letter-spacing: 0.075em;
                position: relative;
                text-transform: uppercase;
                z-index: 1;
            }}

            .mmc-metric-value {{
                color: var(--mmc-text);
                font-size: 2.55rem;
                font-weight: 810;
                letter-spacing: -0.06em;
                line-height: 1.1;
                margin-top: 0.62rem;
                position: relative;
                z-index: 1;
            }}

            .mmc-badge {{
                background: var(--mmc-blue-soft);
                border: 1px solid rgba(100, 105, 255, 0.40);
                border-radius: 999px;
                color: var(--mmc-text);
                display: inline-block;
                font-size: 0.73rem;
                font-weight: 720;
                letter-spacing: -0.01em;
                margin: 0 0.32rem 0.45rem 0;
                padding: 0.3rem 0.64rem;
            }}

            .mmc-badge--success {{
                background: var(--mmc-success-soft);
                border-color: var(--mmc-success);
                color: var(--mmc-success);
            }}

            .mmc-badge--warning {{
                background: var(--mmc-warning-soft);
                border-color: var(--mmc-warning);
                color: var(--mmc-warning);
            }}

            .mmc-badge--danger {{
                background: var(--mmc-danger-soft);
                border-color: var(--mmc-danger);
                color: var(--mmc-danger);
            }}

            .mmc-divider {{
                border-top: 1px solid var(--mmc-border);
                margin: 2.35rem 0;
            }}

            .mmc-notice {{
                background: var(--mmc-blue-soft);
                border: 1px solid rgba(100, 105, 255, 0.28);
                border-left: 3px solid var(--mmc-blue);
                border-radius: 0.75rem;
                color: var(--mmc-muted);
                font-size: 0.94rem;
                line-height: 1.58;
                max-width: 100%;
                padding: 0.95rem 1rem;
            }}

            .mmc-sidebar-identity {{
                border-bottom: 1px solid var(--mmc-border);
                margin: 0.3rem 0.75rem 1.1rem;
                padding: 0.75rem 0 1.3rem;
            }}

            .mmc-sidebar-tagline {{
                color: var(--mmc-muted);
                font-size: 0.88rem;
                line-height: 1.5;
                margin: 0;
            }}

            .mmc-sidebar-label {{
                color: var(--mmc-subtle);
                font-size: 0.7rem;
                font-weight: 760;
                letter-spacing: 0.1em;
                margin: 1.25rem 0 0.15rem 0.75rem;
                text-transform: uppercase;
            }}

            div[data-testid="stSelectbox"] > div > div,
            div[data-testid="stTextInput"] input,
            div[data-testid="stTextArea"] textarea {{
                background: var(--mmc-surface) !important;
                border-color: var(--mmc-border) !important;
                border-radius: 0.72rem !important;
                color: var(--mmc-text) !important;
            }}

            div[data-testid="stTextInput"] input,
            div[data-testid="stTextArea"] textarea {{
                caret-color: var(--mmc-blue);
            }}

            div[data-testid="stTextInput"] input::placeholder,
            div[data-testid="stTextArea"] textarea::placeholder {{
                color: var(--mmc-subtle);
            }}

            div[data-baseweb="select"] > div {{
                background: var(--mmc-surface) !important;
                border-color: var(--mmc-border) !important;
                border-radius: 0.72rem !important;
                color: var(--mmc-text) !important;
            }}

            div[data-baseweb="select"] * {{
                color: var(--mmc-text) !important;
            }}

            div[data-baseweb="popover"],
            [data-baseweb="menu"] {{
                background: var(--mmc-surface-raised) !important;
            }}

            [data-baseweb="menu"] li {{
                color: var(--mmc-text) !important;
            }}

            [data-baseweb="menu"] li:hover {{
                background: var(--mmc-blue-soft) !important;
            }}

            div[data-testid="stButton"] > button,
            div[data-testid="stFormSubmitButton"] > button {{
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
            }}

            div[data-testid="stButton"] > button:hover,
            div[data-testid="stFormSubmitButton"] > button:hover {{
                background: #4148FF;
                border-color: rgba(255, 255, 255, 0.30);
                box-shadow: 0 12px 30px rgba(47, 53, 255, 0.32);
                transform: translateY(-1px);
            }}

            div[data-testid="stButton"] > button[kind="secondary"] {{
                background: var(--mmc-surface-raised);
                border-color: var(--mmc-border);
                box-shadow: none;
                color: var(--mmc-text) !important;
            }}

            div[data-testid="stButton"] > button[kind="secondary"]:hover {{
                background: var(--mmc-blue-soft);
                border-color: var(--mmc-border-strong);
                box-shadow: none;
            }}

            [data-testid="stExpander"] {{
                background: var(--mmc-surface);
                border: 1px solid var(--mmc-border);
                border-radius: 0.82rem;
                overflow: hidden;
            }}

            [data-testid="stExpander"] summary {{
                color: var(--mmc-text);
                font-weight: 650;
            }}

            [data-testid="stAlert"] {{
                border: 1px solid var(--mmc-border);
                border-radius: 0.78rem;
            }}

            [data-testid="stAlert"] * {{
                color: var(--mmc-text);
            }}

            [data-testid="stDataFrame"] {{
                border: 1px solid var(--mmc-border);
                border-radius: 0.9rem;
                overflow: hidden;
            }}

            blockquote {{
                background: var(--mmc-surface-soft);
                border-left: 3px solid var(--mmc-blue);
                border-radius: 0 0.6rem 0.6rem 0;
                color: var(--mmc-muted);
                line-height: 1.65;
                margin: 0.8rem 0 1rem;
                padding: 0.8rem 1rem;
            }}

            button:focus-visible,
            input:focus-visible,
            textarea:focus-visible,
            [data-baseweb="select"] > div:focus-within {{
                box-shadow: 0 0 0 3px var(--mmc-focus) !important;
                outline: none !important;
            }}

            @media (prefers-reduced-motion: reduce) {{
                *,
                *::before,
                *::after {{
                    scroll-behavior: auto !important;
                    transition-duration: 0.01ms !important;
                }}
            }}

            @media (max-width: 900px) {{
                .block-container {{
                    padding: 2.5rem 1.6rem 3.5rem;
                }}

                .mmc-card {{
                    padding: 1.15rem;
                }}

                .mmc-metric {{
                    min-height: 7.8rem;
                    padding: 1.1rem;
                }}

                .mmc-metric-value {{
                    font-size: 2.15rem;
                }}
            }}

            @media (max-width: 640px) {{
                .block-container {{
                    padding: 1.9rem 1rem 2.75rem;
                }}

                h1 {{
                    font-size: 2.35rem;
                }}

                h2 {{
                    font-size: 1.62rem;
                }}

                .mmc-lede {{
                    font-size: 1rem;
                    line-height: 1.6;
                }}

                .mmc-card {{
                    margin-bottom: 0.85rem;
                    padding: 1rem;
                }}

                .mmc-metric {{
                    margin-bottom: 0.75rem;
                    min-height: auto;
                }}

                .mmc-divider {{
                    margin: 1.65rem 0;
                }}
            }}
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

        st.markdown(
            '<div class="mmc-sidebar-label">Appearance</div>',
            unsafe_allow_html=True,
        )

        if "appearance" not in st.session_state:
            st.session_state.appearance = DREAM

        st.selectbox(
            "Appearance",
            options=[DREAM, REALITY],
            key="appearance",
            label_visibility="collapsed",
        )
