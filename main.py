import os
import sys
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python import schema_run_python
from functions.write_file import schema_write_file

from functions.config import system_prompt

from functions.call_function import call_function

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt", help="The prompt to process")  # required positional arg
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    if not args.prompt:
        parser.error('\nError: no prompt provided.\nPlease provide a prompt.\n\nPrompt format: uv run main.py "<PROMPT>"\n')
        sys.exit(1)

    user_prompt = args.prompt
    printer = []

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python,
            schema_write_file
        ]
    )

    for i in range(20):
        try:
            response = client.models.generate_content(
                model='gemini-2.0-flash-001',
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions],
                    system_instruction=system_prompt)
            )
            for candidate in response.candidates:
                messages.append(candidate.content)

            function_calls = response.function_calls or []
            for fc in function_calls:
                # Call the function
                fc_result = call_function(
                    types.FunctionCall(
                        name=fc.name,
                        args=fc.args
                    )
                )
                messages.append(types.Content(
                    role="user",
                    parts=fc_result.parts
                    )
                )
                if not fc_result.parts[0].function_response.response:
                    raise ValueError("Error: No function response returned.")
                else:
                    if args.verbose:
                        print(f"-> {fc_result.parts[0].function_response.response}")

            if response.text and not function_calls:
                print("\n")
                print(response.text)
                print("\n")
                break
        except Exception as e:
            print(f"EXCEPTION: {e}")
            return (f"Error: {e}")

    if args.verbose:
        prompt_tokens = response.usage_metadata.prompt_token_count
        response_tokens = response.usage_metadata.candidates_token_count
        printer.append(f"User prompt: {user_prompt}")
        printer.append(f"Prompt tokens: {prompt_tokens}")
        printer.append(f"Response tokens: {response_tokens}")

    for piece in printer:
        print(piece)

if __name__ == "__main__":
    main()
