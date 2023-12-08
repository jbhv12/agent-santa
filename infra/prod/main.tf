module "capstone" {
  source = "../module"
  env    = var.env
  gcp_project_id = var.gcp_project_id
  gcp_public_resources_bucket = var.gcp_public_resources_bucket

  chainlit_auth_secret = var.chainlit_auth_secret
  chainlit_api_key = var.chainlit_api_key
  aws_cognito_user_pool_id = var.aws_cognito_user_pool_id
  aws_cognito_client_id = var.aws_cognito_client_id
  openai_api_key = var.openai_api_key
  aws_access_key_id = var.aws_access_key_id
  aws_secret_access_key = var.aws_secret_access_key
}