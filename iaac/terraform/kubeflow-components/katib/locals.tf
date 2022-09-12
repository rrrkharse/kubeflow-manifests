locals {
  name = "katib"

  default_helm_config = {
    name        = local.name
    chart       = "/Users/rkharse/kf/jim-helm/kubeflow-manifests/deployments/vanilla/helm/katib"
    # repository  = "https://github.com/jsitu777/kubeflow-manifests"
    version     = "0.1.0"
    namespace   = "default"
    description = "todo replace"
    values      = []
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
