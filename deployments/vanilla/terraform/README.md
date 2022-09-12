# Kubeflow On EKS

This example deploys the following Basic EKS Cluster with VPC and install vanilla Kubeflow

- Creates a new sample VPC, 3 Private Subnets and 3 Public Subnets
- Creates Internet gateway for Public Subnets and NAT Gateway for Private Subnets
- Creates EKS Cluster Control plane with one managed node group
- Deploys Kubeflow addons

## How to Deploy

### Prerequisites


#### Step 1: Clone the repo using the command below

```sh
git clone https://github.com/awslabs/kubeflow-manifests.git
cd kubeflow-manifests/deployments/vanilla/terraform
```

#### Step 2: Install the necessary dependencies
Ensure that you have installed the following tools in your development environment.

1. [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)
2. [Kubectl](https://Kubernetes.io/docs/tasks/tools/)
3. [Terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli)
4. [Helm](https://helm.sh/docs/intro/install/)



Linux users can install by running the below shell script.

The unzip command needs to be installed. 

Ubuntu example:
```
sudo apt install unzip
```

Then install the remaining dependencies:
```sh
source install_deps_linux.sh
```

Verify dependencies:
```sh
aws --version
kubectl version
terraform --version
helm version
```

### Minimum IAM Policy

> **Note**: The policy resource is set as `*` to allow all resources, this is not a recommended practice.

You can find the policy [here](min-iam-policy.json)

#### Creating an instance profile to run the below steps on an ec2 machine

The below steps will create an IAM role and instance profile.
Use the instance profile when creating an ec2 instance to give the instance the necessary AWS permissions to run terraform.

> **Note**: The below steps must be run from the same folder as this README and be run with an account that has permissions to run the below commands.

```sh
export ROLE_NAME=eks-blueprints-role-$RANDOM
export INSTANCE_PROFILE_NAME=eks-blueprints-instance-profile-$RANDOM
aws iam create-role --role-name $ROLE_NAME --assume-role-policy-document file://ec2-instance-trust-policy.json && \
aws iam put-role-policy --role-name $ROLE_NAME --policy-name eks-blueprints-policy-$RANDOM --policy-document file://min-iam-policy.json && \
aws iam create-instance-profile --instance-profile-name $INSTANCE_PROFILE_NAME && \
aws iam add-role-to-instance-profile --instance-profile-name $INSTANCE_PROFILE_NAME --role-name $ROLE_NAME && \
echo "Created role $ROLE_NAME" && \
echo "Created instance profile $INSTANCE_PROFILE_NAME"
```


### Deployment Steps

#### Automated deployment


Run the below command to run the automated deployment for vanilla kubeflow.

By default this will create an an EKS cluster with:
- The name `kf-on-eks-vanilla`
- In the region `us-west-2`
- With K8s version `1.22`

```sh
source deploy.sh
```


##### Optional: High level customization options
The following variables can be exported for further customization before running the deployment script:

```sh
export TF_VAR_cluster_name=<desired_cluster_name>
export TF_VAR_cluster_region=<desired_cluster_region>
export TF_VAR_eks_version=<desired_eks_version>
```

#### Manual deployment

The automated deployment runs the below manual steps. Feel free to extend these steps to meet your use case.

##### Step 1: Clone the Kubeflow helm charts repo for terraform
```sh
git clone --branch helm-installation-bugbash-1.6 https://github.com/rrrkharse/kubeflow-manifests.git kubeflow-helm
export TF_VAR_kf_helm_repo_path=$PWD/kubeflow-helm
```
##### Step 2: Run Terraform INIT

Initialize a working directory with configuration files

```sh
terraform init
```

##### Step 3: Run Terraform PLAN

**Optional: High level customization options**

The following variables can be exported for further customization before running the deployment script:

```sh
export TF_VAR_cluster_name=<desired_cluster_name>
export TF_VAR_cluster_region=<desired_cluster_region>
export TF_VAR_eks_version=<desired_eks_version>
```


Verify the resources created by this execution

```sh
terraform plan
```

##### Step 4: Finally, Terraform APPLY

**Deploy the pattern**

```sh
terraform apply -target="module.vpc"
terraform apply -target="module.eks_blueprints"
terraform apply -target="module.eks_blueprints_kubernetes_addons"
terraform apply -target="module.kubeflow_components"
```

Enter `yes` to apply when prompted.

##### Step 5: Run `update-kubeconfig` command

Update your kube config with the cluster created by terraform.

```sh
$(terraform output -raw configure_kubectl)
```

Run the similiar command that was output after the terraform apply was completed.
##### Step 6: List all the worker nodes by running the command below

    kubectl get nodes

##### Step 7: List all the pods running in `kubeflow` namespace

    kubectl get pods -n kubeflow

All pods should be running.

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

### Automated cleanup

```sh
source destroy.sh
```

### Manual cleanup

To clean up your environment, destroy the Terraform modules in reverse order.

Destroy the Kubernetes Add-ons, EKS cluster with Node groups and VPC

```sh
terraform destroy -target="module.kubeflow_components" -auto-approve
terraform destroy -target="module.eks_blueprints_kubernetes_addons" -auto-approve
terraform destroy -target="module.eks_blueprints" -auto-approve
terraform destroy -target="module.vpc" -auto-approve
```

Finally, destroy any additional resources that are not in the above modules

```sh
terraform destroy -auto-approve
```
