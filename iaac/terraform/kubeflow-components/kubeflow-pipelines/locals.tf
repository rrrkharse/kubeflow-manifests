locals {
  name = "kubeflow-pipelines"

  set_values_map = {
    "rds.dbHost" = var.rds_db_host,
    "s3.bucketName" = var.s3_bucket_name,
    "s3.minioServiceRegion" = var.addon_context.aws_region_name
  }

  set_values = [for k,v in local.set_values_map : {name = k, value = v} if v != ""]

  default_helm_config = {
    name        = local.name
    chart_1       = "/Users/rkharse/kf/jim-helm/kubeflow-manifests/deployments/vanilla/helm/kubeflow-pipelines-copy"
    chart_2       = "/Users/rkharse/kf/jim-helm/kubeflow-manifests/deployments/vanilla/helm/kubeflow-pipelines-copy"
    version     = "0.1.0"
    namespace   = "default"
    description = "todo replace"
    values      = []
    timeout     = "240"
  }
  
  base_helm_config = merge(
    local.default_helm_config,
    var.helm_config,
    {
      set = concat(local.set_values, try(var.helm_config["set"], []))
    }
  )

  helm_config_1 = merge(
    local.base_helm_config,
    {
      name = "${local.name}-1"
      chart = local.base_helm_config["chart_1"]
    }
  )

  helm_config_2 = merge(
    local.base_helm_config,
    {
      name = "${local.name}-2"
      chart = local.base_helm_config["chart_2"]
    }
  )


  argocd_gitops_config = {
    enable = true
  }
}
