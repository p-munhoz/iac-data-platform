import os

import boto3
import pandas as pd

s3 = boto3.client(
    's3',
    endpoint_url=os.environ.get("MINIO_ENDPOINT", "http://minio:9000"),
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID", "admin"),
    aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY", "password"),
    region_name="us-east-1"
)

# Download file from Minio
s3.download_file("demo-bucket", "sample.csv", "downloaded.csv")

# Transform with pandas
df = pd.read_csv("downloaded.csv")
df["age_plus_10"] = df["age"] + 10

# Save transformed file
df.to_csv("transformed.csv", index=False)

# Upload back to Minio
s3.upload_file("transformed.csv", "demo-bucket", "transformed.csv")

print("ETL Complete")
