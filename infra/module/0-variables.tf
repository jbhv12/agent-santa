variable "env" {
  type = string
}
variable "gcp_project_id" {
  type = string
}
variable "gcp_public_resources_bucket" {
  type = string
}
variable "aws_cognito_user_pool_id" {
  type = string
}
variable "aws_cognito_client_id" {
  type = string
}
variable "aws_cognito_domain" {
  type = string
}
variable "aws_cognito_client_secret" {
  type = string
}
variable "aws_cognito_redirect_url" {
  type = string
}
variable "chainlit_auth_secret" {
  type = string
}
variable "chainlit_api_key" {
  type = string
}
variable "openai_api_key" {
  type = string
}
variable "redis_port" {
  type = string
}

variable "redis_db" {
  type = string
}
variable "redis_ttl" {
  type = string
}