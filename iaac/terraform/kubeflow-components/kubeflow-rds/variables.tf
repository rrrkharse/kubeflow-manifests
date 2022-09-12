variable "vpc_id" {
  type        = string
  description = "VPC of the EKS cluster"
}

variable "subnet_ids" {
  type        = list(string)
  description = "Subnet ids of the EKS cluster"
}

variable "security_group_id" {
  type        = string
  description = "SecurityGroup Id of a EKS Worker Node"
}

variable "db_name" {
  type        = string
  description = "Database name"
}

variable "db_username" {
  type        = string
  description = "Database admin account username"
}

variable "db_password" {
  type        = string
  description = "Database admin account password"
}

variable "db_class" {
  type        = string
  description = "Database instance type"
}

variable "db_allocated_storage" {
  type        = string
  description = "The size of the database (Gb)"
}

variable "multi_az" {
  type        = string
  description = "Enables multi AZ for the master database"
}

variable "manage_via_gitops" {
  type        = bool
  default     = false
  description = "Determines if the add-on should be managed via GitOps."
}

variable "secret_recovery_window_in_days" {
  type = number
}

variable "addon_context" {
  type = object({
    aws_caller_identity_account_id = string
    aws_caller_identity_arn        = string
    aws_eks_cluster_endpoint       = string
    aws_partition_id               = string
    aws_region_name                = string
    eks_cluster_id                 = string
    eks_oidc_issuer_url            = string
    eks_oidc_provider_arn          = string
    tags                           = map(string)
    irsa_iam_role_path             = string
    irsa_iam_permissions_boundary  = string
  })
  description = "Input configuration for the addon"
}
