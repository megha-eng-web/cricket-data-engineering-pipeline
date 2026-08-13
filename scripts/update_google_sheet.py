from dotenv import load_dotenv
import os
import gspread
from google.oauth2.service_account import Credentials

# Load environment variables
load_dotenv()

SHEET_ID = os.getenv("GOOGLE_SHEET_ID")

import platform

if platform.system() == "Windows":
    SERVICE_ACCOUNT_FILE = "creds/google_service_account.json"
else:
    SERVICE_ACCOUNT_FILE = "/opt/airflow/creds/google_service_account.json"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


def update_google_sheet(data):
    """
    Update Google Sheet with match data.
    """

    credentials = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=SCOPES
    )

    client = gspread.authorize(credentials)

    sheet = client.open_by_key(SHEET_ID).worksheet("Matches")

    rows = [[
        "Match ID",
        "Match Name",
        "Match Type",
        "Date",
        "Venue",
        "Status",
        "Team 1",
        "Team 2",
        "Match Started",
        "Match Ended"
    ]]

    matches = data.get("data", [])

    for match in matches:

        teams = match.get("teams", [])

        team1 = teams[0] if len(teams) > 0 else ""
        team2 = teams[1] if len(teams) > 1 else ""

        rows.append([
            match.get("id"),
            match.get("name"),
            match.get("matchType"),
            match.get("date"),
            match.get("venue"),
            match.get("status"),
            team1,
            team2,
            match.get("matchStarted"),
            match.get("matchEnded")
        ])

    sheet.clear()

    sheet.update("A1", rows)

    print(f"Google Sheet Updated Successfully ({len(matches)} matches)")