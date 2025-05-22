import subprocess
from datetime import datetime

import boto3
from airflow import DAG
from airflow.operators.python import PythonOperator


def check_and_trigger_etl():
    sqs = boto3.client(
        "sqs",
        endpoint_url="http://localstack:4566",
        aws_access_key_id="test",
        aws_secret_access_key="test",
        region_name="us-east-1"
    )

    queue_url = sqs.get_queue_url(QueueName="my-etl-queue")["QueueUrl"]
    messages = sqs.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=1)

    if "Messages" in messages:
        print("Message received! Triggering ETL.")
        # Simulate Lambda call (run ETL container)
        subprocess.run([
            "docker", "run", "--rm",
            "-e", "MINIO_ENDPOINT=http://minio:9000",
            "-e", "AWS_ACCESS_KEY_ID=admin",
            "-e", "AWS_SECRET_ACCESS_KEY=password",
            "--network", "data_platform_net",
            "etl-transform"
        ])
        # Delete message from queue
        for msg in messages["Messages"]:
            sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=msg["ReceiptHandle"])
    else:
        print("No messages in queue.")

with DAG(
    dag_id="trigger_etl_from_sqs",
    start_date=datetime(2023, 1, 1),
    schedule_interval="@hourly",
    catchup=False,
    is_paused_upon_creation=False,
    tags=["demo"]
) as dag:

    t1 = PythonOperator(
        task_id="check_sqs_and_run_etl",
        python_callable=check_and_trigger_etl,
    )
