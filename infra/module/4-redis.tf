#resource "aws_elasticache_cluster" "example" {
#
#  cluster_id           = "cluster-example"
#  engine               = "redis"
#  node_type            = "cache.t3.micro"
#  num_cache_nodes      = 1
#  parameter_group_name = "default.redis7"
#  engine_version       = "7.1"
#  port                 = 6379
#}

#
## Create a security group with full access from outside
#resource "aws_security_group" "example_sg" {
#  name        = "example-sg"
#  description = "Allow all inbound traffic"
#  vpc_id      = module.vpc.vpc_id
#
#  ingress {
#    from_port   = 0
#    to_port     = 0
#    protocol    = "-1"
#    cidr_blocks = ["0.0.0.0/0"]
#  }
#
#  egress {
#    from_port   = 0
#    to_port     = 0
#    protocol    = "-1"
#    cidr_blocks = ["0.0.0.0/0"]
#  }
#
#  tags = {
#    Name = "example-sg"
#  }
#}
#resource "aws_elasticache_subnet_group" "example_subnet_group" {
#  name       = "example-subnet-group"
#  subnet_ids = module.vpc.private_subnets
#
#  tags = {
#    Name = "example-subnet-group"
#  }
#}
## ElastiCache Redis cluster
#resource "aws_elasticache_cluster" "example" {
#  cluster_id           = "cluster-example"
#  engine               = "redis"
#  node_type            = "cache.t3.micro"
#  num_cache_nodes      = 1
#  parameter_group_name = "default.redis7"
#  engine_version       = "7.1"
#  port                 = 6379
#  subnet_group_name    = aws_elasticache_subnet_group.example_subnet_group.name
#  security_group_ids   = [aws_security_group.example_sg.id]
#}

#resource "aws_elasticache_cluster" "example" {
#  cluster_id           = "cluster-example"
#  engine               = "redis"
#  node_type            = "cache.t3.micro"  # Smallest available node type for cost-saving
#  num_cache_nodes      = 1                 # Single node for minimal setup
#  parameter_group_name = "default.redis7"
#  engine_version       = "7.1"
#  port                 = 6379
#
#  # Snapshotting and Backup - Disable if not needed
#  snapshot_retention_limit = 0  # Set to 0 to disable automated backup to reduce costs
#
#  # Apply Security Group - Ensure minimal access for security and cost-effectiveness
#  # security_group_ids = ["<Your-Security-Group-ID>"]  # Uncomment and specify security group if needed
#
#  # Cost-saving by not enabling Multi-AZ (not recommended for production)
#  automatic_failover_enabled = false
#
#  # Disable or minimize reserved cache nodes
#  # reserved_cache_nodes_offering_id = "<Your-Reserved-Instance-Offering-ID>"  # Uncomment and specify if using reserved instances
#
#  # Other settings like maintenance window and notification can be adjusted as per requirement
#}
