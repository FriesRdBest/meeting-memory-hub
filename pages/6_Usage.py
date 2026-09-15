from __future__ import annotations

from datetime import datetime, timezone

import streamlit as st

from config import PAGE_PREFIX
from utils.ui import configure_page, render_divider

configure_page(f"{PAGE_PREFIX} · Usage")

st.markdown(
    f'<div class="mmc-eyebrow">{PAGE_PREFIX} · Usage (admin only)</div>',
    unsafe_allow_html=True,
)
st.title("Usage (admin only)")

st.caption(
    "This page is for the app owner only. It shows anonymous usage metrics, "
    "not visible to end users in normal navigation."
)

from stores import get_json_store

store = get_json_store()
sessions = store.get("sessions", [])
usage_events = store.get("usage_events", [])

if not sessions:
    st.caption("No usage data yet. Interact with the app to generate sessions.")
    st.stop()

# Basic aggregates
total_sessions = len(sessions)
total_seconds = sum(s.get("total_seconds", 0) for s in sessions)
total_minutes = total_seconds / 60.0

avg_seconds = (total_seconds / total_sessions) if total_sessions else 0
avg_minutes = avg_seconds / 60.0

# Top sessions by duration
top_sessions = sorted(
    sessions,
    key=lambda s: s.get("total_seconds", 0),
    reverse=True,
)[:10]

st.metric("Total sessions", total_sessions)
st.metric("Total minutes (all sessions)", round(total_minutes, 1))
st.metric("Average minutes per session", round(avg_minutes, 1))

render_divider()

st.subheader("Top sessions by duration")

for i, s in enumerate(top_sessions, start=1):
    user_id = s.get("user_id", "unknown")
    start_iso = s.get("start", "")
    total_sec = s.get("total_seconds", 0)

    if start_iso:
        start_dt = datetime.fromisoformat(start_iso).astimezone()
        start_str = start_dt.strftime("%Y-%m-%d %H:%M")
    else:
        start_str = "unknown"

    minutes = round(total_sec / 60.0, 1)

    st.markdown(
        f"**#{i} · {minutes} min · user `{user_id[:8]}...` · started {start_str}**"
    )
    st.caption(f"Last heartbeat: {s.get('last_heartbeat', 'unknown')}")

render_divider()

st.subheader("Recent usage events")

recent_events = sorted(
    usage_events,
    key=lambda e: e.get("timestamp", ""),
    reverse=True,
)[:50]

if not recent_events:
    st.caption("No heartbeat events recorded yet.")
else:
    for e in recent_events:
        user_id = e.get("user_id", "unknown")
        ts_iso = e.get("timestamp", "")
        page = e.get("page", "unknown")

        if ts_iso:
            ts_dt = datetime.fromisoformat(ts_iso).astimezone()
            ts_str = ts_dt.strftime("%Y-%m-%d %H:%M:%S")
        else:
            ts_str = "unknown"

        st.markdown(
            f"`{ts_str}` · user `{user_id[:8]}...` · page `{page}`"
        )
