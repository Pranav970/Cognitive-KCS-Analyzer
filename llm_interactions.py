import openai
from config import API_KEY, LLM_MODEL
# from tenacity import retry, stop_after_attempt, wait_random_exponential # For robust API calls

# Initialize OpenAI client (latest SDK version)
client = openai.OpenAI(api_key=API_KEY)

# @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def get_llm_completion(prompt_text, model=LLM_MODEL, max_tokens=1000, temperature=0.3):
    """
    Gets a completion from the specified OpenAI LLM model.
    Uses the newer openai.completions.create for models like gpt-3.5-turbo-instruct
    or openai.chat.completions.create for models like gpt-3.5-turbo or gpt-4.
    """
    try:
        # Check if it's a chat model (this is a simplification, model naming can be more complex)
        if "gpt-3.5-turbo" == model or "gpt-4" in model and "instruct" not in model : # it's a chat model
             if model == "gpt-3.5-turbo-instruct": # this is a completion model despite the name.
                response = client.completions.create(
                    model=model,
                    prompt=prompt_text,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    # top_p=1,
                    # frequency_penalty=0,
                    # presence_penalty=0
                )
                return response.choices[0].text.strip()
             else: # it's a chat model
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": prompt_text}
                    ],
                    max_tokens=max_tokens,
                    temperature=temperature
                )
                return response.choices[0].message.content.strip()
        else: # It's a completion model like text-davinci-003 or gpt-3.5-turbo-instruct
            response = client.completions.create(
                model=model,
                prompt=prompt_text,
                max_tokens=max_tokens,
                temperature=temperature,
                # top_p=1,
                # frequency_penalty=0,
                # presence_penalty=0
            )
            return response.choices[0].text.strip()

    except openai.APIError as e:
        print(f"OpenAI API Error: {e}")
        return f"Error: Could not get response from LLM. API Error: {str(e)}"
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return f"Error: Could not get response from LLM. Unexpected error: {str(e)}"

if __name__ == '__main__':
    # Test the function (requires your .env file and API key)
    # Ensure config.py correctly loads your API_KEY
    if API_KEY and API_KEY != "your_openai_api_key_here":
        test_prompt = "Explain what a Large Language Model is in one sentence."
        print(f"Testing LLM with model: {LLM_MODEL}")
        explanation = get_llm_completion(test_prompt, model=LLM_MODEL, max_tokens=150)
        print("LLM Response:")
        print(explanation)

        # Test with a chat model if you have one configured, e.g., gpt-3.5-turbo
        # chat_model_name = "gpt-3.5-turbo" # or "gpt-4"
        # print(f"\nTesting LLM with chat model: {chat_model_name}")
        # explanation_chat = get_llm_completion(test_prompt, model=chat_model_name, max_tokens=150)
        # print("LLM Chat Response:")
        # print(explanation_chat)
    else:
        print("Skipping LLM test as API_KEY is not configured or is placeholder.")
        print("Please set your OPENAI_API_KEY in a .env file.")
