module "helm_addon_1" {
  source            = "github.com/aws-ia/terraform-aws-eks-blueprints//modules/kubernetes-addons/helm-addon?ref=v4.9.0"
  helm_config       = local.helm_config_1
  addon_context     = var.addon_context
}

module "helm_addon_2" {
  source            = "github.com/aws-ia/terraform-aws-eks-blueprints//modules/kubernetes-addons/helm-addon?ref=v4.9.0"
  helm_config       = local.helm_config_2
  addon_context     = var.addon_context

  depends_on = [module.helm_addon_1]
}

# Wait 30 seconds after helm chart deployment
resource "time_sleep" "wait_30_seconds" {
  create_duration = "30s"
  destroy_duration = "30s"

  depends_on = [module.helm_addon_2]
}

resource "null_resource" "next" {
  depends_on = [time_sleep.wait_30_seconds]
}