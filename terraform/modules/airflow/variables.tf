variable "container_name" {
  type    = string
  default = "airflow-from-tf"
}

variable "image_name" {
  type    = string
  default = "airflow-custom"
}

variable "executor" {
  type    = string
  default = "SequentialExecutor"
}

variable "sql_alchemy_conn" {
  type    = string
  default = "sqlite:////opt/airflow/airflow.db"
}

variable "host_dags_path" {
  type = string
}

variable "host_data_path" {
  type = string
}

variable "context" {
  type = string
}

variable "dockerfile" {
  type = string
}
