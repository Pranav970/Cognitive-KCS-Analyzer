OPENAI_API_KEY="your_openai_api_key_here"

import os
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

API_KEY = os.getenv("OPENAI_API_KEY")

if not API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables. Please set it in a .env file.")

# You can add other configurations here if needed
LLM_MODEL = "gpt-3.5-turbo-instruct" # Or "gpt-3.5-turbo" for chat models, "text-davinci-003" (legacy)
# If using gpt-3.5-turbo or gpt-4, the API call structure is different (chat completions)
# For simplicity, text-davinci-003 or gpt-3.5-turbo-instruct are easier for direct completion prompts.
# If you use chat models like "gpt-3.5-turbo", llm_interactions.py needs to be adapted.
