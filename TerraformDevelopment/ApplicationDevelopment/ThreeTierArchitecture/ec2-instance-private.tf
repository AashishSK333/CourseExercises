module "ec2-private-instance" {
  source  = "terraform-aws-modules/ec2-instance/aws"
  version = "5.7.1"

  # Meta argument depends_on
  depends_on = [module.vpc-exe1]

  name = "${var.environment}-private-instance"

  ami = data.aws_ami.amilinux2.id

  instance_type = var.ec2-instance-type
  #key_name               = "user1"
  monitoring             = true
  vpc_security_group_ids = [module.public_bastion_sg.security_group_id]
  for_each = toset([ "0", "1" ])
  subnet_id = element(module.vpc-exe1.private_subnets, tonumber(each.key))


  user_data = file("${path.module}/app1-install.sh")

  tags = local.common_tags

}