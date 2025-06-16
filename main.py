import os, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

if len(sys.argv) <= 1:
    print("Error: expecting text argument")
    exit(1)

genai_content = sys.argv[1]

messages = [
    types.Content(role="user", parts=[types.Part(text=genai_content)]),
]
response = client.models.generate_content(model='gemini-2.0-flash-001', contents=messages)
print(response.text)

if (len(sys.argv) >= 3):
    if (sys.argv[2] == "--verbose"):
        print(f'User prompt: {genai_content}')
        print(f'Prompt tokens: {response.usage_metadata.prompt_token_count}')
        print(f'Response tokens: {response.usage_metadata.candidates_token_count}')