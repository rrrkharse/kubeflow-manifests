locals {
  name = "cluster-local-gateway"

  default_helm_config = {
    name        = local.name
    version     = "0.1.0"
    namespace   = "default"
    values      = []
    timeout     = "600"
  }

  helm_config = merge(
    local.default_helm_config,
    var.helm_config
  )

}
