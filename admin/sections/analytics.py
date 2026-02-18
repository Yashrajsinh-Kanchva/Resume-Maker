import streamlit as st
import pandas as pd
import plotly.express as px
import requests

def analytics_page(api_base: str):
    st.header("📊 Analytics & Insights")

    headers = {
        "X-Admin-Email": st.session_state.admin["email"]
    }

    res = requests.get(
        f"{api_base}/analytics",
        headers=headers,
        timeout=5
    )

    if not res.ok:
        st.error("Failed to load analytics data")
        return

    data = res.json()

    # ================= USERS OVER TIME =================
    st.subheader("👤 User Registrations Over Time")

    users_raw = data.get("users_over_time", [])
    users_df = pd.DataFrame(users_raw)

    if not users_df.empty:
        users_df = users_df.dropna(subset=["_id"])
        users_df.rename(columns={"_id": "date", "count": "users"}, inplace=True)

        st.plotly_chart(
            px.line(users_df, x="date", y="users", markers=True),
            use_container_width=True
        )
    else:
        st.info("No user registration data")

    # ================= RESUMES OVER TIME =================
    st.subheader("📄 Resumes Created Over Time")

    resumes_raw = data.get("resumes_over_time", [])
    resumes_df = pd.DataFrame(resumes_raw)

    if not resumes_df.empty:
        # Remove invalid rows
        resumes_df = resumes_df.dropna(subset=["_id"])

        # Rename columns
        resumes_df.rename(
            columns={"_id": "date", "count": "resumes"},
            inplace=True
        )

        # Convert date string → datetime
        resumes_df["date"] = pd.to_datetime(resumes_df["date"])

        # Sort by date (VERY IMPORTANT)
        resumes_df = resumes_df.sort_values("date")

        fig = px.line(
            resumes_df,
            x="date",
            y="resumes",
            markers=True,
            labels={
                "date": "Date",
                "resumes": "Number of Resumes"
            },
            title="Resumes Created Over Time"
        )

        fig.update_traces(line_width=3)
        fig.update_layout(
            xaxis={"tickformat": "%d %b %Y"},
            yaxis={"dtick": 1},
            height=400
        )

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("No resume activity data available")

    # ================= TOP USERS BY RESUME COUNT =================
    st.subheader("🏆 Top Users by Resume Count")

    top_users = data.get("top_users", [])

    if top_users:
        df_top = pd.DataFrame(top_users)

        # Ensure columns exist
        if "user_email" in df_top.columns and "count" in df_top.columns:
            fig = px.bar(
                df_top,
                x="user_email",
                y="count",
                text="count",
                labels={
                    "user_email": "User Email",
                    "count": "Number of Resumes"
                }
            )
            fig.update_traces(textposition="outside")

            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Top users data format is invalid")
    else:
        st.info("No top user data available")