variable "ec2-instance-type" {
  type    = string
  default = "t2.micro"
}

variable "private_instance_count" {
  type    = number
  default = 1
}