import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("AKASH_API_KEY")
github_token = os.getenv("GITHUB_TOKEN")

print(f"API Key: {api_key}")
print(f"GitHub Token: {github_token}")