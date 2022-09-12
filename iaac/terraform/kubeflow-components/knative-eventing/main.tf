module "helm_addon" {
  source            = "github.com/aws-ia/terraform-aws-eks-blueprints/modules/kubernetes-addons/helm-addon"
  manage_via_gitops = var.manage_via_gitops
  helm_config       = local.helm_config
  addon_context     = var.addon_context
}
