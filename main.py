import sys
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

from config import SYSTEM_PROMPT
from availabe_functions import available_functions
from call_function import call_function


def main():
    load_dotenv()

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

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt = " ".join(args)

    if verbose:
        print(f"User prompt: {user_prompt}\n")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    try:
        for x in range(0, 20):
            response = generate_content(client, messages, verbose)
            if response != None and response.text:
                print(f"response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")


def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], #what fn to use
            system_instruction=SYSTEM_PROMPT), #SP > up
    )
    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)
    print("Response:")

    for candidate in response.candidates:
        messages.append(candidate.content)

    if response.candidates[0].content.parts[0].function_call: #accessing fn_call
        function_call = response.candidates[0].content.parts[0].function_call
        # print(f"Calling function: {function_call.name}({function_call.args})")
        function_call_result = call_function(function_call) #calling the fn

        function_response = []

        if not function_call_result.parts[0].function_response.response:
            raise Exception("No fn_response")
        
        if function_call_result.parts[0].function_response.response and verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        else:
            print("No verbose")

        new_message = types.Content(role='user', parts=[types.Part(function_response=function_call_result.parts[0].function_response)])
                                    
        messages.append(new_message)
    else:
        print("No function call found in response")
        return response


if __name__ == "__main__":
    main()
