#!/bin/bash

# hack to handle the automatic deletion of the sa when calling helm delete 
# which causes deletion of the tf created sa to fail
# todo: profiles-and-kfam helm chart should accept an optional irsa role annotation
terraform state rm "module.kubeflow_components.module.kubeflow_profiles_and_kfam.kubernetes_service_account_v1.profile_controller_sa" || true

terraform destroy -target="module.kubeflow_components" -auto-approve && \
terraform destroy -target="module.eks_blueprints_kubernetes_addons" -auto-approve && \
terraform destroy -target="module.eks_blueprints" -auto-approve && \
terraform destroy -target="module.vpc" -auto-approve && \
terraform destroy -auto-approve