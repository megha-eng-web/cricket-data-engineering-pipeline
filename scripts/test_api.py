from dotenv import load_dotenv
import os
import requests
import json


# Load environment variables
load_dotenv()


# Get API key from .env
API_KEY = os.getenv("CRICKET_API_KEY")


# Check API key loaded
if not API_KEY:
    print("❌ API Key not found. Check your .env file")
    exit()


# Series ID
series_id = "47b54677-34de-4378-9019-154e82b9cc1a"


# API URL
url = f"https://api.cricapi.com/v1/series_info?apikey={API_KEY}&offset=0&id={series_id}"


# API Request
response = requests.get(url)


# Status
print("Status Code:", response.status_code)


# Convert response to JSON
data = response.json()


# Print response
print(json.dumps(data, indent=4))


# Optional: Save response for checking
with open("series_info_response.json", "w") as file:
    json.dump(data, file, indent=4)


print("\n✅ API data saved as series_info_response.json")