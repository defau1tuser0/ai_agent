#!/home/user1/workspace/github.com/defau1tuser0/ai_agent/.venv/bin/python3
import os
import sys
from google import genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

if len(sys.argv) > 1:
	prompt = sys.argv[1] 
	print("---------")
	print(prompt)
	print("---------")
	response = client.models.generate_content(
    	model="gemini-2.0-flash-001", contents=prompt + " in short"
	)

	print(response.text)
	print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
	print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
else:
	print("No prompt given")
