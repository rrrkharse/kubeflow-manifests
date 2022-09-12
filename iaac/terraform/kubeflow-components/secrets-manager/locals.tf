locals {
  name = "secrets-manager"

  set_values = [
    {
      name = "rds.secretName",
      value = var.rds_secret
    },
    {
      name = "s3.secretName",
      value = var.s3_secret
    }
  ]

  default_helm_config = {
    name        = local.name
    chart       = "/Users/rkharse/kf/jim-helm/kubeflow-manifests/deployments/vanilla/helm/secrets-manager"
    # repository  = "https://github.com/jsitu777/kubeflow-manifests"
    version     = "0.1.0"
    namespace   = "default"
    description = "todo replace"
    values      = []
    set         = local.set_values
    timeout     = "240"
  }

  helm_config = merge(
    local.default_helm_config,
    var.helm_config
  )

  argocd_gitops_config = {
    enable = true
  }
}
