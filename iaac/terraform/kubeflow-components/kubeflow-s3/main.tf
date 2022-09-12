resource "aws_s3_bucket" "artifact_store" {
  # todo region
}

resource "aws_secretsmanager_secret" "s3_secret" {
  recovery_window_in_days = var.secret_recovery_window_in_days
}

resource "aws_secretsmanager_secret_version" "s3_secret_version" {
  secret_id     = aws_secretsmanager_secret.s3_secret.id
  secret_string = jsonencode({
    accesskey = var.aws_access_key
    secretkey = var.aws_secret_key
  })
}