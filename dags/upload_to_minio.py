from datetime import datetime

import boto3
import duckdb
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

MINIO_ENDPOINT = "http://minio:9000"
AWS_ACCESS_KEY = "admin"
AWS_SECRET_KEY = "password"
BUCKET_NAME = "demo-bucket"
CSV_FILE = "/opt/airflow/data/sample.csv"
DUCKDB_FILE = "/opt/airflow/data/warehouse.duckdb"


def upload_to_minio():
    s3 = boto3.client(
        "s3",
        endpoint_url=MINIO_ENDPOINT,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name="us-east-1",
    )

    if BUCKET_NAME not in [b["Name"] for b in s3.list_buckets()["Buckets"]]:
        s3.create_bucket(Bucket=BUCKET_NAME)

    s3.upload_file(CSV_FILE, BUCKET_NAME, "sample.csv")


def load_to_duckdb():
    # Download CSV from Minio
    s3 = boto3.client(
        "s3",
        endpoint_url=MINIO_ENDPOINT,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name="us-east-1",
    )
    local_csv = "/opt/airflow/data/temp_sample.csv"
    s3.download_file(BUCKET_NAME, "sample.csv", local_csv)

    # Load into DuckDB
    con = duckdb.connect(DUCKDB_FILE)
    con.execute("CREATE TABLE IF NOT EXISTS users AS SELECT * FROM read_csv_auto(?);", (local_csv,))
    con.close()

def load_transformed_to_duckdb():
    s3 = boto3.client(
        "s3",
        endpoint_url=MINIO_ENDPOINT,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name="us-east-1",
    )

    local_csv = "/opt/airflow/data/transformed.csv"
    s3.download_file(BUCKET_NAME, "transformed.csv", local_csv)

    con = duckdb.connect(DUCKDB_FILE)
    con.execute("CREATE OR REPLACE TABLE users_transformed AS SELECT * FROM read_csv_auto(?);", (local_csv,))
    con.close()

t4 = PythonOperator(
    task_id="load_transformed_to_duckdb",
    python_callable=load_transformed_to_duckdb,
)


with DAG(
    dag_id="upload_and_duckdb",
    start_date=datetime(2023, 1, 1),
    schedule_interval=None,
    catchup=False,
    is_paused_upon_creation=False,
    tags=["demo"]
) as dag:

    t1 = PythonOperator(
        task_id="upload_csv",
        python_callable=upload_to_minio,
    )

    t2 = PythonOperator(
        task_id="load_to_duckdb",
        python_callable=load_to_duckdb,
    )

    etl_task = BashOperator(
        task_id="etl_task",
        bash_command=(
            "docker run --rm "
            "-e MINIO_ENDPOINT=http://minio:9000 "
            "-e AWS_ACCESS_KEY_ID=admin "
            "-e AWS_SECRET_ACCESS_KEY=password "
            "--network data_platform_net "
            "etl-transform"
        ),
    )

    t4 = PythonOperator(
        task_id="load_transformed_to_duckdb",
        python_callable=load_transformed_to_duckdb,
    )

    t1 >> t2 >> etl_task >> t4
