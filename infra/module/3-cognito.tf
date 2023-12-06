#resource "aws_cognito_user_pool" "my_user_pool" {
#  name = "my-user-pool"
#
#  username_attributes = ["email"]
#  auto_verified_attributes = ["email"]
#
#  verification_message_template {
#    default_email_option = "CONFIRM_WITH_CODE"
#  }
#
#  admin_create_user_config {
#    allow_admin_create_user_only = false
#  }
#
#  schema {
#    attribute_data_type = "String"
#    name = "email"
#    required = true
#    string_attribute_constraints {
#      min_length = 0
#      max_length = 2048
#    }
#  }
#
#  password_policy {
#    minimum_length    = 8
#    require_lowercase = true
#    require_numbers   = true
#    require_symbols   = true
#    require_uppercase = true
#  }
#
#  email_configuration {
#    email_sending_account = "COGNITO_DEFAULT"
#  }
#}
#
#resource "aws_cognito_user_pool_client" "client" {
#  name         = "my-user-pool-client"
#  user_pool_id = aws_cognito_user_pool.my_user_pool.id
#
#  explicit_auth_flows = [
#    "ALLOW_USER_SRP_AUTH",
#    "ALLOW_REFRESH_TOKEN_AUTH",
#    "ALLOW_USER_PASSWORD_AUTH",
#    "ALLOW_ADMIN_USER_PASSWORD_AUTH"
#  ]
#
#  generate_secret = false
#
#  allowed_oauth_flows_user_pool_client = true
#  allowed_oauth_flows                  = ["code", "implicit"]
#  allowed_oauth_scopes                 = ["phone", "email", "openid", "profile", "aws.cognito.signin.user.admin"]
#
#  callback_urls = ["http://localhost:1225/login-callback"]
#  logout_urls   = ["https://myapp.com/logout"]
#
#  supported_identity_providers = ["COGNITO"]
#  default_redirect_uri = "http://localhost:1225/login-callback"
#  prevent_user_existence_errors = "ENABLED"
#}
#
#resource "aws_cognito_user_pool_domain" "domain" {
#  domain       = "capstonetestdev" # Replace with your desired domain prefix
#  user_pool_id = aws_cognito_user_pool.my_user_pool.id
#}
