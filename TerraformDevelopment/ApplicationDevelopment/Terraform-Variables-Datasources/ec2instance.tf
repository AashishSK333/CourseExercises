resource "aws_instance" "ec2-demo-instance" {
  ami = data.aws_ami.awslinux2.id
  instance_type = var.instance_type
  user_data = file("${path.module}/app1-install.sh")

  vpc_security_group_ids = [
    aws_security_group.vpc-ssh.id,
    aws_security_group.vpc-web.id
  ]

  tags = {
    Name = "EC2 Demo Instance"
    Terraform = "True"
  }
}