# AI Chatbot Project

Simple AI chatbot application with basic chat and advanced agent mode with web search.

## Description

This project is an AI chatbot built with Python and Streamlit.
It connects to the IAC Student API (GPT-5-Nano model) and supports two modes:
1. **Simple Chat (Chat Completions)** – basic question and answer 
2. **Agent Mode (Responses API)** – advanced interaction with web search and context awareness

Context is managed using `previous_response_id`, as supported by the API, allowing the system to maintain conversation flow without sending the full history each time.

The application also monitors token usage using `iac_quota_status` to help prevent exceeding API limits.

## Getting Started

### Dependencies

* Python 3.10 or higher  
* pip (Python package manager)  
* Internet connection
* Access to the IAC Student API (API key required)

Libraries used:
* streamlit  
* requests  
* python-dotenv  

### Installing

1. Clone the repository from GitHub
   ```
   git clone https://github.com/beni-il/chatbot-project.git
   cd chatbot-project
   ```

2. Install required libraries  
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file and add your API key  

   ```
   API_KEY=your_api_key
   ```

Important:
Make sure the `.env` file is included in `.gitignore` and never uploaded to GitHub.

### Executing program

1. Run the application  

   ```
   streamlit run app.py
   ```

2. Steps:
  * Select a mode (Simple Chat or Agent)  
  * Enter a message  
  * Click "Send"  
  * View the response  

## Help

Common issues and solutions:

- Make sure the `.env` file exists and contains a valid API key  
- Check that all required libraries are installed  
- Verify that you are connected to the internet  
- If the app does not start, try running the command again:
   ```
   streamlit run app.py
   ```


streamlit run app.py


## Authors

Beni J, Noam K

## Version History

## Version History

- Initial chatbot implementation (Simple Chat mode)  
- Added Agent mode with context using previous_response_id  
- Implemented Streamlit user interface  
- Improved user experience by adding a loading spinner

## License

This project is for academic use only.

## Acknowledgments

* IAC Student API
* Streamlit documentation
* Python community resources