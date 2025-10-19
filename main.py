import os, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import SYSTEM_PROMPT

def main():

    # Load environment variables from .env file
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    # pull prompt from command line argument, assign prompt to user messages, set model, and generate content
    if len(sys.argv) < 2:
        raise ValueError("Please provide content as a command line argument.")
    else:
        user_prompt = sys.argv[1]
    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)]),]
    response = client.models.generate_content(
        model = "gemini-2.0-flash-001", 
        contents = messages, 
        config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
        )

    # Check for verbose flag in command line arguments. If present print user prompt and token counts.
    if "--verbose" in sys.argv:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        print(response.text)
    else:
        print(response.text)

if __name__ == "__main__":
    main()
