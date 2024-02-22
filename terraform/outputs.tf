output "ssh_connect_cmd" {
  description = "connect with ssh"
  value       = "ssh -i \"${var.aws_private_key_ssh_path}\" ubuntu@${aws_instance.my-ec2.public_dns}"
}

output "ansible_hosts_ip_to_add" {
  description = "add public ip to ./ansible/hosts"
  value       = aws_instance.my-ec2.public_ip
}