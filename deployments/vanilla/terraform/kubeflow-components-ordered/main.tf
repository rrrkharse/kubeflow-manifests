resource "kubernetes_namespace" "kubeflow" {
  metadata {
    labels = {
      control-plane = "kubeflow"
      istio-injection = "enabled"
    }

    name = "kubeflow"
  }
}

module "kubeflow_issuer" {
  source            = "../../../../iaac/terraform/kubeflow-components/kubeflow-issuer"
  helm_config = {
    chart = "${var.kf_helm_repo_path}/charts/common/kubeflow-issuer"
  }

  addon_context = var.addon_context
  # depends_on = [module.kubeflow_cert_manager]
}

module "kubeflow_istio" {
  source            = "../../../../iaac/terraform/kubeflow-components/istio-1-11"
  helm_config = {
    chart = "${var.kf_helm_repo_path}/charts/common/istio-1-14"
  }
  addon_context = var.addon_context
  depends_on = [module.kubeflow_issuer]
}

module "kubeflow_dex" {
  source            = "../../../../iaac/terraform/kubeflow-components/dex"
  helm_config = {
    chart = "${var.kf_helm_repo_path}/charts/common/dex"
  }
  addon_context = var.addon_context
  depends_on = [module.kubeflow_istio]
}

module "kubeflow_oidc_authservice" {
  source            = "../../../../iaac/terraform/kubeflow-components/oidc-authservice"
  helm_config = {
    chart = "${var.kf_helm_repo_path}/charts/common/oidc-authservice" 
  }
  addon_context = var.addon_context
  depends_on = [module.kubeflow_dex]
}

module "kubeflow_knative_serving" {
  source            = "../../../../iaac/terraform/kubeflow-components/knative-serving"
  helm_config = {
    chart = "${var.kf_helm_repo_path}/charts/common/knative-serving"
  }  
  addon_context = var.addon_context
  depends_on = [module.kubeflow_oidc_authservice]
}

module "kubeflow_cluster_local_gateway" {
  source            = "../../../../iaac/terraform/kubeflow-components/cluster-local-gateway"
  helm_config = {
    chart = "${var.kf_helm_repo_path}/charts/common/cluster-local-gateway"
  }  
  addon_context = var.addon_context
  depends_on = [module.kubeflow_knative_serving]
}

module "kubeflow_knative_eventing" {
  source            = "../../../../iaac/terraform/kubeflow-components/knative-eventing"
  helm_config = {
    chart = "${var.kf_helm_repo_path}/charts/common/knative-eventing"
  }  
  addon_context = var.addon_context
  depends_on = [module.kubeflow_cluster_local_gateway]
}

module "kubeflow_roles" {
  source            = "../../../../iaac/terraform/kubeflow-components/kubeflow-roles"
  helm_config = {
    chart = "${var.kf_helm_repo_path}/charts/common/kubeflow-roles"
  }  
  addon_context = var.addon_context
  depends_on = [module.kubeflow_knative_eventing]
}

module "kubeflow_istio_resources" {
  source            = "../../../../iaac/terraform/kubeflow-components/kubeflow-istio-resources"
  helm_config = {
    chart = "${var.kf_helm_repo_path}/charts/common/kubeflow-istio-resources"
  }  
  addon_context = var.addon_context
  depends_on = [module.kubeflow_roles]
}

module "kubeflow_pipelines" {
  source            = "../../../../iaac/terraform/kubeflow-components/kubeflow-pipelines"
  helm_config = {
    chart_1 = "${var.kf_helm_repo_path}/charts/apps/kubeflow-pipelines/vanilla-part-1"
    chart_2 = "${var.kf_helm_repo_path}/charts/apps/kubeflow-pipelines/vanilla-part-2"
  }  
  addon_context = var.addon_context
  depends_on = [module.kubeflow_istio_resources]
}

module "kubeflow_kserve" {
  source            = "../../../../iaac/terraform/kubeflow-components/kserve"
  helm_config = {
    chart = "${var.kf_helm_repo_path}/charts/common/kserve"
  }  
  addon_context = var.addon_context
  depends_on = [module.kubeflow_pipelines]
}

module "kubeflow_models_web_app" {
  source            = "../../../../iaac/terraform/kubeflow-components/models-web-app"
  helm_config = {
    chart = "${var.kf_helm_repo_path}/charts/apps/models-web-app"
  }  
  addon_context = var.addon_context
  depends_on = [module.kubeflow_kserve]
}

module "kubeflow_katib" {
  source            = "../../../../iaac/terraform/kubeflow-components/katib"
  helm_config = {
    chart = "${var.kf_helm_repo_path}/charts/apps/katib/vanilla"
  }  
  addon_context = var.addon_context
  depends_on = [module.kubeflow_models_web_app]
}

module "kubeflow_central_dashboard" {
  source            = "../../../../iaac/terraform/kubeflow-components/central-dashboard"
  helm_config = {
    chart = "${var.kf_helm_repo_path}/charts/apps/central-dashboard"
  }  
  addon_context = var.addon_context
  depends_on = [module.kubeflow_katib]
}

module "kubeflow_admission_webhook" {
  source            = "../../../../iaac/terraform/kubeflow-components/admission-webhook"
  helm_config = {
    chart = "${var.kf_helm_repo_path}/charts/common/admission-webhook"
  }  
  addon_context = var.addon_context
  depends_on = [module.kubeflow_central_dashboard]
}

module "kubeflow_notebook_controller" {
  source            = "../../../../iaac/terraform/kubeflow-components/notebook-controller"
  helm_config = {
    chart = "${var.kf_helm_repo_path}/charts/apps/notebook-controller"
  }  
  addon_context = var.addon_context
  depends_on = [module.kubeflow_admission_webhook]
}

module "kubeflow_jupyter_web_app" {
  source            = "../../../../iaac/terraform/kubeflow-components/jupyter-web-app"
  helm_config = {
    chart = "${var.kf_helm_repo_path}/charts/apps/jupyter-web-app"
  }  
  addon_context = var.addon_context
  depends_on = [module.kubeflow_notebook_controller]
}

module "kubeflow_profiles_and_kfam" {
  source            = "../../../../iaac/terraform/kubeflow-components/profiles-and-kfam"
  helm_config = {
    chart = "${var.kf_helm_repo_path}/charts/common/profiles-and-kfam"
  }  
  addon_context = var.addon_context
  depends_on = [module.kubeflow_jupyter_web_app]
}

module "kubeflow_volumes_web_app" {
  source            = "../../../../iaac/terraform/kubeflow-components/volumes-web-app"
  helm_config = {
    chart = "${var.kf_helm_repo_path}/charts/apps/volumes-web-app"
  }  
  addon_context = var.addon_context
  depends_on = [module.kubeflow_profiles_and_kfam]
}

module "kubeflow_tensorboards_web_app" {
  source            = "../../../../iaac/terraform/kubeflow-components/tensorboards-web-app"
  helm_config = {
    chart = "${var.kf_helm_repo_path}/charts/apps/tensorboards-web-app"
  }  
  addon_context = var.addon_context
  depends_on = [module.kubeflow_volumes_web_app]
}

module "kubeflow_tensorboard_controller" {
  source            = "../../../../iaac/terraform/kubeflow-components/tensorboard-controller"
  helm_config = {
    chart = "${var.kf_helm_repo_path}/charts/apps/tensorboard-controller"
  }  
  addon_context = var.addon_context
  depends_on = [module.kubeflow_tensorboards_web_app]
}

module "kubeflow_training_operator" {
  source            = "../../../../iaac/terraform/kubeflow-components/training-operator"
  helm_config = {
    chart = "${var.kf_helm_repo_path}/charts/apps/training-operator"
  }  
  addon_context = var.addon_context
  depends_on = [module.kubeflow_tensorboard_controller]
}

module "kubeflow_aws_telemetry" {
  count = var.enable_aws_telemetry ? 1 : 0
  source            = "../../../../iaac/terraform/kubeflow-components/aws-telemetry"
  helm_config = {
    chart = "${var.kf_helm_repo_path}/charts/common/aws-telemetry"
  }  
  addon_context = var.addon_context
  depends_on = [module.kubeflow_training_operator]
}

module "kubeflow_user_namespace" {
  source            = "../../../../iaac/terraform/kubeflow-components/user-namespace"
  helm_config = {
    chart = "${var.kf_helm_repo_path}/charts/common/user-namespace"
  }  
  addon_context = var.addon_context
  depends_on = [module.kubeflow_aws_telemetry]
}

module "ack_sagemaker" {
  source            = "../../../../iaac/terraform/kubernetes-addons/amazon-controller-for-k8s-sagemaker"
  addon_context = var.addon_context
}