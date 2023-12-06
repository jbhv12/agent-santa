variable "env" {
  type    = string
  default = "prod"
}
variable "gcp_project_id" {
  type    = string
  default = "personal-334605"
}
variable "gcs_bucket" {
  type    = string
  default = "jbhv12-personal"
}


variable "chainlit_auth_secret" {
  type = string
  default = "mysecret473dsf89secret47389sret47389s54cre"
}
variable "chainlit_api_key" {
  type = string
  default = "cl_cRhIg03Y49SgjUQV0J4X9ML+fpZCRsFYcjP7A3jbdl8="
}

variable "aws_cognito_user_pool_id" {
    type = string
    default = "us-west-2_s98mQ8kp4"

}
variable "aws_cognito_client_id" {
    type = string
    default = "6sbgbp02gj406maku5hj9cgmlj"

}
variable "openai_api_key" {
    type = string
    default = "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"

}
variable "aws_access_key_id" {
    type = string
    default = "AKIA3UXD3T3U4OYYEP57"

}
variable "aws_secret_access_key" {
    type = string
    default = "fbSomTc73kE/YdKEI7YPj9YriUltLv1cNqR037oL"
}