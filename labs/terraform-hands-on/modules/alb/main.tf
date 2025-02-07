

resource "aws_lb" "app_lb" {
  name               = "application-lb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb_sg.id]
  subnets            = [var.public_subnet_id]
}


resource "aws_security_group" "alb_sg" {
  name        = "alb-security-group"
  description = "Security group for ALB"
  vpc_id      = var.vpc_id

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
}

resource "aws_launch_configuration" "web_config" {
  name_prefix   = "web-launch-config"
  image_id      = "ami-0c55b159cbfafe1f0"  # Ubuntu 22.04
  instance_type = "t2.micro"
}

resource "aws_autoscaling_group" "web_asg" {
  name                 = "web-asg"
  launch_configuration = aws_launch_configuration.web_config.name
  min_size             = 1
  max_size             = 3
  desired_capacity     = 2

  vpc_zone_identifier = [var.public_subnet_id]
}