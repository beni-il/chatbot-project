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
    previous_response_id = None

    while True:
        prompt = input("You: ")

        if prompt == "exit":
            break

        payload = {
            "reasoning": {"effort": "low"},
            "instructions": "Give a short answer up to 50 words only.",
            "input": prompt,
            "tools": [{"type": "web_search"}]
        }

        # Add context only if this is not the first request
        if previous_response_id is not None:
            payload["previous_response_id"] = previous_response_id

        r = requests.post(
            "https://server.iac.ac.il/api/v1/studentapi/responses",
            json=payload,
            headers=headers
        )

        data = r.json()
        print(data)

        # Save the response ID for the next request
        previous_response_id = data.get("id")

    print("End of chat")

else:
    print("Invalid choice")