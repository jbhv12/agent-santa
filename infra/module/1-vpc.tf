#module "vpc" {
#  source  = "terraform-aws-modules/vpc/aws"
#  version = "5.1.0"
#
#  name = "capstone-test-vpc"
#  cidr = "10.75.0.0/16"
#
#  azs             = ["us-west-2a", "us-west-2b"]
#  private_subnets = ["10.75.101.0/24", "10.75.102.0/24"]
#  public_subnets  = ["10.75.1.0/24", "10.75.2.0/24"]
#
#  enable_nat_gateway = true
#  enable_vpn_gateway = true
#
#  enable_dns_hostnames = true
#  enable_dns_support   = true
#
#  tags = {
#    Terraform   = "true"
#    Environment = var.env
#  }
#}