provider "aws" {
  region = var.region
  profile = var.profile
}

resource "aws_key_pair" "admin" {
  key_name   = "admin"
  public_key = file(var.aws_public_key_ssh_path)
}

resource "aws_default_vpc" "default" {
  tags = {
    Name = "Default VPC"
  }
}

resource "aws_default_security_group" "default" {
  vpc_id = aws_default_vpc.default.id
  ingress {
    protocol  = "tcp"
    from_port = 22
    to_port   = 22
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    protocol  = "tcp"
    from_port = 80
    to_port   = 80
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "my-ec2" {
  ami           = var.ami_id
  instance_type = var.instance_type
  key_name = aws_key_pair.admin.key_name
  
  depends_on = [ aws_key_pair.admin ]
}
