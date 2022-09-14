#!/bin/bash

terraform init && \
terraform apply -target="module.vpc" -auto-approve && \
terraform apply -target="module.eks_blueprints" -auto-approve && \
terraform apply -target="module.eks_blueprints_kubernetes_addons" -auto-approve && \
terraform apply -target="module.kubeflow_components" -auto-approve