import sys
from datetime import datetime, timedelta

sys.path.append("/opt/airflow/scripts")
sys.path.append("/opt/airflow/dags")

from airflow import DAG
from airflow.operators.python import PythonOperator

from fetch_cricket_data import fetch_cricket_data
from transform_cricket_data import transform_cricket_data
from upload_to_s3 import upload_json_to_s3
from update_google_sheet import update_google_sheet
from load_to_redshift import load_to_redshift


default_args = {
    "owner": "babita",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


# ------------------------------------------------------------
# Task 1: Fetch cricket data
# ------------------------------------------------------------

def fetch_task(**context):

    data = fetch_cricket_data()

    context["ti"].xcom_push(
        key="cricket_data",
        value=data
    )


# ------------------------------------------------------------
# Task 2: Transform + Upload to S3
# ------------------------------------------------------------

def upload_s3_task(**context):

    raw_data = context["ti"].xcom_pull(
        task_ids="fetch_live_data",
        key="cricket_data"
    )

    transformed_data = transform_cricket_data(raw_data)

    s3_key = upload_json_to_s3(transformed_data)

    # Pass the uploaded S3 file path to the next task
    context["ti"].xcom_push(
        key="s3_key",
        value=s3_key
    )


# ------------------------------------------------------------
# Task 3: Load S3 data into Redshift
# ------------------------------------------------------------

def redshift_task(**context):

    s3_key = context["ti"].xcom_pull(
        task_ids="upload_to_s3",
        key="s3_key"
    )

    if not s3_key:
        raise ValueError("S3 key was not found in XCom.")

    print(f"Loading S3 file into Redshift: {s3_key}")

    load_to_redshift(s3_key)


# ------------------------------------------------------------
# Task 4: Update Google Sheet
# ------------------------------------------------------------

def update_sheet_task(**context):

    raw_data = context["ti"].xcom_pull(
        task_ids="fetch_live_data",
        key="cricket_data"
    )

    update_google_sheet(raw_data)


# ------------------------------------------------------------
# DAG
# ------------------------------------------------------------

with DAG(
    dag_id="cricket_etl_pipeline",
    default_args=default_args,
    description="Automated hourly Cricket Data Engineering Pipeline",
    start_date=datetime(2026, 7, 21),
    schedule="@hourly",
    catchup=False,
) as dag:

    fetch_live_data = PythonOperator(
        task_id="fetch_live_data",
        python_callable=fetch_task,
    )

    upload_to_s3 = PythonOperator(
        task_id="upload_to_s3",
        python_callable=upload_s3_task,
    )

    load_redshift = PythonOperator(
        task_id="load_to_redshift",
        python_callable=redshift_task,
    )

    update_google_sheet_task = PythonOperator(
        task_id="update_google_sheet",
        python_callable=update_sheet_task,
    )


    # --------------------------------------------------------
    # Pipeline dependencies
    # --------------------------------------------------------

    fetch_live_data >> upload_to_s3

    upload_to_s3 >> load_redshift

    fetch_live_data >> update_google_sheet_task
    