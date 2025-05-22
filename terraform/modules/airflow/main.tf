resource "docker_image" "airflow" {
  name = var.image_name

  build {
    context    = var.context
    dockerfile = var.dockerfile
  }
}

resource "docker_volume" "airflow_dags" {
  name = "airflow-dags"
}

resource "docker_container" "airflow" {
  name  = var.container_name
  image = docker_image.airflow.name

  networks_advanced {
    name    = "data_platform_net"
    aliases = ["airflow"]
  }


  ports {
    internal = 8080
    external = 8080
  }

  env = [
    "AIRFLOW__CORE__EXECUTOR=${var.executor}",
  "AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=${var.sql_alchemy_conn}"]


  command = [
    "bash", "-c",
    "airflow db init && airflow users create --username admin --firstname Admin --lastname User --role Admin --email admin@example.com --password admin && airflow scheduler & airflow webserver -p 8080"
  ]


  volumes {
    container_path = "/opt/airflow/dags"
    host_path      = var.host_dags_path
  }
  volumes {
    container_path = "/var/run/docker.sock"
    host_path      = "/var/run/docker.sock"
  }

  volumes {
    container_path = "/opt/airflow/data"
    host_path      = var.host_data_path
  }

  restart = "always"
}