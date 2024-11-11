provider "aws" {
  region     = "ap-southeast-1"
}

module "vpc" {
  source            = "./modules/vpc"
  cidr_block        = "10.0.0.0/16"
  subnet_cidr_block = "10.0.1.0/24"
  vpc_name          = "zta-demo-vpc"
  subnet_name       = "zta-demo-subnet"
  availability_zone = "ap-southeast-1a"
}

module "ec2" {
  source = "./modules/ec2"
  ami_id = "ami-08f49baa317796afd"
  instance_type = "t2.micro"
  subnet_id = module.vpc.subnet_id
  instance_name = "zta-instance"
}