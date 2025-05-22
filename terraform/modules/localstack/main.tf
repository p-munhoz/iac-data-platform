resource "docker_image" "localstack" {
  name = "localstack/localstack"
}

resource "docker_container" "localstack" {
  name  = var.container_name
  image = docker_image.localstack.name

  env = [
    "SERVICES=sqs",
    "EDGE_PORT=4566",
    "AWS_ACCESS_KEY_ID=test",
    "AWS_SECRET_ACCESS_KEY=test",
    "DEFAULT_REGION=us-east-1"
  ]

  ports {
    internal = 4566
    external = 4566
  }

  restart = "always"

  networks_advanced {
    name    = "data_platform_net"
    aliases = ["localstack"]
  }
}
