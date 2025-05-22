terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0.1"
    }
  }

  required_version = ">= 1.5.0"
}

provider "docker" {}

resource "docker_network" "data_platform" {
  name = "data_platform_net"
}

module "minio" {
  source         = "./modules/minio"
  container_name = "minio-from-tf"
  minio_user     = "admin"
  minio_password = "password"
  host_data_path = "/tmp/minio-data"

  providers = {
    docker = docker
  }
}

module "airflow" {
  source           = "./modules/airflow"
  container_name   = "airflow-from-tf"
  image_name       = "airflow-custom"
  context          = "${path.module}/../"
  dockerfile       = "airflow.Dockerfile"
  executor         = "SequentialExecutor"
  sql_alchemy_conn = "sqlite:////opt/airflow/airflow.db"
  host_dags_path   = "${path.cwd}/../dags"
  host_data_path   = "${path.cwd}/../data"

  providers = {
    docker = docker
  }
}

module "localstack" {
  source         = "./modules/localstack"
  container_name = "localstack"

  providers = {
    docker = docker
  }
}