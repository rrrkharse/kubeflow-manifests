#!/bin/bash

terraform destroy -target="module.kubeflow_components" -auto-approve && \
terraform destroy -target="module.eks_blueprints_kubernetes_addons" -auto-approve && \
terraform destroy -target="module.eks_blueprints" -auto-approve && \
terraform destroy -target="module.vpc" -auto-approve && \
terraform destroy -auto-approve