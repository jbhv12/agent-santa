variable "env" {
  type    = string
}
variable "gcp_project_id" {
  type = string
}


variable "chainlit_auth_secret" {
  type = string
}
variable "chainlit_api_key" {
  type = string
}

variable "aws_cognito_user_pool_id" {
    type = string
}
variable "aws_cognito_client_id" {
    type = string
}
variable "openai_api_key" {
    type = string
}
variable "aws_access_key_id" {
    type = string
}
variable "aws_secret_access_key" {
    type = string
}