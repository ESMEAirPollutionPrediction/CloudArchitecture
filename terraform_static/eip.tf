provider "aws" {
  region = var.region
  profile = var.profile
}

resource "aws_eip" "eip" {
  domain   = "vpc"
  tags = {
    Name = var.tag_name
  }
}