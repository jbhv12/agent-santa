variable "env" {
  type    = string
  default = "prod"
}
variable "gcp_region" {
  type = string
  default = "us-east1"
}
variable "gcp_public_resources_bucket" {
  type    = string
}

variable "redis_port" {
  type    = string
  default = "6379"
}
variable "redis_db" {
  type    = string
  default = "0"
}
variable "redis_ttl" {
  type    = string
  default = "600"
}

variable "openai_api_key" {
  type    = string
}
variable "gcp_project_id" {
  type    = string
}
variable "chainlit_auth_secret" {
  type    = string
}
variable "chainlit_api_key" {
  type    = string
}