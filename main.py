import os
import sys
from dotenv import load_dotenv
from google import genai

def main():
    if len(sys.argv) < 2:
        print('\nError: no prompt provided.\nPlease provide a prompt.\n\n'
            'Prompt format: uv run main.py "<PROMPT>"\n')
        sys.exit(1)

    prompt = sys.argv[1]

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model='gemini-2.0-flash-001', contents=prompt
    )

    print(response.text)
    print("Prompt tokens:", response.usage_metadata.prompt_token_count)
    print("Response tokens:", response.usage_metadata.candidates_token_count)

if __name__ == "__main__":
    main()
