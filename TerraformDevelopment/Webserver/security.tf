# Security Group
resource "aws_security_group" "web_sg" {
  vpc_id = aws_vpc.web_vpc.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "web_sg"
  }
}

# NACL
resource "aws_network_acl" "web_acl" {
  vpc_id = aws_vpc.web_vpc.id
  tags = {
    Name = "web_acl"
  }
}

resource "aws_network_acl_rule" "inbound_http" {
  network_acl_id = aws_network_acl.web_acl.id
  rule_number    = 100
  protocol       = "6"
  rule_action    = "allow"
  cidr_block     = "0.0.0.0/0"
  from_port      = 80
  to_port        = 80
}

resource "aws_network_acl_rule" "outbound_all" {
  network_acl_id = aws_network_acl.web_acl.id
  rule_number    = 200
  protocol       = "-1"
  rule_action    = "allow"
  cidr_block     = "0.0.0.0/0"
}

# IAM Role for EC2
resource "aws_iam_role" "ec2_role" {
  name = "ec2_web_role"
  assume_role_policy = jsonencode({
    "Version": "2012-10-17",
    "Statement": [
      {
        "Action": "sts:AssumeRole",
        "Principal": { "Service": "ec2.amazonaws.com" },
        "Effect": "Allow",
        "Sid": ""
      }
    ]
  })
}

# EC2 Instances
resource "aws_instance" "web_instance" {
  count         = 3
  ami           = var.ami_id
  instance_type = var.instance_type
  subnet_id     = aws_subnet.web_subnet[count.index].id
  vpc_security_group_ids = [aws_security_group.web_sg.id]
  #security_groups = [aws_security_group.web_sg.name]
  #user_data     = file("userdata.sh")
  user_data = <<EOF
    #!/bin/bash
    # Update the system
    sudo yum update -y

    # Install the web server (e.g., Apache)
    sudo yum install -y httpd

    # Start and enable the web server
    sudo systemctl start httpd
    sudo systemctl enable httpd

    # Create an index.html file
    echo "Hello, World!" > /var/www/html/index.html
    EOF
      
  tags = {
    Name = "web_instance_${count.index}"
  }
}

# Load Balancer
resource "aws_lb" "web_lb" {
  name               = "web-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.web_sg.id]
  subnets            = aws_subnet.web_subnet[*].id
}

resource "aws_lb_target_group" "web_tg" {
  name     = "web-tg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = aws_vpc.web_vpc.id
}

resource "aws_lb_listener" "web_listener" {
  load_balancer_arn = aws_lb.web_lb.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.web_tg.arn
  }
}

resource "aws_lb_target_group_attachment" "web_attachment" {
  count            = 3
  target_group_arn = aws_lb_target_group.web_tg.arn
  target_id        = aws_instance.web_instance[count.index].id
  port             = 80
}
