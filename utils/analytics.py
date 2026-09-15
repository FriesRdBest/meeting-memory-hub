from __future__ import annotations

import uuid
from datetime import datetime, timezone

import streamlit as st

from repositories.json_store import get_json_store


def get_or_create_anonymous_user_id() -> str:
    if "anonymous_user_id" not in st.session_state:
        st.session_state.anonymous_user_id = str(uuid.uuid4())
    return st.session_state.anonymous_user_id


def get_session_start_time() -> datetime:
    if "session_start_time" not in st.session_state:
        st.session_state.session_start_time = datetime.now(timezone.utc)
    return st.session_state.session_start_time


def _safe_current_page() -> str:
    # Best-effort page identifier; fallback to "unknown"
    try:
        params = st.experimental_get_query_params()
        page = params.get("page", [])
        if page:
            return str(page[0])
    except Exception:
        pass
    return "unknown"


def log_usage_heartbeat() -> None:
    user_id = get_or_create_anonymous_user_id()
    start_time = get_session_start_time()
    now = datetime.now(timezone.utc)
    page = _safe_current_page()

    store = get_json_store()
    usage_events = store.get("usage_events", [])

    usage_events.append(
        {
            "type": "heartbeat",
            "user_id": user_id,
            "session_start": start_time.isoformat(),
            "timestamp": now.isoformat(),
            "page": page,
        }
    )

    # Keep list bounded
    if len(usage_events) > 5000:
        usage_events = usage_events[-5000:]

    store["usage_events"] = usage_events


def update_session_duration() -> None:
    user_id = get_or_create_anonymous_user_id()
    start_time = get_session_start_time()
    now = datetime.now(timezone.utc)

    store = get_json_store()
    sessions = store.get("sessions", [])

    session = None
    for s in sessions:
        if s["user_id"] == user_id and s["start"] == start_time.isoformat():
            session = s
            break

    if session is None:
        session = {
            "user_id": user_id,
            "start": start_time.isoformat(),
            "last_heartbeat": start_time.isoformat(),
            "total_seconds": 0,
        }
        sessions.append(session)

    prev = datetime.fromisoformat(session["last_heartbeat"])
    delta = (now - prev).total_seconds()
    if delta > 0:
        session["total_seconds"] += delta
    session["last_heartbeat"] = now.isoformat()

    if len(sessions) > 2000:
        sessions = sessions[-2000:]

    store["sessions"] = sessions


def log_usage() -> None:
    # Call this once per page load / interaction
    log_usage_heartbeat()
    update_session_duration()
