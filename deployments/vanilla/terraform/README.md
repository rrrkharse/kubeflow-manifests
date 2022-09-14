# Kubeflow On EKS

This example deploys the following Basic EKS Cluster with VPC and install vanilla Kubeflow

- Creates a new sample VPC, 3 Private Subnets and 3 Public Subnets
- Creates Internet gateway for Public Subnets and NAT Gateway for Private Subnets
- Creates EKS Cluster Control plane with one managed node group
- Deploys Kubeflow addons

## How to Deploy

### Prerequisites

todo: link to our pre-req script

### Minimum IAM Policy

> **Note**: The policy resource is set as `*` to allow all resources, this is not a recommended practice.

You can find the policy [here](min-iam-policy.json)

### Deployment Steps

Run the below command to run the automated deployment for vanilla kubeflow.

By default this will create an an EKS cluster with:
- The name `kf-on-eks-vanilla`
- In the region `us-west-2`
- With K8s version `1.22`

```sh
bash deploy.sh
```

#### Optional: High level customization options
The following variables can be exported for further customization before running the deployment script:

```sh
export TF_VAR_cluster_name=<desired_cluster_name>
export TF_VAR_cluster_region=<desired_cluster_region>
export TF_VAR_eks_version=<desired_eks_version>
export TF_VAR_enable_aws_telemetry=<true|false>
```

## Verification

The following steps will allow you to access the Kubeflow central dashboard from your browser.

#### Step 0: Update the kubeconfig
```sh
$(terraform output -raw configure_kubectl)
```

#### Step 1: Enable portforwarding for the central dashboard
```sh
kubectl port-forward svc/istio-ingressgateway -n istio-system 8080:80
```

#### [Optional] Step 2: Enable portfowarding from your ec2 instance

If you are running kubectl on an ec2 instance you will need to run the below command on your local machine to access the dashboard.
```sh
ssh -i your-ssh-key.pem -N -L 8080:localhost:8080 your-ec2-instance-username@your-ec2-instance-dns.us-west-2.compute.amazonaws.com
```

This is an extension of the ssh command used to ssh to the instance, so if your ssh command was:
```sh
ssh -i "key.pem" ubuntu@ec2-xx-xx-xxx-xx.us-west-2.compute.amazonaws.com
```

then you would run:
```sh
ssh -i "key.pem" -N -L 8080:localhost:8080 ubuntu@ec2-xx-xx-xxx-xx.us-west-2.compute.amazonaws.com
```

#### Step 3: Login to the central dashboard.

Open `http://localhost:8080` in a browser of your choosing.

Provide the following username and password at the login screen:
- Username: `user@example.com`
- Password: `12341234`

## Cleanup

```sh
bash destroy.sh
```