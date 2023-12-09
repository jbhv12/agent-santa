## Load Balancer using the created VPC, Subnet, and Security Group
#resource "aws_lb" "my_alb" {
#  name               = "my-alb"
#  internal           = false
#  load_balancer_type = "application"
#  security_groups    = [aws_security_group.public_access_sg.id]
#  subnets            = [aws_subnet.my_subnet1.id, aws_subnet.my_subnet2.id]
#
#  enable_deletion_protection = false
#}
#
## Target Group for the Load Balancer
#resource "aws_lb_target_group" "my_tg" {
#  name     = "my-tg"
#  port     = 80
#  protocol = "HTTP"
#  vpc_id   = aws_vpc.my_vpc.id
#  target_type = "ip"
#}
#
#resource "aws_lb_listener" "my_listener" {
#  load_balancer_arn = aws_lb.my_alb.arn
#  port              = 80
#  protocol          = "HTTP"
#
#  default_action {
#    type             = "forward"
#    target_group_arn = aws_lb_target_group.my_tg.arn
#  }
#}
