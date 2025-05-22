# 🧪 IaC Data Platform (Local + Free)

This project is a **mock data platform** built entirely with **Terraform and Docker**, designed to emulate a modern cloud data stack **locally and for free**.

It showcases core data engineering skills: infrastructure as code, orchestration, storage, event-driven compute, and transformations.

This repository contains the example code and documentation referenced in the article [Building a Local Data Platform with Terraform and Docker](https://p-munhoz.github.io/blog/building-local-data-platform-terraform-docker)

---

## 📦 Tech Stack

| Component      | Tool/Service        | Emulated with         |
| -------------- | ------------------- | --------------------- |
| Object Storage | AWS S3              | Minio                 |
| Compute (ETL)  | AWS Lambda          | Docker + BashOperator |
| Orchestration  | MWAA / Airflow      | Dockerized Airflow    |
| Message Queue  | SQS/SNS             | LocalStack            |
| Data Warehouse | Redshift / BigQuery | DuckDB                |
| IaC Tool       | Terraform           | Local                 |

---

## 🗺 Architecture Overview

```
User / DAG Trigger
   |
   v
Airflow DAG
   |
   |--> Upload CSV to Minio
   |--> Load raw CSV to DuckDB
   |--> [Triggered via SQS] Run Docker ETL
   |--> Load transformed data to DuckDB
```

* **Airflow** orchestrates tasks
* **Minio** simulates S3 object storage
* **ETL step** is a Docker container simulating Lambda
* **DuckDB** acts as the local data warehouse
* **LocalStack** provides SQS queue to trigger the ETL

---

## 🚀 How to Run the Project

### 1. Clone the Repo

```bash
git clone https://github.com/YOUR_USERNAME/iac-data-platform.git
cd iac-data-platform
```

### 2. Apply Terraform Infrastructure

```bash
cd terraform
terraform init
terraform apply
```

### 3. Access Airflow

Visit [http://localhost:8080](http://localhost:8080)
Login: `admin` / `admin`

### 4. Create the SQS Queue (once)

```bash
AWS_ACCESS_KEY_ID=test \
AWS_SECRET_ACCESS_KEY=test \
aws --endpoint-url=http://localhost:4566 \
    sqs create-queue \
    --queue-name my-etl-queue \
    --region us-east-1
```

### 5. Upload a Message to SQS

```bash
AWS_ACCESS_KEY_ID=test \
AWS_SECRET_ACCESS_KEY=test \
aws --endpoint-url=http://localhost:4566 \
     sqs send-message \
     --queue-url http://localhost:4566/000000000000/my-etl-queue \
     --message-body "trigger"
```

---

## 📁 Project Structure

```
iac-data-platform/
├── terraform/              # Infra provisioning
│   ├── modules/            # Minio, Airflow, LocalStack
├── dags/                   # Airflow DAGs
├── scripts/                # ETL transformation logic
├── data/                   # CSV files and DuckDB storage
├── airflow.Dockerfile      # Custom Airflow image
├── scripts/Dockerfile.etl  # ETL image
└── README.md
```

---

## ✨ What This Project Demonstrates

* 📦 Infrastructure-as-Code with Terraform modules
* 🧩 Airflow DAGs connected to Dockerized transformations
* 🔁 Event-driven execution via SQS (LocalStack)
* 🛠 Realistic dev environment with local S3 + DuckDB
* ⚙️ Simulated Lambda compute via `docker run`

---

## 🧠 Ideas to Extend It

* Use GitHub Actions to test provisioning on every commit
* Add unit tests for transformation logic
* Add Prometheus + Grafana for basic monitoring
* Support streaming (Kafka or Kinesis with LocalStack)

---

## 📜 License

MIT License — free to use, fork, adapt, and learn!
