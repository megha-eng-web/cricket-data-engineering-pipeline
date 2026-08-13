from scripts.fetch_cricket_data import fetch_cricket_data
from scripts.update_google_sheet import update_google_sheet

print("Fetching cricket data...")

data = fetch_cricket_data()

print("Updating Google Sheet...")

update_google_sheet(data)

print("Done!")