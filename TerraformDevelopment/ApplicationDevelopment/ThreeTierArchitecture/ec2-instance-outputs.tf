# AWS EC2 Instance Terraform Outputs
# Public EC2 Instances - Bastion Host

## ec2_bastion_public_instance_ids

output "ec2_bastion_public_instance_ids" {
  description = "ec2 bastion host instance id"
  value       = module.ec2-public-instance.id
}

output "ec2_bastion_public_instance_public_ip" {
  description = "ec2 bastion host instance id"
  value       = module.ec2-public-instance.public_ip
}

# Private EC2 Instances
## ec2_private_instance_ids
output "ec2_private_instance_ids" {
  description = "List of Id's of private ec2-instance"
  value       = [for ec2private in module.ec2-private-instance : ec2private.id]
}

## ec2_private_instance_ids
output "ec2_private_instance_private_ips" {
  description = "List of IP addresses of private ec2-instance"
  value       = [for ec2private in module.ec2-private-instance : ec2private.public_ip]
}