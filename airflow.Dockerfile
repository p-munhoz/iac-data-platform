FROM apache/airflow:2.9.1

USER airflow

# Install both boto3 (S3 access) and duckdb (local warehouse)
RUN pip install --no-cache-dir boto3 duckdb