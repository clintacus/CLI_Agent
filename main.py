import os, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import SYSTEM_PROMPT
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.write_file import write_file, schema_write_file
from functions.run_python_file import run_python_file, schema_run_python_file

def main():

    # Load environment variables from .env file
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    
    # Define available functions for the agent
    available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file,
    ]
)

    # pull prompt from command line argument, assign prompt to user messages, set model, and generate content
    if len(sys.argv) < 2:
        raise ValueError("Please provide content as a command line argument.")
    else:
        user_prompt = sys.argv[1]
    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)]),]
    response = client.models.generate_content(
        model = "gemini-2.0-flash-001", 
        contents = messages, 
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=SYSTEM_PROMPT),)

    # Check for verbose flag in command line arguments. If present print user prompt and token counts.
    if "--verbose" in sys.argv:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    # If no function calls were made, print the response text
    if not response.function_calls:
        return response.text

    # If function calls were made, print the function call details
    for function_call_part in response.function_calls:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")

if __name__ == "__main__":
    main()
