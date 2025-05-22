resource "docker_image" "minio" {
  name = "minio/minio"
}


resource "docker_container" "minio" {
  image = docker_image.minio.name
  name  = var.container_name

  networks_advanced {
    name    = "data_platform_net"
    aliases = ["minio"]
  }


  ports {
    internal = 9000
    external = 9000
  }

  ports {
    internal = 9001
    external = 9001
  }

  env = [
    "MINIO_ROOT_USER=${var.minio_user}",
    "MINIO_ROOT_PASSWORD=${var.minio_password}"
  ]

  command = ["server", "/data", "--console-address", ":9001"]

  volumes {
    container_path = "/data"
    host_path      = var.host_data_path
  }
}