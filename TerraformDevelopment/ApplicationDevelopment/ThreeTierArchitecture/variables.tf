variable "aws_region" {
  type    = string
  default = "ap-southeast-1"
}

variable "instance_type" {
  type    = string
  default = "t2.micro"
}

variable "instance_keypair" {
  type    = string
  default = "terraform-key"
}

# Environment Variable
variable "environment" {
  description = "Environment Variable used as a prefix"
  type        = string
  default     = "dev"
}
# Business Division
variable "business_divison" {
  description = "Business Division in the large organization this Infrastructure belongs"
  type        = string
  default     = "Capital Market"
}