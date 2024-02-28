output "ansible_hosts_ip_to_add" {
  description = "add public ip to ./ansible/hosts (taken from eip public ip, not ec2 public ip)"
  value       = aws_eip.eip.public_ip
}

output "eip_id" {
  description = "eip allocation ID used to import it into the main terraform module"
  value       = aws_eip.eip.allocation_id
}