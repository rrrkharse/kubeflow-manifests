[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/awslabs/kubeflow-manifests/issues)
![current development version](https://img.shields.io/badge/Kubeflow-v1.5.1-green.svg?style=flat)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](./LICENSE)
# Helm Installation for Kubeflow on AWS (RDS/S3)

## Overview
[Helm][] is the package manager for Kubernetes. In the following instructions, users can use **Helm** to install and manage **Kubeflow** instead of [Kustomize][].

## Install Helm
[Install Helm][] to you computer with one of the options you preferred. Check your helm version running:
```bash
helm version
```
Make sure you are using **helm v3.7+**.

## Prerequisites
Install required dependencies and create an EKS cluster following the [Prerequisite][] guideline. 

## RDS and S3 Installation
This guide describes how to deploy Kubeflow on AWS EKS using **RDS/S3** to persist KFP data. For advantage of using **RDS/S3**, refer to [existing installation guideline][] with kustomize.


Be sure that you have satisfied the [Installation Prerequisite][] before working through this guide.

Install helm through `helm install [Release Name] [Path]` command: 


## Automated Deployment Guide

1. Install Cert-Manager:

```bash
helm install cert-manager helm/common/cert-manager \
--namespace cert-manager \
--create-namespace \
--set installCRDs=true
```

Install [cmctl][] and verify the installation following [cert-manager Verification][]

Check if cmctl is ready:
```bash
$ cmctl check api
The cert-manager API is ready
```

Verify cert-manager pods are running:
```bash
$ kubectl get pods --namespace cert-manager

NAME                                       READY   STATUS    RESTARTS   AGE
cert-manager-5c6866597-zw7kh               1/1     Running   0          2m
cert-manager-cainjector-577f6d9fd7-tr77l   1/1     Running   0          2m
cert-manager-webhook-787858fcdb-nlzsq      1/1     Running   0          2m
```


2. Install Istio:
```bash
helm install istio-1-11 helm/common/istio-1-11
```

3. Install kubeflow namespace:
```bahs
helm install kubeflow-namespace helm/common/kubeflow-namespace
```


Follow [Step 2.1][] for AWS resources automated setup. The script takes care of creating the S3 bucket, creating the S3 Secrets using the Secrets manager, setting up the RDS database, and creating the RDS Secret using the Secrets manager. The script also edits the required configuration files for Kubeflow Pipelines to be properly configured for the RDS database during Kubeflow installation. The script also handles cases where the resources already exist. In this case, the script will simply skip the step.

```bash
export CLUSTER_REGION=
export CLUSTER_NAME=
export S3_BUCKET=
export MINIO_AWS_ACCESS_KEY_ID=
export MINIO_AWS_SECRET_ACCESS_KEY=
export RDS_SECRET_NAME=
export S3_SECRET_NAME=
export DB_INSTANCE_NAME=
export DB_SUBNET_GROUP_NAME=
```

```bash
cd tests/e2e
```

```bash
PYTHONPATH=.. python3 utils/rds-s3/auto-rds-s3-setup.py \
--region $CLUSTER_REGION --cluster $CLUSTER_NAME \
--bucket $S3_BUCKET --rds_secret_name $RDS_SECRET_NAME \
--s3_aws_access_key_id $MINIO_AWS_ACCESS_KEY_ID \
--s3_aws_secret_access_key $MINIO_AWS_SECRET_ACCESS_KEY \
--db_instance_name $DB_INSTANCE_NAME --s3_secret_name $S3_SECRET_NAME  \
--db_subnet_group_name $DB_SUBNET_GROUP_NAME
```



4. Install Kubeflow Networking Components:

```bash
helm install kubeflow-roles helm/apps/kubeflow-roles;
helm install kubeflow-issuer helm/apps/kubeflow-issuer;
helm install kubeflow-istio-resources helm/apps/kubeflow-istio-resources;
helm install cluster-local-gateway helm/apps/cluster-local-gateway;
helm install knative-serving helm/apps/knative-serving;
helm install knative-eventing helm/apps/knative-eventing;
```


5. Install the rest of Kubeflow Components:
```bash
helm install dex helm/apps/dex;
helm install oidc-authservice helm/apps/oidc-authservice;
helm install aws-telemetry helm/apps/aws-telemetry;
helm install central-dashboard helm/apps/central-dashboard;
helm install training-operator helm/apps/training-operator;
helm install tensorboard-controller helm/apps/tensorboard-controller;
helm install tensorboards-web-app helm/apps/tensorboards-web-app;
helm install volumes-web-app helm/apps/volumes-web-app;
helm install jupyter-web-app helm/apps/jupyter-web-app;
helm install notebook-controller helm/apps/notebook-controller;
helm install models-web-app helm/apps/models-web-app;
helm install kserve helm/apps/kserve;
```

## [RDS and S3] Deploy both RDS and S3
6. Filled in parameters for **values.yaml** in the following charts: \
        -`helm/deployment-specifics/rds-s3/rds-and-s3/aws-secrets-manager/values.yaml` \
        -`helm/deployment-specifics/rds-s3/rds-and-s3/kubeflow-pipelines/values.yaml` \
You can file your rds-host end point from `awsconfigs/apps/pipeline/rds/params.env`

7. Configure for RDS and S3 to persist data: \
        - Install **Kubeflow-pipelines** \
        ```bash
        helm install kubeflow-pipelines helm/deployment-specifics/rds-s3/rds-and-s3/kubeflow-pipelines;
        ``` \
        -Install **Katib** \
        ```bash
        helm install katib helm/deployment-specifics/rds-s3/rds-and-s3/katib;
        ``` \
        -Install **AWS-Secrets-Manager** \
        ```bash
         helm install aws-secrets-manager helm/deployment-specifics/rds-s3/rds-and-s3/aws-secrets-manager;
        ```

## [RDS Only] Deploy only with RDS
6. Filled in parameters for **values.yaml** in the following charts: \
        -`helm/deployment-specifics/rds-s3/rds-only/aws-secrets-manager/values.yaml` \
        -`helm/deployment-specifics/rds-s3/rds-only/kubeflow-pipelines/values.yaml` \
You can file your rds-host end point from `awsconfigs/apps/pipeline/rds/params.env`

7. Configure for RDS to persist data: \
        - Install **Kubeflow-pipelines** \
        ```bash
        helm install kubeflow-pipelines helm/deployment-specifics/rds-s3/rds-only/kubeflow-pipelines;
        ```
        -Install **Katib** \
        ```bash
        helm install katib helm/deployment-specifics/rds-s3/rds-only/katib;
        ```
        -Install **AWS-Secrets-Manager** \
        ```bash
         helm install aws-secrets-manager helm/deployment-specifics/rds-s3/rds-only/aws-secrets-manager;
        ```

## [S3 Only] Deploy only with RDS
6. Filled in parameters for **values.yaml** in the following charts: \
        -`helm/deployment-specifics/rds-s3/s3-only/aws-secrets-manager/values.yaml` \
        -`helm/deployment-specifics/rds-s3/s3-only/kubeflow-pipelines/values.yaml` \
You can file your rds-host end point from `awsconfigs/apps/pipeline/rds/params.env`

7. Configure for RDS to persist data: \
        - Install **Kubeflow-pipelines** \
        ```bash
        helm install kubeflow-pipelines helm/deployment-specifics/rds-s3/s3-only/kubeflow-pipelines;
        ```
        -Install **Katib** \
        ```bash
        helm install katib helm/deployment-specifics/rds-s3/s3-only/katib;
        ```
        -Install **AWS-Secrets-Manager**
        ```bash
         helm install aws-secrets-manager helm/deployment-specifics/rds-s3/s3-only/aws-secrets-manager;
        ```




8. Install **Admission Webhook** , **Profiles and Kubeflow Access-Management** and **User Namespace** \
```bash
helm install admission-webhook helm/apps/admission-webhook;
helm install profiles-and-kfam helm/apps/profiles-and-kfam;
helm install user-namespace helm/apps/user-namespace;
```



9. Verify the installation following (https://awslabs.github.io/kubeflow-manifests/docs/deployment/rds-s3/guide/#40-verify-the-installation)

10. Port-forward into Kubeflow Dashboard
```bash
kubectl port-forward svc/istio-ingressgateway -n istio-system 8080:80
```

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This project is [licensed](LICENSE) under the Apache-2.0 License.


[Helm]: https://helm.sh/
[Kustomize]: https://kustomize.io/
[Install Helm]: https://helm.sh/docs/intro/install/
[Prerequisite]: https://awslabs.github.io/kubeflow-manifests/docs/deployment/prerequisites/
[cert-manager Verification]: https://cert-manager.io/docs/installation/verify/#check-cert-manager-api
[cmctl]: https://cert-manager.io/docs/usage/cmctl/#installation
[existing installation guideline]: https://awslabs.github.io/kubeflow-manifests/docs/deployment/rds-s3/guide/
[Step 2.1]: https://awslabs.github.io/kubeflow-manifests/docs/deployment/rds-s3/guide/#21-option-1-automated-setup