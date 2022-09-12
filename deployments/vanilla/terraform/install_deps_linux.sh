#!/bin/bash

mkdir tmp
cd tmp

# Install AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Install Terraform
curl "https://releases.hashicorp.com/terraform/1.2.7/terraform_1.2.7_linux_amd64.zip" -o "terraform.zip"
unzip terraform.zip
sudo install -o root -g root -m 0755 terraform /usr/local/bin/terraform

# Install Helm
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

cd -
rm -rf tmp