from dotenv import load_dotenv
import os
import requests
import json

# Load environment variables from .env
load_dotenv()

# Read API key from .env
API_KEY = os.getenv("CRICKET_API_KEY")

# API Endpoint
url = f"https://api.cricapi.com/v1/series?apikey={API_KEY}&offset=0"

# Send request
response = requests.get(url)

print("Status Code:", response.status_code)

# Convert response to JSON
data = response.json()

# Print formatted JSON
print(json.dumps(data, indent=4))
