resource "aws_instance" "ec2demo" {
  ami = "ami-0f935a2ecd3a7bd5c"
  instance_type = "t2.micro"
  user_data = file("${path.module}/app1-install.sh")
  tags = {
    Name = "EC2 Instance"
    Terraform = "True"
  }
}
/*
#Define the VPC
resource "aws_vpc" "vpc" {
  cidr_block = var.vpc_cidr

  tags = {
    Name        = var.vpc_name
    Environment = "demo_environment"
    Terraform   = "true"
  }
}*/