module "ec2-public-instance" {
  source  = "terraform-aws-modules/ec2-instance/aws"
  version = "5.7.1"

  name = "${var.environment}-bastion-instance"

  ami = data.aws_ami.amilinux2.id

  instance_type = var.ec2-instance-type
  #key_name               = "user1"
  monitoring             = true
  vpc_security_group_ids = [module.public_bastion_sg.security_group_id]
  subnet_id              = module.vpc-exe1.public_subnets[0]

  tags = local.common_tags
}