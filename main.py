import os
import sys
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

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

    response = client.models.generate_content(
        model='gemini-2.0-flash-001', contents=messages
    )

    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count

    if args.verbose:
        printer.append(f"User prompt: {user_prompt}")
        printer.append(f"Prompt tokens: {prompt_tokens}")
        printer.append(f"Response tokens: {response_tokens}")

    printer.insert(0, response.text)

    for piece in printer:
        print(piece)

if __name__ == "__main__":
    main()
