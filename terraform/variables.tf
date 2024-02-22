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

variable "ami_id" {
  description = "id of an ami by default it's ubuntu 22.04"
  type        = string
  default     = "ami-01dd271720c1ba44f"
}

variable "instance_type" {
  description = "aws ec2 instance type"
  type        = string
  default     = "t2.micro"
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