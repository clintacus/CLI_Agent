import sys
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

from config import SYSTEM_PROMPT
from config import MAX_ITERS
from functions.call_function import call_function, available_functions


def main():
    # Load environment variables from .env file
    load_dotenv()

    # Check for verbose flag and collect user prompt
    verbose = "--verbose" in sys.argv
    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I fix the calculator?"')
        sys.exit(1)

    # Get Gemini API key from environment variables
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    # Combine all args into a single user prompt
    user_prompt = " ".join(args)

    # If verbose, print the user prompt
    if verbose:
        print(f"User prompt: {user_prompt}\n")

    # Prepare messages for the model
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    
    # Iteratively call the model until a final response is obtained
    iters = 0
    while True:
        iters += 1
        if iters > MAX_ITERS:
            print(f"Maximum iterations ({MAX_ITERS}) reached.")
            sys.exit(1)

        try:
            final_response = generate_content(client, messages, verbose)
            if final_response:
                print("Final response:")
                print(final_response)
                break
        except Exception as e:
            print(f"Error in generate_content: {e}")


def generate_content(client, messages, verbose):
    # Call the model with the user prompt and available functions
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=SYSTEM_PROMPT
        ),
    )
    # If verbose, print token usage
    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    # Append all candidate contents to messages for context
    if response.candidates:
        for candidate in response.candidates:
            function_call_content = candidate.content
            messages.append(function_call_content)


     # If there are no function calls, just print the text response
    if not response.function_calls:
        return response.text

    # Process each function call
    function_responses = []
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose)
        if (
            not function_call_result.parts
            or not function_call_result.parts[0].function_response
        ):
            raise Exception("empty function call result")
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        function_responses.append(function_call_result.parts[0])

    # Error if no function responses were generated
    if not function_responses:
        raise Exception("no function responses generated, exiting.")

    # Append function responses to messages for the next iteration
    messages.append(types.Content(role="user", parts=function_responses))

if __name__ == "__main__":
    main()
