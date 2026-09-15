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
                --mmc-black: #0B0B0D;
                --mmc-surface: #15151A;
                --mmc-surface-raised: #1D1D24;
                --mmc-border: rgba(247, 247, 250, 0.12);
                --mmc-border-strong: rgba(119, 125, 255, 0.42);
                --mmc-text: #F7F7FA;
                --mmc-muted: #B7B7C6;
                --mmc-subtle: #858596;
                --mmc-success: #61D095;
                --mmc-warning: #F5BE62;
                --mmc-danger: #F17B7B;
                --mmc-radius: 1rem;
                --mmc-radius-small: 0.72rem;
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
                        circle at 88% 4%,
                        rgba(47, 53, 255, 0.18),
                        transparent 27%
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

            [data-testid="stToolbar"] {
                right: 1rem;
            }

            [data-testid="stSidebar"] {
                background: rgba(15, 15, 19, 0.98);
                border-right: 1px solid var(--mmc-border);
            }

            [data-testid="stSidebar"] * {
                color: var(--mmc-text);
            }

            [data-testid="stSidebarContent"] {
                display: flex;
                flex-direction: column;
                min-height: 100%;
                padding-top: 0.7rem;
            }

            /*
             * Sidebar workflow narrative
             *
             * Page sequence:
             * 1. Overview
             * 2. Signal Desk
             * 3. Pattern Library
             * 4. Action Queue
             * 5. Learning Loop
             * 6. Prototype Context
             *
             * Overview and Prototype Context are bookends.
             * Items 2–5 are the working intelligence flow.
             */
            [data-testid="stSidebarNav"] {
                flex: 1;
                padding-top: 0.55rem;
            }

            [data-testid="stSidebarNav"] ul {
                display: flex;
                flex-direction: column;
                gap: 0.3rem;
                min-height: calc(100vh - 11.5rem);
                padding-bottom: 0.75rem;
            }

            [data-testid="stSidebarNav"] li {
                position: relative;
            }

            [data-testid="stSidebarNav"] a {
                position: relative;
                z-index: 2;
                display: flex;
                align-items: center;
                min-height: 2.85rem;
                margin: 0;
                padding: 0.65rem 0.78rem;
                border: 1px solid transparent;
                border-radius: 0.8rem;
                color: var(--mmc-muted);
                transition:
                    background 160ms ease,
                    border-color 160ms ease,
                    box-shadow 160ms ease,
                    color 160ms ease,
                    transform 160ms ease;
            }

            [data-testid="stSidebarNav"] a:hover {
                background: rgba(47, 53, 255, 0.13);
                border-color: rgba(117, 122, 255, 0.23);
                color: var(--mmc-text);
                transform: translateX(2px);
            }

            /*
             * Overview: neutral top bookend with complementary padding.
             */
            [data-testid="stSidebarNav"] li:first-child {
                margin: 0 0.6rem 1.2rem;
            }

            [data-testid="stSidebarNav"] li:first-child a {
                background: rgba(247, 247, 250, 0.025);
                border-color: rgba(247, 247, 250, 0.07);
                color: var(--mmc-text);
            }

            /*
             * The middle workflow rail spans Signal Desk through Learning Loop.
             * The line begins below Signal Desk and ends above Learning Loop.
             */
            [data-testid="stSidebarNav"] li:nth-child(2),
            [data-testid="stSidebarNav"] li:nth-child(3),
            [data-testid="stSidebarNav"] li:nth-child(4),
            [data-testid="stSidebarNav"] li:nth-child(5) {
                margin: 0 0.6rem;
                padding-left: 0.82rem;
            }

            [data-testid="stSidebarNav"] li:nth-child(2)::after,
            [data-testid="stSidebarNav"] li:nth-child(3)::after,
            [data-testid="stSidebarNav"] li:nth-child(4)::after {
                position: absolute;
                top: 2.7rem;
                bottom: -0.5rem;
                left: 1.12rem;
                z-index: 0;
                width: 1px;
                content: "";
                background:
                    repeating-linear-gradient(
                        to bottom,
                        rgba(99, 105, 255, 0.68) 0 3px,
                        rgba(99, 105, 255, 0) 3px 8px
                    );
                opacity: 0.62;
            }

            /*
             * Workflow nodes: small circles to the left of the page label.
             * They replace the earlier pill idea and better suit vertical nav.
             */
            [data-testid="stSidebarNav"] li:nth-child(2) a::before,
            [data-testid="stSidebarNav"] li:nth-child(3) a::before,
            [data-testid="stSidebarNav"] li:nth-child(4) a::before,
            [data-testid="stSidebarNav"] li:nth-child(5) a::before {
                position: absolute;
                top: 50%;
                left: 0.12rem;
                z-index: 3;
                width: 0.62rem;
                height: 0.62rem;
                border: 2px solid rgba(154, 158, 255, 0.7);
                border-radius: 50%;
                content: "";
                background: var(--mmc-surface);
                box-shadow: 0 0 0 3px rgba(15, 15, 19, 0.96);
                transform: translateY(-50%);
                transition:
                    background 160ms ease,
                    border-color 160ms ease,
                    box-shadow 160ms ease,
                    transform 160ms ease;
            }

            /*
             * Completed / signal-passed stages:
             * Applies to pages before the current active workflow page.
             */
            [data-testid="stSidebarNav"] li:nth-child(2):has(
                ~ li:nth-child(3) a[aria-current="page"]
            ) a,
            [data-testid="stSidebarNav"] li:nth-child(2):has(
                ~ li:nth-child(4) a[aria-current="page"]
            ) a,
            [data-testid="stSidebarNav"] li:nth-child(2):has(
                ~ li:nth-child(5) a[aria-current="page"]
            ) a,
            [data-testid="stSidebarNav"] li:nth-child(3):has(
                ~ li:nth-child(4) a[aria-current="page"]
            ) a,
            [data-testid="stSidebarNav"] li:nth-child(3):has(
                ~ li:nth-child(5) a[aria-current="page"]
            ) a,
            [data-testid="stSidebarNav"] li:nth-child(4):has(
                ~ li:nth-child(5) a[aria-current="page"]
            ) a {
                background: rgba(47, 53, 255, 0.10);
                border-color: rgba(94, 100, 255, 0.19);
                color: #D9DAFF;
            }

            [data-testid="stSidebarNav"] li:nth-child(2):has(
                ~ li:nth-child(3) a[aria-current="page"]
            ) a::before,
            [data-testid="stSidebarNav"] li:nth-child(2):has(
                ~ li:nth-child(4) a[aria-current="page"]
            ) a::before,
            [data-testid="stSidebarNav"] li:nth-child(2):has(
                ~ li:nth-child(5) a[aria-current="page"]
            ) a::before,
            [data-testid="stSidebarNav"] li:nth-child(3):has(
                ~ li:nth-child(4) a[aria-current="page"]
            ) a::before,
            [data-testid="stSidebarNav"] li:nth-child(3):has(
                ~ li:nth-child(5) a[aria-current="page"]
            ) a::before,
            [data-testid="stSidebarNav"] li:nth-child(4):has(
                ~ li:nth-child(5) a[aria-current="page"]
            ) a::before {
                border-color: #7880FF;
                background: #5F66FF;
                box-shadow:
                    0 0 0 3px rgba(15, 15, 19, 0.96),
                    0 0 12px rgba(47, 53, 255, 0.48);
            }

            /*
             * Active workflow stage:
             * stronger visual separation without a large or flashy pill.
             */
            [data-testid="stSidebarNav"] li:nth-child(2) a[aria-current="page"],
            [data-testid="stSidebarNav"] li:nth-child(3) a[aria-current="page"],
            [data-testid="stSidebarNav"] li:nth-child(4) a[aria-current="page"] {
                background:
                    linear-gradient(
                        90deg,
                        rgba(47, 53, 255, 0.39),
                        rgba(47, 53, 255, 0.14)
                    );
                border-color: rgba(123, 129, 255, 0.54);
                box-shadow:
                    inset 3px 0 0 #8A8FFF,
                    0 8px 24px rgba(19, 25, 182, 0.18);
                color: #FFFFFF;
                font-weight: 760;
            }

            [data-testid="stSidebarNav"] li:nth-child(2) a[aria-current="page"]::before,
            [data-testid="stSidebarNav"] li:nth-child(3) a[aria-current="page"]::before,
            [data-testid="stSidebarNav"] li:nth-child(4) a[aria-current="page"]::before {
                border-color: #D8D9FF;
                background: var(--mmc-blue);
                box-shadow:
                    0 0 0 3px rgba(15, 15, 19, 0.96),
                    0 0 16px rgba(47, 53, 255, 0.78);
                transform: translateY(-50%) scale(1.12);
            }

            /*
             * Learning Loop: a calm, distinct final state.
             * It intentionally does not use the "signal in motion" treatment
             * that connects Signal, Pattern, and Action.
             */
            [data-testid="stSidebarNav"] li:nth-child(5) {
                margin-top: 0.38rem;
            }

            [data-testid="stSidebarNav"] li:nth-child(5) a {
                background: rgba(97, 208, 149, 0.035);
                border-color: rgba(97, 208, 149, 0.12);
            }

            [data-testid="stSidebarNav"] li:nth-child(5) a::before {
                border-color: rgba(97, 208, 149, 0.62);
                background: rgba(97, 208, 149, 0.08);
            }

            [data-testid="stSidebarNav"] li:nth-child(5) a[aria-current="page"] {
                background:
                    linear-gradient(
                        90deg,
                        rgba(97, 208, 149, 0.20),
                        rgba(97, 208, 149, 0.06)
                    );
                border-color: rgba(97, 208, 149, 0.48);
                box-shadow:
                    inset 3px 0 0 var(--mmc-success),
                    0 8px 24px rgba(37, 133, 79, 0.14);
                color: #FFFFFF;
                font-weight: 760;
            }

            [data-testid="stSidebarNav"] li:nth-child(5) a[aria-current="page"]::before {
                border-color: #D6FFE6;
                background: var(--mmc-success);
                box-shadow:
                    0 0 0 3px rgba(15, 15, 19, 0.96),
                    0 0 14px rgba(97, 208, 149, 0.55);
                transform: translateY(-50%) scale(1.12);
            }

            /*
             * Prototype Context: neutral bottom bookend, held down by the
             * flexible sidebar list space. No lifecycle line enters this item.
             */
            [data-testid="stSidebarNav"] li:last-child {
                margin: auto 0.6rem 0.3rem;
                padding-top: 1.15rem;
            }

            [data-testid="stSidebarNav"] li:last-child::before {
                position: absolute;
                top: 0.35rem;
                right: 0.15rem;
                left: 0.15rem;
                height: 1px;
                content: "";
                background: var(--mmc-border);
            }

            [data-testid="stSidebarNav"] li:last-child a {
                background: rgba(247, 247, 250, 0.025);
                border-color: rgba(247, 247, 250, 0.07);
                color: var(--mmc-muted);
            }

            /*
             * Standard active style for the two bookend pages.
             */
            [data-testid="stSidebarNav"] li:first-child a[aria-current="page"],
            [data-testid="stSidebarNav"] li:last-child a[aria-current="page"] {
                background: rgba(247, 247, 250, 0.08);
                border-color: rgba(247, 247, 250, 0.17);
                box-shadow: inset 3px 0 0 rgba(247, 247, 250, 0.68);
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
                color: var(--mmc-text) !important;
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
                color: var(--mmc-muted);
            }

            [data-testid="stCaptionContainer"] {
                color: var(--mmc-subtle);
            }

            [data-testid="stMarkdownContainer"] strong {
                color: var(--mmc-text);
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
                border: 1px solid var(--mmc-border);
                border-radius: var(--mmc-radius);
                box-shadow:
                    0 18px 46px rgba(0, 0, 0, 0.20),
                    inset 0 1px 0 rgba(255, 255, 255, 0.025);
                min-height: 100%;
                padding: 1.42rem;
                transition:
                    transform 0.15s ease,
                    box-shadow 0.15s ease;
            }

            .mmc-card:hover {
                transform: translateY(-2px);
                box-shadow:
                    0 22px 52px rgba(0, 0, 0, 0.26),
                    inset 0 1px 0 rgba(255, 255, 255, 0.035);
            }

            .mmc-card-title {
                color: var(--mmc-text);
                font-size: 1.03rem;
                font-weight: 760;
                letter-spacing: -0.022em;
                margin-bottom: 0.55rem;
            }

            .mmc-card-copy {
                color: var(--mmc-muted);
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
                border-radius: var(--mmc-radius);
                box-shadow:
                    0 18px 46px rgba(0, 0, 0, 0.22),
                    inset 0 1px 0 rgba(255, 255, 255, 0.06);
                min-height: 9.2rem;
                overflow: hidden;
                padding: 1.32rem;
                position: relative;
                transition:
                    transform 0.15s ease,
                    box-shadow 0.15s ease;
            }

            .mmc-metric:hover {
                transform: translateY(-2px);
                box-shadow:
                    0 22px 52px rgba(0, 0, 0, 0.28),
                    inset 0 1px 0 rgba(255, 255, 255, 0.08);
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
                color: var(--mmc-muted);
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
                transition:
                    transform 0.12s ease,
                    box-shadow 0.12s ease;
            }

            .mmc-badge:hover {
                transform: translateY(-1px);
                box-shadow: 0 6px 14px rgba(47, 53, 255, 0.18);
            }

            .mmc-badge--success {
                background: rgba(97, 208, 149, 0.14);
                border-color: rgba(97, 208, 149, 0.52);
                color: #7AE4A9;
            }

            .mmc-badge--warning {
                background: rgba(245, 190, 98, 0.15);
                border-color: rgba(245, 190, 98, 0.54);
                color: #FFD183;
            }

            .mmc-badge--danger {
                background: rgba(241, 123, 123, 0.14);
                border-color: rgba(241, 123, 123, 0.54);
                color: #FFAAAA;
            }

            .mmc-divider {
                border-top: 1px solid var(--mmc-border);
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
                border-left: 3px solid var(--mmc-blue);
                border-radius: 0.76rem;
                color: #C5C5D3;
                font-size: 0.94rem;
                line-height: 1.58;
                max-width: 100%;
                padding: 0.96rem 1.04rem;
            }

            .mmc-sidebar-identity {
                border-bottom: 1px solid var(--mmc-border);
                margin: 0.3rem 0.75rem 0.8rem;
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
                border-radius: var(--mmc-radius-small) !important;
                color: var(--mmc-text) !important;
                transition:
                    border-color 160ms ease,
                    box-shadow 160ms ease;
            }

            div[data-testid="stTextInput"] input::placeholder,
            div[data-testid="stTextArea"] textarea::placeholder {
                color: var(--mmc-subtle);
            }

            div[data-baseweb="select"] > div,
            div[data-baseweb="select"] * {
                color: var(--mmc-text) !important;
            }

            div[data-baseweb="popover"],
            [data-baseweb="menu"] {
                background: var(--mmc-surface-raised) !important;
            }

            [data-baseweb="menu"] li {
                color: var(--mmc-text) !important;
            }

            [data-baseweb="menu"] li:hover {
                background: rgba(47, 53, 255, 0.16) !important;
            }

            div[data-testid="stButton"] > button,
            div[data-testid="stFormSubmitButton"] > button {
                background: var(--mmc-blue);
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
                color: var(--mmc-text) !important;
                transition:
                    background 160ms ease,
                    border-color 160ms ease,
                    transform 160ms ease;
            }

            div[data-testid="stButton"] > button[kind="secondary"]:hover {
                background: rgba(47, 53, 255, 0.14);
                border-color: var(--mmc-border-strong);
                transform: translateY(-1px);
            }

            [data-testid="stExpander"] {
                background: rgba(20, 20, 26, 0.84);
                border: 1px solid rgba(247, 247, 250, 0.13);
                border-radius: 0.84rem;
                overflow: hidden;
                transition:
                    border-color 160ms ease,
                    box-shadow 160ms ease;
            }

            [data-testid="stExpander"]:hover {
                border-color: rgba(119, 125, 255, 0.28);
                box-shadow: 0 8px 22px rgba(0, 0, 0, 0.18);
            }

            [data-testid="stExpander"] summary {
                color: var(--mmc-text);
                font-weight: 670;
            }

            [data-testid="stAlert"] {
                border: 1px solid rgba(247, 247, 250, 0.13);
                border-radius: 0.78rem;
                transition:
                    transform 0.12s ease,
                    box-shadow 0.12s ease;
            }

            [data-testid="stAlert"]:hover {
                transform: translateY(-1px);
                box-shadow: 0 10px 24px rgba(0, 0, 0, 0.16);
            }

            [data-testid="stAlert"] * {
                color: var(--mmc-text);
            }

            [data-testid="stDataFrame"] {
                border: 1px solid var(--mmc-border);
                border-radius: 0.9rem;
                overflow: hidden;
            }

            blockquote {
                background: rgba(47, 53, 255, 0.10);
                border-left: 3px solid var(--mmc-blue);
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

            @keyframes mmcFadeInRow {
                from {
                    opacity: 0;
                    transform: translateY(4px);
                }

                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }

            .mmc-new-row {
                animation: mmcFadeInRow 0.2s ease-out;
            }

            @keyframes mmcSoftPulse {
                0%,
                100% {
                    box-shadow: 0 0 0 0 rgba(47, 53, 255, 0.35);
                }

                50% {
                    box-shadow: 0 0 0 6px rgba(47, 53, 255, 0);
                }
            }

            .mmc-badge-new,
            .mmc-badge-alert {
                animation: mmcSoftPulse 1.8s infinite;
            }

            @keyframes mmcRadarSpin {
                0% {
                    transform: rotate(0deg);
                }

                100% {
                    transform: rotate(360deg);
                }
            }

            @keyframes mmcTextShine {
                0% {
                    background-position: -150% center;
                }

                60% {
                    background-position: 250% center;
                }

                100% {
                    background-position: 250% center;
                }
            }

            .mmc-signal-loader {
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                min-height: 40vh;
                position: relative;
            }

            .mmc-radar-container {
                position: relative;
                display: flex;
                align-items: center;
                justify-content: center;
                width: 5.5rem;
                height: 5.5rem;
                margin-bottom: 1rem;
            }

            .mmc-radar-ring {
                position: absolute;
                width: 100%;
                height: 100%;
                border: 2px solid rgba(47, 53, 255, 0.18);
                border-radius: 50%;
            }

            .mmc-radar-ring:nth-child(2) {
                width: 70%;
                height: 70%;
                border-color: rgba(47, 53, 255, 0.28);
            }

            .mmc-radar-sweep {
                position: absolute;
                width: 100%;
                height: 100%;
                border-radius: 50%;
                background: conic-gradient(
                    from 0deg,
                    rgba(47, 53, 255, 0) 0deg,
                    rgba(47, 53, 255, 0) 260deg,
                    rgba(47, 53, 255, 0.9) 300deg,
                    rgba(47, 53, 255, 0) 360deg
                );
                animation: mmcRadarSpin 2.2s linear infinite;
                filter: blur(1px);
            }

            .mmc-signal-loader-label {
                position: relative;
                background: linear-gradient(
                    90deg,
                    var(--mmc-muted) 0%,
                    var(--mmc-muted) 10%,
                    rgba(47, 53, 255, 0.95) 25%,
                    var(--mmc-muted) 40%,
                    var(--mmc-muted) 100%
                );
                background-clip: text;
                background-size: 200% 100%;
                color: transparent;
                font-size: 0.95rem;
                font-weight: 700;
                letter-spacing: 0.02em;
                animation: mmcTextShine 2.2s ease-in-out infinite;
                animation-delay: 0.15s;
                -webkit-background-clip: text;
            }

            @media (prefers-reduced-motion: reduce) {
                *,
                *::before,
                *::after {
                    animation-duration: 0.01ms !important;
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
                [data-testid="stSidebarNav"] ul {
                    min-height: auto;
                }

                [data-testid="stSidebarNav"] li:last-child {
                    margin-top: 1.15rem;
                }

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
                    min-height: auto;
                    margin-bottom: 0.75rem;
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
        f'<span class="{get_badge_class(label)}">{escape(label)}</span>'
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


def render_signal_loader(label: str = "Signals incoming…") -> None:
    st.markdown(
        f"""
        <div class="mmc-signal-loader">
            <div class="mmc-radar-container">
                <div class="mmc-radar-ring"></div>
                <div class="mmc-radar-ring"></div>
                <div class="mmc-radar-sweep"></div>
            </div>
            <div class="mmc-signal-loader-label">{escape(label)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
