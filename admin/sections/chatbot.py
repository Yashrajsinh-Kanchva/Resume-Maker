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
                url = f"{api_base}/chatbot"
                admin_email = st.session_state.admin.get("email", "")
                print(f"[admin_chatbot_ui] POST {url} email={admin_email!r} q={prompt!r}")

                res = requests.post(
                    url,
                    json={"question": prompt},
                    headers={"X-Admin-Email": admin_email},
                    timeout=10,
                )
                build = res.headers.get("X-Chatbot-Build")
                mode = res.headers.get("X-Chatbot-Mode")
                print(f"[admin_chatbot_ui] status={res.status_code} build={build!r} mode={mode!r} body={res.text[:200]!r}")
                if res.ok:
                    try:
                        data = res.json()
                        # Backend always returns {"answer": "..."} via _respond() helper
                        answer = data.get("answer", res.text)
                    except Exception as e:
                        print(f"[admin_chatbot_ui] JSON parse error: {e}")
                        answer = "Received an invalid response from the server."
                    st.write(answer)
                    st.caption(f"build: {build or '(missing)'} | mode: {mode or '(missing)'}")
                    st.session_state.chat_history.append({"role": "assistant", "content": answer})
                else:
                    err_msg = "Could not get a response. Please try again."
                    try:
                        # Backend always returns {"answer": "..."} even for errors (401, 403, 400)
                        # Never use .get("message") - backend uses "answer" field consistently
                        err_msg = res.json().get("answer", err_msg)
                    except Exception as e:
                        print(f"[admin_chatbot_ui] Error response JSON parse failed: {e}")
                        # Fall back to default error message if JSON parsing fails
                        pass
                    st.write(err_msg)
                    st.caption(f"build: {build or '(missing)'} | mode: {mode or '(missing)'}")
                    st.session_state.chat_history.append({"role": "assistant", "content": err_msg})
            except requests.exceptions.RequestException:
                err_msg = "Server is not reachable. Please try again later."
                st.write(err_msg)
                st.session_state.chat_history.append({"role": "assistant", "content": err_msg})

        st.rerun()
