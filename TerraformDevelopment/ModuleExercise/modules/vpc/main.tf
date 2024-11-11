resource "aws_vpc" "main_vpc" {
  cidr_block = var.cidr_block
  enable_dns_hostnames = true
  tags = {
    Name = var.vpc_name
    Terraform = "True"
  }
}

resource "aws_subnet" "main_subnet" {
  vpc_id = aws_vpc.main_vpc.id
  cidr_block = var.subnet_cidr_block
  availability_zone = var.availability_zone
  tags = {
    Name = var.subnet_name
    Terraform = "True"
  }
}
/*
output "vpc_id" {
  value = aws_vpc.main_vpc.id
}*/
