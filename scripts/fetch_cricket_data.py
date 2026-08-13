import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def fetch_cricket_data():
    """
    Fetch live cricket match data from CricAPI.
    """

    API_KEY = os.getenv("CRICKET_API_KEY")

    if not API_KEY:
        raise ValueError("CRICKET_API_KEY not found in .env")

    url = "https://api.cricapi.com/v1/matches"

    params = {
        "apikey": API_KEY,
        "offset": 0
    }

    try:
        response = requests.get(url, params=params, timeout=30)

        print("API Status:", response.status_code)

        response.raise_for_status()

        data = response.json()

        if data.get("status") != "success":
            raise Exception(f"CricAPI Error: {data}")

        matches = data.get("data", [])

        print(f"✅ Live Matches Retrieved: {len(matches)}")

        return data

    except requests.exceptions.RequestException as e:
        print("❌ API Request Failed")
        raise e


if __name__ == "__main__":

    data = fetch_cricket_data()

    matches = data.get("data", [])

    print("\n========== LIVE MATCH SUMMARY ==========")
    print(f"Total Matches : {len(matches)}")

    if matches:

        first_match = matches[0]

        print("First Match :", first_match.get("name"))
        print("Status      :", first_match.get("status"))
        print("Venue       :", first_match.get("venue"))
        print("Date        :", first_match.get("date"))

    print("========================================")