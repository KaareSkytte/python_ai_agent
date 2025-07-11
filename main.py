import os
from dotenv import load_dotenv
from google import genai
import sys
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python import schema_run_python_file
from functions.write_file import schema_write_file

available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
        ]
    )   

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

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
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
    )
    
    if len(response.function_calls) != 0:
        print(f"Calling function: {response.function_calls[0].name}({response.function_calls[0].args})")

    else:
        print("Response:")
        print(response.text)

def generate_content_verbose(client, messages):
    print(f"User prompt: {messages[0].parts[0].text}")

    response = client.models.generate_content(
        model='gemini-2.0-flash-001', 
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
    )
    
    if len(response.function_calls) != 0:
        print(f"Calling function: {response.function_calls[0].name}({response.function_calls[0].args})")

    else:
        print("Response:")
        print(response.text)

    prompt_tokens_used = response.usage_metadata.prompt_token_count
    response_tokens_used = response.usage_metadata.candidates_token_count
    
    print(f"Prompt tokens: {prompt_tokens_used}")
    print(f"Response tokens: {response_tokens_used}")

if __name__ == "__main__":
    main()
