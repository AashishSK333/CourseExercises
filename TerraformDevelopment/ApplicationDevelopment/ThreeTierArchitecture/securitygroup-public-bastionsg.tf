# AWS EC2 security group Terraform module
# Security group for Public Bastion Host
module "public_bastion_sg" {
  source  = "terraform-aws-modules/security-group/aws"
  version = "5.1.0"

  name        = "public-bastion-securitygroup"
  description = "Security group with SSH port open for everybody (IPV4 CIDR), egress ports are open for all internet"
  vpc_id      = module.vpc-exe1.vpc_id
  # Ingress Rules & CIDR Blocks
  ingress_rules       = ["ssh-tcp"]
  ingress_cidr_blocks = ["0.0.0.0/0"]
  # Egress Rule - all-all open
  egress_rules = ["all-all"]
  tags         = local.common_tags
}