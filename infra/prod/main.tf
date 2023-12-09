module "capstone" {
  source                      = "../module"
  env                         = var.env
  gcp_project_id              = var.gcp_project_id
  gcp_public_resources_bucket = var.gcp_public_resources_bucket

  chainlit_auth_secret = var.chainlit_auth_secret
  chainlit_api_key     = var.chainlit_api_key

  aws_cognito_user_pool_id  = var.aws_cognito_user_pool_id
  aws_cognito_client_id     = var.aws_cognito_client_id
  aws_cognito_domain        = var.aws_cognito_domain
  aws_cognito_client_secret = var.aws_cognito_client_secret
  aws_cognito_redirect_url  = var.aws_cognito_redirect_url

  openai_api_key = var.openai_api_key

  redis_port = var.redis_port
  redis_db   = var.redis_db
  redis_ttl  = var.redis_ttl
}