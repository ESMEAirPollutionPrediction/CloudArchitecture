resource "aws_s3_bucket" "bucket" {
  bucket = "esme-pollution-bucket"
  force_destroy = true
  object_lock_enabled = true
  tags = {
    Name = var.tag_name
  }
}