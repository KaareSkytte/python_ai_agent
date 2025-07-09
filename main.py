import os
from dotenv import load_dotenv
from google import genai
import sys
from google.genai import types

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    verbose = "--verbose" in sys.argv
    userInput = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    if not userInput:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I build a calculator app?"')
        sys.exit(1)

    prompt = " ".join(userInput)

    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)])
    ]    

    if verbose:
        generate_content_verbose(client, messages)
        return

    generate_content(client, messages)

def generate_content(client, messages):
    response = client.models.generate_content(
        model='gemini-2.0-flash-001', 
        contents=messages
    )
    print("Response:")
    print(response.text)

def generate_content_verbose(client, messages):
    print(f"User prompt: {messages[0].parts[0].text}")

    response = client.models.generate_content(
        model='gemini-2.0-flash-001', 
        contents=messages
    )

    print("Response:")
    print(response.text)

    prompt_tokens_used = response.usage_metadata.prompt_token_count
    response_tokens_used = response.usage_metadata.candidates_token_count
    
    print(f"Prompt tokens: {prompt_tokens_used}")
    print(f"Response tokens: {response_tokens_used}")

if __name__ == "__main__":
    main()
