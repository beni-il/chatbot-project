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

st.set_page_config(page_title="AI Chatbot", page_icon="🤖")

st.title("🤖 AI Chatbot")

# Mode selection
mode = st.radio("Choose mode:", ["Simple Chat", "Agent"])

# Session state for context (IMPORTANT for Agent)
if "previous_response_id" not in st.session_state:
    st.session_state.previous_response_id = None

# Input box
user_input = st.text_input("You:")

# Send button
if st.button("Send"):

    if user_input.strip():

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

            r = requests.post(
                "https://server.iac.ac.il/api/v1/studentapi/chat/completions",
                json=payload,
                headers=headers
            )

            data = r.json()

            try:
                answer = data["choices"][0]["message"]["content"]
                st.write(answer if answer else "No response text")
            except:
                st.write(data)

        # ----------------------------
        # Agent (WITH previous_response_id)
        # ----------------------------
        else:

            payload = {
                "reasoning": {"effort": "low"},
                "instructions": "Give a short answer up to 50 words only.",
                "input": user_input,
                "tools": [{"type": "web_search"}]
            }

            if st.session_state.previous_response_id is not None:
                payload["previous_response_id"] = st.session_state.previous_response_id

            r = requests.post(
                "https://server.iac.ac.il/api/v1/studentapi/responses",
                json=payload,
                headers=headers
            )

            data = r.json()

            # Save ID for next message
            st.session_state.previous_response_id = data.get("id")

            try:
                answer = data["output"][1]["content"][0]["text"]
                st.write(answer)
            except:
                st.write(data)

    else:
        st.warning("Please enter a message")