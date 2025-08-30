#!/home/user1/workspace/github.com/defau1tuser0/ai_agent/.venv/bin/python3
import os
import sys
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

if len(sys.argv) > 1:
    user_prompt = sys.argv[1]

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]
    
    response = client.models.generate_content(
        model="gemini-2.0-flash-001", contents=messages
    )
    
    print(response.text)

    try: 
        if sys.argv[2] and sys.argv[2] == "--verbose":
            print(f"User prompt: {user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    except Exception as e:
        pass
   
else:
    print("No prompt given")
    sys.exit(1)
