import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load API key
load_dotenv()
API_KEY = os.getenv("API_KEY")

headers = {
    "Authorization": f"Bearer {API_KEY}"
}

# Page config
st.set_page_config(page_title="AI Chatbot", page_icon="🤖")

st.title("🤖 AI Chatbot")

# Mode selection
mode = st.radio("Choose mode:", ["Simple Chat", "Agent"])

# Session state for Agent context
if "previous_response_id" not in st.session_state:
    st.session_state.previous_response_id = None

# Session state for chat history (UI only)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Clear chat button
if st.button("Clear Chat"):
    st.session_state.messages = []
    st.session_state.previous_response_id = None
    st.rerun()

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("Type your message...")

if user_input:
    # Save and display user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    # ----------------------------
    # Simple Chat
    # ----------------------------
    if mode == "Simple Chat":
        payload = {
            "messages": [
                {
                    "role": "user",
                    "content": user_input
                }
            ],
            "max_completion_tokens": 500
        }

        with st.chat_message("assistant"):
            response_placeholder = st.empty()

            with st.spinner("Thinking..."):
                r = requests.post(
                    "https://server.iac.ac.il/api/v1/studentapi/chat/completions",
                    json=payload,
                    headers=headers
                )

            data = r.json()
            print("Quota status:", data.get("iac_quota_status"))

            try:
                answer = data["choices"][0]["message"]["content"]

                if answer and answer.strip():
                    response_placeholder.markdown(answer)
                else:
                    answer = "No response text"
                    response_placeholder.markdown(answer)
                    st.json(data)

            except Exception:
                answer = "Error reading response"
                response_placeholder.markdown(answer)
                st.json(data)

        # Save assistant message for UI display only
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })

    # ----------------------------
    # Agent
    # ----------------------------
    else:
        payload = {
            "reasoning": {"effort": "low"},
            "instructions": "Give a short answer up to 50 words only.",
            "input": user_input,
            "tools": [{"type": "web_search"}]
        }

        # Add API context if this is not the first message
        if st.session_state.previous_response_id is not None:
            payload["previous_response_id"] = st.session_state.previous_response_id

        with st.chat_message("assistant"):
            response_placeholder = st.empty()

            with st.spinner("Thinking..."):
                r = requests.post(
                    "https://server.iac.ac.il/api/v1/studentapi/responses",
                    json=payload,
                    headers=headers
                )

            data = r.json()
            print("Quota status:", data.get("iac_quota_status"))

            # Save response ID for the next request
            st.session_state.previous_response_id = data.get("id")

            try:
                answer = None

                # Find the assistant message safely
                for item in data.get("output", []):
                    if item.get("type") == "message":
                        for content_item in item.get("content", []):
                            if content_item.get("type") == "output_text":
                                answer = content_item.get("text")
                                break
                        if answer:
                            break

                if answer and answer.strip():
                    response_placeholder.markdown(answer)
                else:
                    answer = "Error reading response"
                    response_placeholder.markdown(answer)
                    st.json(data)

            except Exception:
                answer = "Error reading response"
                response_placeholder.markdown(answer)
                st.json(data)

        # Save assistant message for UI display
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })