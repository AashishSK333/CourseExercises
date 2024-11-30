output "aws_instance_publicip" {
  description = "ec2 instance public ip"
  value = aws_instance.ec2-demo-instance.public_ip
}

output "aws_instance_privateip" {
  description = "ec2 private ip address"
  value = aws_instance.ec2-demo-instance.private_ip
}