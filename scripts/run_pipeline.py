from fetch_cricket_data import fetch_cricket_data
from upload_to_s3 import upload_json_to_s3
from update_google_sheet import update_google_sheet


def main():
    print("Fetching cricket data...")

    data = fetch_cricket_data()

    print("Uploading data to S3...")
    upload_json_to_s3(data)

    print("Updating Google Sheet...")
    update_google_sheet(data)

    print("Pipeline completed successfully!")


if __name__ == "__main__":
    main()