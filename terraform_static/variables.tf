variable "region" {
  description = "The aws region the resources will be built in"
  type        = string
  default = "eu-west-1"
}

variable "profile" {
  description = "The AWS Configure profile to use (local credentials)"
  type        = string
  default = "ESMEAdmin"
}

variable "tag_name" {
  description = "Aws tag name permit to search an instance by tag"
  type        = string
}

variable "aws_public_key_ssh_path" {
  description = "The key name of the Key Pair to use for the instance"
  type        = string
  default = "~/.ssh/ec2.pub"
}

variable "aws_private_key_ssh_path" {
  description = "The key name of the Key Pair to use for the instance"
  type        = string
  default = "~/.ssh/ec2"
}