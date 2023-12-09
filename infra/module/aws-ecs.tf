## Define the ECS Cluster
#resource "aws_ecs_cluster" "cluster" {
#  name = "my-cluster"
#}
#
## Define the task definition
#resource "aws_ecs_task_definition" "task" {
#  family                   = "my-task-2"
#  network_mode             = "awsvpc"
#  requires_compatibilities = ["FARGATE"]
#  cpu                      = "2048" # 8 vCPU
#  memory                   = "4096" # 16GB
#
#  container_definitions = jsonencode([{
#    name  = "red2"
#    image = "public.ecr.aws/n3y9v4e6/red-jingles:latest"
#    portMappings = [{
#      containerPort = 1225
#    }]
#    environment = [
#      {
#          name = "CHAINLIT_API_KEY"
#          value = var.chainlit_api_key
#        },
#      {
#          name  = "CHAINLIT_AUTH_SECRET"
#          value = var.chainlit_auth_secret
#        },
#      {
#          name  = "COGNITO_USER_POOL_ID"
#          value = var.aws_cognito_user_pool_id
#        },
#         {
#          name  = "COGNITO_CLIENT_ID"
#          value = var.aws_cognito_client_id
#        },
#         {
#          name  = "COGNITO_DOMAIN"
#          value = var.aws_cognito_domain
#        },
#         {
#          name  = "COGNITO_CLIENT_SECRET"
#          value = var.aws_cognito_client_secret
#        }
#        , {
#          name  = "COGNITO_REDIRECT_URI"
#          value = var.aws_cognito_redirect_url
#        }
#    ]
#  }])
#}
#
## IAM roles for ECS tasks
#resource "aws_iam_role" "ecs_execution_role" {
#  name = "ecs_execution_role"
#
#  assume_role_policy = jsonencode({
#    Version = "2012-10-17",
#    Statement = [{
#      Action = "sts:AssumeRole",
#      Effect = "Allow",
#      Principal = {
#        Service = "ecs-tasks.amazonaws.com"
#      },
#    }]
#  })
#}
#
## Define the ECS service
#resource "aws_ecs_service" "service" {
#  name            = "my-service"
#  cluster         = aws_ecs_cluster.cluster.id
#  task_definition = "arn:aws:ecs:us-west-2:856636742446:task-definition/mytask:1" //aws_ecs_task_definition.task.arn
#  launch_type     = "FARGATE"
#   network_configuration {
#    subnets = [aws_subnet.my_subnet1.id, aws_subnet.my_subnet2.id]
#    security_groups = [aws_security_group.public_access_sg.id]
#  }
#
#  load_balancer {
#    target_group_arn = aws_lb_target_group.my_tg.arn
#    container_name   = "red"
#    container_port   = 1225
#  }
#
#  desired_count = 1
#}
#
#resource "aws_iam_role_policy_attachment" "ecs_execution_role_policy" {
#  role       = aws_iam_role.ecs_execution_role.name
#  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
#}
## Attach the custom policy to the ECS execution role
#resource "aws_iam_role_policy_attachment" "ecs_ecr_policy_attachment" {
#  role       = aws_iam_role.ecs_execution_role.name
#  policy_arn = aws_iam_policy.ecs_ecr_policy.arn
#}
#resource "aws_iam_policy" "ecs_ecr_policy" {
#  name        = "ecs_ecr_policy"
#  path        = "/"
#  description = "Policy for ECS tasks to interact with ECR"
#
#  policy = jsonencode({
#    Version = "2012-10-17",
#    Statement = [
#      {
#        Action = [
#          "ecs:*",
#          "ecr:GetDownloadUrlForLayer",
#          "ecr:BatchGetImage",
#          "ecr:BatchCheckLayerAvailability",
#          "ecr:PutImage",
#          "ecr:InitiateLayerUpload",
#          "ecr:UploadLayerPart",
#          "ecr:CompleteLayerUpload",
#          "ecr:DescribeRepositories",
#          "ecr:GetRepositoryPolicy",
#          "ecr:ListImages",
#          "ecr:DescribeImages",
#          "ecr:BatchDeleteImage",
#          "ecr:SetRepositoryPolicy",
#          "ecr:DeleteRepository",
#          "logs:*"
#        ],
#        Effect = "Allow",
#        Resource = "*"
#      }
#    ]
#  })
#}