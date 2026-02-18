import streamlit as st
import requests


def _parse_success_response(res: requests.Response) -> str:
    """Parse JSON body from a successful chatbot response. Returns answer or fallback."""
    try:
        data = res.json()
        return data.get("answer", res.text)
    except Exception as e:
        print(f"[admin_chatbot_ui] JSON parse error: {e}")
        return "Received an invalid response from the server."


def _parse_error_response(res: requests.Response, default: str) -> str:
    """Parse error body from a failed chatbot response. Returns answer or default."""
    try:
        return res.json().get("answer", default)
    except Exception as e:
        print(f"[admin_chatbot_ui] Error response JSON parse failed: {e}")
        return default


def _fetch_chatbot_reply(api_base: str, prompt: str, admin_email: str) -> tuple[str, str | None, str | None]:
    """
    POST to chatbot API and return (message, build_header, mode_header).
    Raises requests.exceptions.RequestException on network errors.
    """
    url = f"{api_base}/chatbot"
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
        answer = _parse_success_response(res)
    else:
        answer = _parse_error_response(res, "Could not get a response. Please try again.")

    return (answer, build, mode)


def chatbot_page(api_base: str) -> None:
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
                admin_email = st.session_state.admin.get("email", "")
                answer, build, mode = _fetch_chatbot_reply(api_base, prompt, admin_email)
                st.write(answer)
                st.caption(f"build: {build or '(missing)'} | mode: {mode or '(missing)'}")
                st.session_state.chat_history.append({"role": "assistant", "content": answer})
            except requests.exceptions.RequestException:
                err_msg = "Server is not reachable. Please try again later."
                st.write(err_msg)
                st.session_state.chat_history.append({"role": "assistant", "content": err_msg})

        st.rerun()
