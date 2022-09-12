resource "random_password" "db_password" {
  length           = 16
  special          = true
  override_special = "!#$%&*()-_=+[]{}<>:?"
}

resource "aws_db_subnet_group" "rds_db_subnet_group" {
  subnet_ids = var.subnet_ids
}

resource "random_uuid" "db_snapshot_suffix" {
  keepers = {
    instance_class       = var.db_class
    db_name                 = var.db_name
    username = coalesce(var.db_username, "admin")
    password = coalesce(var.db_password, random_password.db_password.result)
    multi_az = var.multi_az
    db_subnet_group_name = aws_db_subnet_group.rds_db_subnet_group.id
    security_group_id = var.security_group_id
  }
}

resource "aws_db_instance" "kubeflow_db" {
  allocated_storage    = var.db_allocated_storage
  engine               = "mysql"
  engine_version       = "8.0.17"
  instance_class       = var.db_class
  db_name                 = var.db_name
  username = coalesce(var.db_username, "admin")
  password = coalesce(var.db_password, random_password.db_password.result)
  multi_az = var.multi_az
  db_subnet_group_name = aws_db_subnet_group.rds_db_subnet_group.id
  vpc_security_group_ids = [var.security_group_id]
  final_snapshot_identifier = "snp-${random_uuid.db_snapshot_suffix.result}"
}

resource "aws_secretsmanager_secret" "rds_secret" {
  recovery_window_in_days = var.secret_recovery_window_in_days
}

resource "aws_secretsmanager_secret_version" "rds_secret_version" {
  secret_id     = aws_secretsmanager_secret.rds_secret.id
  secret_string = jsonencode({
    username = aws_db_instance.kubeflow_db.username
    password = aws_db_instance.kubeflow_db.password
    database = aws_db_instance.kubeflow_db.db_name
    host = aws_db_instance.kubeflow_db.address
    port = tostring(aws_db_instance.kubeflow_db.port)
  })
}