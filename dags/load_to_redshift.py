import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

REDSHIFT_HOST = os.getenv("REDSHIFT_HOST")
REDSHIFT_PORT = os.getenv("REDSHIFT_PORT")
REDSHIFT_DATABASE = os.getenv("REDSHIFT_DATABASE")
REDSHIFT_USER = os.getenv("REDSHIFT_USER")
REDSHIFT_PASSWORD = os.getenv("REDSHIFT_PASSWORD")

S3_BUCKET = os.getenv("S3_BUCKET")
REDSHIFT_IAM_ROLE = os.getenv("REDSHIFT_IAM_ROLE")


def load_to_redshift(s3_key):
    """
    Load one NDJSON file from S3 into Amazon Redshift.
    """

    conn = None
    cur = None

    try:
        conn = psycopg2.connect(
            host=REDSHIFT_HOST,
            port=REDSHIFT_PORT,
            dbname=REDSHIFT_DATABASE,
            user=REDSHIFT_USER,
            password=REDSHIFT_PASSWORD,
        )

        cur = conn.cursor()

        copy_sql = f"""
        COPY public.cricket_matches
        FROM 's3://{S3_BUCKET}/{s3_key}'
        IAM_ROLE '{REDSHIFT_IAM_ROLE}'
        JSON 'auto'
        TIMEFORMAT 'auto';
        """

        print(copy_sql)

        cur.execute(copy_sql)

        conn.commit()

        print("✅ Data loaded into Redshift successfully.")

    except Exception as e:
        if conn:
            conn.rollback()

        print("❌ Redshift Load Failed")
        raise e

    finally:
        if cur:
            cur.close()

        if conn:
            conn.close()
            