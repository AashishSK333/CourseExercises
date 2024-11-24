variable "region" {
  default = "ap-southeast-1"
}

variable "vpc_cidr" {
  default = "10.0.0.0/16"
}

variable "subnet_cidr" {
  type = list(string)
  default = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
}

variable "instance_type" {
  default = "t2.micro"
}

variable "ami_id" {
  description = "AMI ID for AWS Linux"
  default     = "ami-07c9c7aaab42cba5a"  # Example AWS Linux AMI for eu-west-3
}

variable "html_content" {
  default = "<html><body><h1>Welcome to Terraform Web Server</h1></body></html>"
}
