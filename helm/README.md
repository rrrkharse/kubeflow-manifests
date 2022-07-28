[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/awslabs/kubeflow-manifests/issues)
![current development version](https://img.shields.io/badge/Kubeflow-v1.5.1-green.svg?style=flat)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](./LICENSE)
# Helm Installation for Kubeflow on AWS (Vanilla)

## Overview
[Helm][] is the package manager for Kubernetes. In the following instructions, users can use **Helm** to install and manage **Kubeflow** instead of [Kustomize][].

## Install Helm
[Install Helm][] to your computer with one of the options you preferred. Check your helm version running:
```bash
helm version
```
Make sure you are using **helm v3.7+**.

## Prerequisites
Install required dependencies and create an EKS cluster following the [Installation Prerequisite][] guideline. 

## Vanilla Installation
This guide describes how to deploy Kubeflow on AWS EKS with **Helm**. This vanilla version has minimal changes to the upstream Kubeflow manifests.

Be sure that you have satisfied the [Installation Prerequisite][] before working through this guide.

Install helm through `helm install [Release Name] [Path]` command: 


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
helm install dex helm/apps/dex;
helm install oidc-authservice helm/apps/oidc-authservice;
helm install admission-webhook helm/apps/admission-webhook;
helm install profile-and-kfam helm/apps/profiles-and-kfam;
helm install user-namespace helm/apps/user-namespace;
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

## Connect to your Kubeflow cluster 
After installation, it will take some time for all Pods to become ready. Make sure all Pods are ready before trying to connect, otherwise you might get unexpected errors. To check that all Kubeflow-related Pods are ready, use the following commands:

```bash
kubectl get pods -n cert-manager
kubectl get pods -n istio-system
kubectl get pods -n auth
kubectl get pods -n knative-eventing
kubectl get pods -n knative-serving
kubectl get pods -n kubeflow
kubectl get pods -n kubeflow-user-example-com
# Depending on your installation if you installed KServe
kubectl get pods -n kserve
```

Your should see helm releases are in deployed status:
```bash
$ helm list --namespace cert-manager
NAME        	NAMESPACE   	REVISION	UPDATED                            	STATUS  	CHART              	APP VERSION
cert-manager	cert-manager	1       	2022-07-28 12:05:28.69295 -0700 PDT	deployed	cert-manager-v1.5.0	v1.5.0     
```

```bash
$ helm list
NAME                    	NAMESPACE	REVISION	UPDATED                             	STATUS  	CHART                         	APP VERSION
admission-webhook       	default  	1       	2022-07-28 12:57:27.613949 -0700 PDT	deployed	admission-webhook-0.1.0       	1.16.0     
aws-secrets-manager     	default  	1       	2022-07-28 12:55:30.291808 -0700 PDT	deployed	aws-secrets-manager-0.1.0     	1.16.0     
aws-telemetry           	default  	1       	2022-07-28 12:39:24.261685 -0700 PDT	deployed	aws-telemetry-0.1.0           	1.16.0     
central-dashboard       	default  	1       	2022-07-28 12:39:41.64472 -0700 PDT 	deployed	central-dashboard-0.1.0       	1.16.0     
cluster-local-gateway   	default  	1       	2022-07-28 12:31:55.501454 -0700 PDT	deployed	cluster-local-gateway-0.1.0   	1.16.0     
dex                     	default  	1       	2022-07-28 12:38:35.15731 -0700 PDT 	deployed	dex-0.1.0                     	1.16.0     
istio-1-11              	default  	1       	2022-07-28 12:07:47.921271 -0700 PDT	deployed	istio-1-11-0.1.0              	1.16.0     
jupyter-web-app         	default  	1       	2022-07-28 12:42:23.163274 -0700 PDT	deployed	jupyter-web-app-0.1.0         	1.16.0     
katib                   	default  	1       	2022-07-28 12:54:47.810424 -0700 PDT	deployed	katib-0.1.0                   	1.16.0     
knative-eventing        	default  	1       	2022-07-28 12:34:36.922185 -0700 PDT	deployed	knative-eventing-0.1.0        	1.16.0     
knative-serving         	default  	1       	2022-07-28 12:32:33.226445 -0700 PDT	deployed	knative-serving-0.1.0         	1.16.0     
kserve                  	default  	1       	2022-07-28 12:44:00.152331 -0700 PDT	deployed	kserve-0.1.0                  	1.16.0     
kubeflow-issuer         	default  	1       	2022-07-28 12:31:22.068229 -0700 PDT	deployed	kubeflow-issuer-0.1.0         	1.16.0     
kubeflow-istio-resources	default  	1       	2022-07-28 12:31:40.286801 -0700 PDT	deployed	kubeflow-istio-resources-0.1.0	1.16.0     
kubeflow-namespace      	default  	1       	2022-07-28 12:09:07.416695 -0700 PDT	deployed	kubeflow-namespace-0.1.0      	1.16.0     
kubeflow-pipelines      	default  	1       	2022-07-28 12:51:57.293078 -0700 PDT	deployed	kubeflow-pipelines-0.1.0      	1.16.0     
kubeflow-roles          	default  	1       	2022-07-28 12:31:03.351416 -0700 PDT	deployed	kubeflow-roles-0.1.0          	1.16.0     
models-web-app          	default  	1       	2022-07-28 12:43:29.275867 -0700 PDT	deployed	models-web-app-0.1.0          	1.16.0     
notebook-controller     	default  	1       	2022-07-28 12:42:58.397411 -0700 PDT	deployed	notebook-controller-0.1.0     	1.16.0     
oidc-authservice        	default  	1       	2022-07-28 12:39:01.325914 -0700 PDT	deployed	oidc-authservice-0.1.0        	1.16.0     
profiles-and-kfam       	default  	1       	2022-07-28 12:58:02.22225 -0700 PDT 	deployed	profiles-and-kfam-0.1.0       	1.16.0     
tensorboard-controller  	default  	1       	2022-07-28 12:40:59.266969 -0700 PDT	deployed	tensorboard-controller-0.1.0  	1.16.0     
tensorboards-web-app    	default  	1       	2022-07-28 12:41:26.352725 -0700 PDT	deployed	tensorboards-web-app-0.1.0    	1.16.0     
training-operator       	default  	1       	2022-07-28 12:40:25.528385 -0700 PDT	deployed	training-operator-0.1.0       	1.16.0     
user-namespace          	default  	1       	2022-07-28 12:58:32.830817 -0700 PDT	deployed	user-namespace-0.1.0          	1.16.0     
volumes-web-app         	default  	1       	2022-07-28 12:41:57.884204 -0700 PDT	deployed	volumes-web-app-0.1.0         	1.16.0  
```



## Port-Forward
Follow the following port-forward guideline to access Kubeflow (https://awslabs.github.io/kubeflow-manifests/docs/deployment/vanilla/guide/#port-forward)


## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This project is [licensed](LICENSE) under the Apache-2.0 License.


[Helm]: https://helm.sh/
[Kustomize]: https://kustomize.io/
[Install Helm]: https://helm.sh/docs/intro/install/
[Installation Prerequisite]: https://awslabs.github.io/kubeflow-manifests/docs/deployment/prerequisites/
[cert-manager Verification]: https://cert-manager.io/docs/installation/verify/#check-cert-manager-api
[cmctl]: https://cert-manager.io/docs/usage/cmctl/#installation