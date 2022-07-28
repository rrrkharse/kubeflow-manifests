[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/awslabs/kubeflow-manifests/issues)
![current development version](https://img.shields.io/badge/Kubeflow-v1.5.1-green.svg?style=flat)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](./LICENSE)
# Helm Installation for Kubeflow on AWS

## Overview
[Helm][] is the package manager for Kubernetes. In the following instructions, users can use **Helm** to install and manage **Kubeflow** instead of [Kustomize][].

## Install Helm
[Install Helm][] to you computer with one of the options you preferred. Check your helm version running:
```bash
helm version
```
Make sure you are using **helm v3.7+**.

## Prerequisites
Install required dependencies and create an EKS cluster following the [Installation Prerequisite][] guideline. 

## Cognito Installation
This guide describes how to deploy Kubeflow on AWS EKS using **Cognito** as identity provider. Kubeflow uses Istio to manage internal traffic. In this guide we will be creating an Ingress to manage external traffic to the Kubernetes services and an Application Load Balancer (ALB) to provide public DNS and enable TLS authentication at the load balancer. We will also be creating a custom domain to host Kubeflow since certificates (needed for TLS) for ALB’s public DNS names are not supported.


Be sure that you have satisfied the [Installation Prerequisite][] before working through this guide.

Install helm through `helm install [Release Name] [Path]` command: 


## Automated Deployment Guide

The following steps automate 
        -[section 1.0(Custom domain and certificates)][] (creating a custom domain to host Kubeflow and TLS certificates for the domain)
        -[section 2.0(Cognito user pool)][] (creating a Cognito Userpool used for user authentication) -[section 3.0(Configure Ingress)][] (configuring ingress and load balancer controller manifests) of the cognito guide.

Follow (https://awslabs.github.io/kubeflow-manifests/docs/deployment/cognito/guide-automated/#create-required-resources-and-deploy-kubeflow) to finish **step 1**, which utilize the automation script `tests/e2e/utils/cognito_bootstrap/cognito_pre_deployment.py` to configure required AWS resources. Come back to this page **before running the kustomize build command**.



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

3. Install Kubeflow Namespace:
```bash
helm install kubeflow-namespace helm/common/kubeflow-namespace
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
helm install admission-webhook helm/apps/admission-webhook;
helm install profile-and-kfam helm/apps/profiles-and-kfam;
helm install aws-telemetry helm/apps/aws-telemetry;
helm install central-dashboard helm/apps/central-dashboard;
helm install training-operator helm/apps/training-operator;
helm install tensorboard-controller helm/apps/tensorboard-controller;
helm install tensorboards-web-app helm/apps/tensorboards-web-app;
helm install volumes-web-app helm/apps/volumes-web-app;
helm install jupyter-web-app helm/apps/jupyter-web-app;
helm install notebook-controller helm/apps/notebook-controller;
helm install katib helm/apps/katib;
helm install models-web-app helm/apps/models-web-app;
helm install kserve helm/apps/kserve;
helm install kubeflow-pipelines helm/apps/kubeflow-pipelines
```

6. Based on the generated `tests/e2e/utils/cognito_bootstrap/config.yaml/config.yaml`, fill in parameters for **values.yaml** in the following charts:
        -`helm/deployment-specifics/cognito/alb-controller/values.yaml`
        -`helm/deployment-specifics/cognito/aws-authservice/values.yaml`
        -`helm/deployment-specifics/cognito/ingress/values.yaml`

7. Install **Ingress**, **ALB-Controller**, and **Authservice** for Cognito configuration:
```bash
helm install alb-controller helm/deployment-specifics/cognito/alb-controller;
helm install aws-authservice helm/deployment-specifics/cognito/aws-authservice;
helm install ingress helm/deployment-specifics/cognito/ingress;
```

8. Check if ALB is provisioned. It takes around 3-5 minutes:
```bash
kubectl get ingress -n istio-system
NAME            CLASS    HOSTS ADDRESS                                                                 PORTS   AGE
istio-ingress   <none>   *     k8s-istiosys-istioing-xxxxxx-988711998.ca-central-1.elb.amazonaws.com   80      8s
```

If ADDRESS is empty after a few minutes, check the logs of alb-ingress-controller by following [this guide][]

9. Substitute the ALB address under kubeflow.alb.dns in tests/e2e/utils/cognito_bootstrap/config.yaml. The kubeflow section of the config file will look like:
```bash
kubeflow:
  alb:
    dns: k8s-istiosys-istioing-xxxxxx-988711998.ca-central-1.elb.amazonaws.com
    serviceAccount:
      name: aws-load-balancer-controller
      namespace: kube-system
      policyArn: arn:aws:iam::258812065542:policy/alb_ingress_controller_helm-bugbash-123456
```

10. Run the following script to update the subdomain with ALB address:
```bash
 cd tests/e2e
 PYTHONPATH=.. python utils/cognito_bootstrap/cognito_post_deployment.py
 cd -
```

11. Follow the rest of the cognito guide from [section 6.0(Connecting to central dashboard)][] to:

-Create a user in Cognito user pool
-Create a profile for the user from the user pool
-Connect to the central dashboard


## Connect to your Kubeflow cluster 



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
[section 1.0(Custom domain and certificates)]: https://awslabs.github.io/kubeflow-manifests/docs/deployment/cognito/guide/#10-custom-domain-and-certificates
[section 2.0(Cognito user pool)]: https://awslabs.github.io/kubeflow-manifests/docs/deployment/cognito/guide/#20-cognito-user-pool
[section 3.0(Configure Ingress)]: https://awslabs.github.io/kubeflow-manifests/docs/deployment/cognito/guide/#30-configure-ingress
[this guide]:https://awslabs.github.io/kubeflow-manifests/docs/troubleshooting-aws/#alb-fails-to-provision
[section 6.0(Connecting to central dashboard)]:https://awslabs.github.io/kubeflow-manifests/docs/deployment/cognito/guide/#60-connecting-to-central-dashboard