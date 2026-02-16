import streamlit as st
import requests


def chatbot_page(api_base: str):
    st.header("Chatbot")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if prompt := st.chat_input("Ask about users, resumes, or feedback..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            try:
                res = requests.post(
                    f"{api_base}/chatbot",
                    json={"question": prompt},
                    headers={"X-Admin-Email": st.session_state.admin.get("email", "")},
                    timeout=10,
                )
                if res.ok:
                    data = res.json()
                    answer = data.get("answer", res.text)
                    st.write(answer)
                    st.session_state.chat_history.append({"role": "assistant", "content": answer})
                else:
                    err_msg = "Could not get a response. Please try again."
                    try:
                        err_msg = res.json().get("answer", err_msg)
                    except Exception:
                        pass
                    st.write(err_msg)
                    st.session_state.chat_history.append({"role": "assistant", "content": err_msg})
            except requests.exceptions.RequestException:
                err_msg = "Server is not reachable. Please try again later."
                st.write(err_msg)
                st.session_state.chat_history.append({"role": "assistant", "content": err_msg})

        st.rerun()
