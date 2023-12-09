## Create a VPC (if you don't already have one)
#resource "aws_vpc" "my_vpc" {
#  cidr_block = "10.0.0.0/16"
#  enable_dns_hostnames = true
#
#  tags = {
#    Name = "my_vpc"
#  }
#}
#
## Create an Internet Gateway (for public internet access)
#resource "aws_internet_gateway" "gw" {
#  vpc_id = aws_vpc.my_vpc.id
#
#  tags = {
#    Name = "my_gateway"
#  }
#}
#
## Existing subnet in the first Availability Zone
#resource "aws_subnet" "my_subnet1" {
#  vpc_id            = aws_vpc.my_vpc.id
#  cidr_block        = "10.0.1.0/24"
#  availability_zone = "us-west-2a"  # Example Availability Zone
#  map_public_ip_on_launch = true
#
#  tags = {
#    Name = "my_subnet1"
#  }
#}
#
## New subnet in a different Availability Zone
#resource "aws_subnet" "my_subnet2" {
#  vpc_id            = aws_vpc.my_vpc.id
#  cidr_block        = "10.0.2.0/24"
#  availability_zone = "us-west-2b"  # Different Availability Zone
#  map_public_ip_on_launch = true
#
#  tags = {
#    Name = "my_subnet2"
#  }
#}
#
## Create a Security Group that allows public access
#resource "aws_security_group" "public_access_sg" {
#  name        = "public_access_sg"
#  description = "Allow public access"
#  vpc_id      = aws_vpc.my_vpc.id
#
#  ingress {
#    cidr_blocks = ["0.0.0.0/0"]
#    from_port   = 0
#    to_port     = 0
#    protocol    = "-1"
#  }
#  egress {
#    from_port   = 0
#    to_port     = 0
#    protocol    = "-1"
#    cidr_blocks = ["0.0.0.0/0"]
#  }
#
#  tags = {
#    Name = "public_access_sg"
#  }
#}