output "instance_ip" {
  description = "The public dns for ssh access (scripts created in ./bin/)"
  value       = aws_instance.my-ec2.public_dns
}