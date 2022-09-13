#!/bin/bash

git -C kubeflow-helm pull || git clone --branch helm-chart-vanilla-v1.6.0 https://github.com/rrrkharse/kubeflow-manifests.git kubeflow-helm
export TF_VAR_kf_helm_repo_path=$PWD/kubeflow-helm


terraform init && \
terraform apply -target="module.vpc" -auto-approve && \
terraform apply -target="module.eks_blueprints" -auto-approve && \
terraform apply -target="module.eks_blueprints_kubernetes_addons" -auto-approve && \
terraform apply -target="module.kubeflow_components" -auto-approve