# tflint-ignore: terraform_unused_declarations
variable "cluster_name" {
  description = "Name of cluster"
  type        = string
}

variable "cluster_region" {
  description = "Region to create the cluster"
  type        = string
}

variable "eks_version" {
  description = "The EKS version to use"
  type        = string
  default     = "1.22"
}

variable "enable_aws_telemetry" {
  description = "Enable AWS telemetry component"
  type = bool
  default = true
}

variable "db_name" {
  type        = string
  description = "Database name"
  default = "kubeflow"
}

variable "db_username" {
  type        = string
  description = "Database admin account username"
  default = "admin"
}

variable "db_password" {
  type        = string
  description = "Database admin account password"
  default = null
}

variable "db_class" {
  type        = string
  description = "Database instance type"
  default = "db.m5.large"
}

variable "db_allocated_storage" {
  type        = string
  description = "The size of the database (Gb)"
  default = "20"
}

variable "multi_az" {
  type        = string
  description = "Enables multi AZ for the master database"
  default     = "true"
}

variable "mlmdb_name" {
  type        = string
  default = "metadb"
  description = "Name of the mlm DB to create"
}

variable "minio_service_host" {
  type        = string
  default = "s3.amazonaws.com"
  description = "S3 service host DNS. This field will need to be changed when making requests from other partitions e.g. China Regions"
}

variable "secret_recovery_window_in_days" {
  type = number
  default = 7
}

variable "generate_db_password" {
  description = "Generates a random admin password for the RDS database. Is overriden by db_password"
  type = bool
  default = false
}

variable "force_destroy_s3_bucket" {
  type = bool
  description = "Destroys s3 bucket even when the bucket is not empty"
  default = false
}

variable "aws_access_key" {
  type        = string
  description = "AWS access key to authenticate minio client"
  default = null
}

variable "aws_secret_key" {
  type        = string
  description = "AWS secret key to authenticate minio client"
  default = null
}

variable "kf_helm_repo_path" {
  description = "Full path to the location of the helm repo for KF"
  type        = string
  default = "../../.."
}