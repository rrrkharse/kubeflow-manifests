# tflint-ignore: terraform_unused_declarations
variable "cluster_name" {
  description = "Name of cluster"
  type        = string
  default     = "kf-on-eks-vanilla"
}

variable "cluster_region" {
  description = "Region to create the cluster"
  type        = string
  default     = "us-west-2"
}

variable "eks_version" {
  description = "The EKS version to use"
  type        = string
  default     = "1.22"
}

variable "enable_aws_telemetry" {
  description = "Enable AWS telemetry addon to provide diagnostic data to AWS"
  type = bool
  default = true
}

variable "kf_helm_repo_path" {
  description = "Full path to the location of the helm folder to install from for KF 1.6"
  type        = string
}