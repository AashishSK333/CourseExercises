variable "aws_region" {
  type = string
  default = "ap-southeast-1"
}

variable "instance_type" {
  type = string
  default = "t2.micro"
}

variable "instance_keypair" {
  type = string
  default = "terraform-key"
}