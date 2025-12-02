"""
Streamlit frontend for NewsGenie.

Run locally:
    streamlit run src/ui/app.py
"""

from typing import Dict, List

import streamlit as st

from src.core.config import Settings
from src.workflow.graph import build_graph, run_graph


# Cache the compiled graph so it is built once per process.
@st.cache_resource
def load_graph():
    return build_graph()


# Lazily load settings so missing env vars can be surfaced in the UI.
@st.cache_resource
def load_settings():
    try:
        return Settings(), None
    except Exception as exc:  # noqa: BLE001
        return None, str(exc)


def ensure_history():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history: List[Dict[str, str]] = []


def main():
    st.set_page_config(page_title="NewsGenie", page_icon="🗞️", layout="wide")
    st.title("🗞️ NewsGenie")
    st.caption("AI-powered news + general query assistant")

    settings, settings_error = load_settings()

    # Sidebar controls
    with st.sidebar:
        st.header("Preferences")
        categories = ["No specific category", "Technology", "Finance", "Sports", "Politics", "Health", "Entertainment"]
        category = st.selectbox("News category (optional)", categories, index=0)
        custom_topic = st.text_input("Custom topic (optional)", value="", placeholder="e.g., AI policy, climate")
        st.markdown("---")
        st.subheader("Status")
        if settings_error:
            st.error(f"Config error: {settings_error}")
        else:
            st.success("Config loaded from .env")
        st.write(f"News API key: {'✅' if settings and settings.news_api_key else '⚠️ missing'}")
        st.write(f"OpenAI API key: {'✅' if settings and settings.openai_api_key else '⚠️ missing'}")
        st.markdown("---")
        st.info("Ask for the latest news on a topic or any general question.")

    ensure_history()

    # Display history
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("source") or msg.get("error"):
                meta = " · ".join(
                    part for part in [msg.get("source"), f"error: {msg['error']}" if msg.get("error") else None] if part
                )
                st.caption(meta)

    # User input
    user_prompt = st.chat_input("Ask for news or any question")
    if user_prompt:
        topic_hint = custom_topic.strip() or (category if category != "No specific category" else "")
        # Add a gentle hint to steer classification if a topic is chosen.
        enriched_prompt = (
            f"{user_prompt}\n\nTopic hint: {topic_hint}" if topic_hint else user_prompt
        )
        st.session_state.chat_history.append({"role": "user", "content": enriched_prompt})
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                graph = load_graph()
                try:
                    result = run_graph(graph, enriched_prompt)
                    reply = result.message
                    source = result.source
                    error = result.error
                except Exception as exc:  # noqa: BLE001
                    reply = "Sorry, something went wrong while processing your request."
                    source = "ui"
                    error = str(exc)
            st.markdown(reply)
            if source or error:
                meta = " · ".join(
                    part for part in [source, f"error: {error}" if error else None] if part
                )
                st.caption(meta)
        st.session_state.chat_history.append(
            {"role": "assistant", "content": reply, "source": source, "error": error}
        )


if __name__ == "__main__":
    main()
