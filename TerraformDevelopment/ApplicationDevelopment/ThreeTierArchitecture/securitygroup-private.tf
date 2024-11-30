# AWS EC2 security group Terraform module
# Security group for Private EC2 instances
module "private_sg" {
  source  = "terraform-aws-modules/security-group/aws"
  version = "5.1.0"

  name        = "private-securitygroup"
  description = "Security group with HTTP & SSH port open for entire VPC block"
  vpc_id      = module.vpc-exe1.vpc_id
  # Ingress Rules & CIDR Blocks
  ingress_rules       = ["ssh-tcp", "http-80-tcp"]
  ingress_cidr_blocks = [module.vpc-exe1.vpc_cidr_block]
  # Egress Rule - all-all open
  egress_rules = ["all-all"]
  tags         = local.common_tags
}