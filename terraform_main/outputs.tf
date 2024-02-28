output "ssh_connect_cmd" {
  description = "connect with ssh"
  value       = "ssh -i ${var.aws_private_key_ssh_path} ubuntu@${aws_instance.my-ec2.public_dns}"
}

output "ansible_hosts_ip_to_add" {
  description = "add public ip to ./ansible/hosts (taken from eip public ip, not ec2 public ip)"
  value       = data.aws_eip.eip.public_ip
}

output "ansible_playbook_command" {
  description = "Static command to execute ansible-playbook"
  value = "ansible-playbook --private-key ~/.ssh/ec2 -i ansible/hosts ansible/main.yml"
}