import streamlit as st
import requests
import pandas as pd
from datetime import datetime
from email.utils import parsedate_to_datetime

_DATE_FMT = "%d %b %Y %H:%M"
COL_CREATED_AT = "Created At"


def _format_date(value):
    """Format created_at for display: support None, datetime, or ISO/RFC 2822 string."""
    if not value:
        return ""
    if isinstance(value, datetime):
        return value.strftime(_DATE_FMT)
    if isinstance(value, str):
        try:
            if "GMT" in value:
                return parsedate_to_datetime(value).strftime(_DATE_FMT)
            return datetime.fromisoformat(value).strftime(_DATE_FMT)
        except (ValueError, TypeError):
            return value
    return value


def _fetch_resumes(api_base: str) -> tuple[dict | None, str | None]:
    """GET /resumes. Returns (payload, None) on success or (None, error_message) on failure."""
    try:
        res = requests.get(f"{api_base}/resumes", timeout=5)
        res.raise_for_status()
        return (res.json(), None)
    except requests.exceptions.RequestException as e:
        return (None, str(e))


def _render_csv_export(api_base: str) -> None:
    """Render CSV download button or show warning on fetch failure."""
    try:
        csv_res = requests.get(f"{api_base}/resumes/export", timeout=5)
        csv_res.raise_for_status()
        st.download_button(
            "⬇️ Export Resumes CSV",
            data=csv_res.text,
            file_name="resumes.csv",
            mime="text/csv"
        )
    except requests.exceptions.RequestException as e:
        st.warning(f"CSV export failed: {e}")


def resumes_page(api_base: str) -> None:
    st.header("📄 Resumes")

    payload, err = _fetch_resumes(api_base)
    if err:
        st.error(f"Request failed: {err}")
        return

    if not payload.get("success"):
        st.error("Invalid API response format")
        st.json(payload)
        return

    resumes = payload.get("data", [])
    st.metric("Total Resumes", len(resumes))

    if not resumes:
        st.info("No resumes found")
        return

    df = pd.DataFrame(resumes)
    df.rename(columns={
        "email": "Email",
        "title": "Title",
        "created_at": COL_CREATED_AT
    }, inplace=True)

    if COL_CREATED_AT in df.columns:
        df[COL_CREATED_AT] = df[COL_CREATED_AT].apply(_format_date)

    st.subheader("📋 Resume List")
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.subheader("🔍 Resume Details")
    for r in resumes:
        email = r.get("email", "N/A")
        title = r.get("title", "Untitled")
        created_at = _format_date(r.get("created_at"))
        with st.expander(f"{email} — {title}"):
            st.write(f"**Email:** {email}")
            st.write(f"**Title:** {title}")
            st.write(f"**{COL_CREATED_AT}:** {created_at}")

    st.divider()
    _render_csv_export(api_base)
