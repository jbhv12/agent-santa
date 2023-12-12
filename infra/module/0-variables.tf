variable "env" {
  type = string
}
variable "gcp_project_id" {
  type = string
}
variable "gcp_region" {
  type = string
}
variable "gcp_public_resources_bucket" {
  type = string
}
variable "chainlit_auth_secret" {
  type = string
}
variable "chainlit_api_key" {
  type = string
}
variable "serp_api_key" {
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