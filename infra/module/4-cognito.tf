resource "aws_cognito_user_pool" "cognito_pool" {
  name = "red-jingle-users"

  username_attributes = ["email"]
  auto_verified_attributes = ["email"]

  verification_message_template {
    default_email_option = "CONFIRM_WITH_CODE"
    email_message = "Welcome to Red Jingles! Your verification code is {####}."
    email_subject = "Verify Your Red Jingles Account"
  }

  admin_create_user_config {
    allow_admin_create_user_only = false
  }

  schema {
    attribute_data_type = "String"
    name = "email"
    required = true
    string_attribute_constraints {
      min_length = 0
      max_length = 2048
    }
  }

  password_policy {
    minimum_length    = 8
    require_lowercase = true
    require_numbers   = true
    require_symbols   = true
    require_uppercase = true
  }

  email_configuration {
    email_sending_account = "COGNITO_DEFAULT"
  }
}

resource "aws_cognito_user_pool_client" "client" {
  name         = "red-jingles-client"
  user_pool_id = aws_cognito_user_pool.cognito_pool.id

  explicit_auth_flows = [
    "ALLOW_USER_SRP_AUTH",
    "ALLOW_REFRESH_TOKEN_AUTH",
    "ALLOW_USER_PASSWORD_AUTH",
    "ALLOW_ADMIN_USER_PASSWORD_AUTH"
  ]

  generate_secret = true

  allowed_oauth_flows_user_pool_client = true
  allowed_oauth_flows                  = ["code", "implicit"]
  allowed_oauth_scopes                 = ["phone", "email", "openid", "profile", "aws.cognito.signin.user.admin"]

  callback_urls = ["http://localhost:1225/auth/oauth/cognito/callback", "http://localhost:8001/auth/callback", "http://localhost:1225/login-callback"]
  logout_urls   = ["http://localhost:1225/logout"]

  supported_identity_providers = ["COGNITO"]
  default_redirect_uri = "http://localhost:1225/auth/oauth/cognito/callback"
  prevent_user_existence_errors = "ENABLED"
}

resource "aws_cognito_user_pool_domain" "domain" {
  domain       = "redjingles"
  user_pool_id = aws_cognito_user_pool.cognito_pool.id
}

resource "aws_cognito_user_pool_ui_customization" "ui_customization" {
  css        = ".label-customizable {font-weight: 400;}"
  image_file = filebase64("logo.png")
  user_pool_id = aws_cognito_user_pool_domain.domain.user_pool_id
}