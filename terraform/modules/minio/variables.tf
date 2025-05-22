variable "container_name" {
  type    = string
  default = "minio-from-tf"
}

variable "minio_user" {
  type    = string
  default = "admin"
}

variable "minio_password" {
  type    = string
  default = "password"
}

variable "host_data_path" {
  type    = string
  default = "/tmp/minio-data"
}
