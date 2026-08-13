import os
import json
from datetime import datetime

import boto3
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
BUCKET_NAME = os.getenv("S3_BUCKET")


def upload_json_to_s3(data):
    """
    Upload transformed cricket data to S3 in NDJSON format.
    One JSON object per line (Redshift friendly).
    """

    s3 = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=AWS_REGION,
    )

    now = datetime.now()

    file_name = (
        f"cricket-data/"
        f"year={now.year}/"
        f"month={now.strftime('%m')}/"
        f"day={now.strftime('%d')}/"
        f"hour={now.strftime('%H')}/"
        f"matches_{now.strftime('%Y%m%d_%H%M%S')}.json"
    )

    print("Bucket:", BUCKET_NAME)
    print("Region:", AWS_REGION)

    # Convert list of dictionaries to NDJSON
    ndjson_data = "\n".join(
        json.dumps(record, default=str)
        for record in data
    )

    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=file_name,
        Body=ndjson_data,
        ContentType="application/json",
    )

    print(f"✅ Uploaded Successfully: {file_name}")

    return file_name