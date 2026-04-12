import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key securely
API_KEY = os.getenv("API_KEY")

# Check if API key exists
if not API_KEY:
    print("Error: API_KEY not found. Check your .env file.")
    exit()

# Ask the user which mode to use:
# 0 = Chat Completions
# 1 = Responses API
state = input("Please select 0 for simple chat or 1 for agent: ")

headers = {
    "Authorization": f"Bearer {API_KEY}"
}

if state == "0":
    while True:
        prompt = input("You: ")

        if prompt == "exit":
            break

        payload = {
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_completion_tokens": 500
        }

        r = requests.post(
            "https://server.iac.ac.il/api/v1/studentapi/chat/completions",
            json=payload,
            headers=headers
        )

        print(r.json())

    print("End of chat")

elif state == "1":
    conversation = []

    while True:
        prompt = input("You: ")

        if prompt == "exit":
            break

        conversation.append({
            "role": "user",
            "content": prompt
        })

        payload = {
            "reasoning": {"effort": "low"},
            "instructions": "Give a short answer up to 50 words only.",
            "input": conversation,
            "tools": [{"type": "web_search"}]
        }

        r = requests.post(
            "https://server.iac.ac.il/api/v1/studentapi/responses",
            json=payload,
            headers=headers
        )

        print(r.json())

        try:
            reply = r.json()["output_text"]
            conversation.append({
                "role": "assistant",
                "content": reply
            })
        except:
            pass

    print("End of chat")

else:
    print("Invalid choice")