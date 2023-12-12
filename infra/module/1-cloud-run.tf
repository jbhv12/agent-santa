#locals {
#  timestamp = timestamp()
#}
#resource "google_cloud_run_service" "default" {
#  name     = "red-jingles-service"
#  location = "us-east1"
#
#  template {
#    spec {
#      containers {
#        image = "docker.io/jbhv12/red-jingles:latest"
#        ports {
#          container_port = 1225
#        }
#        env {
#          name  = "LAST_UPDATED"
#          value = local.timestamp
#        }
#        env {
#          name  = "CHAINLIT_API_KEY"
#          value = var.chainlit_api_key
#        }
#        env {
#          name  = "CHAINLIT_AUTH_SECRET"
#          value = var.chainlit_auth_secret
#        }
#        env {
#          name  = "COGNITO_USER_POOL_ID"
#          value = var.aws_cognito_user_pool_id
#        }
#        env {
#          name  = "COGNITO_CLIENT_ID"
#          value = var.aws_cognito_client_id
#        }
#        env {
#          name  = "COGNITO_DOMAIN"
#          value = var.aws_cognito_domain
#        }
#        env {
#          name  = "COGNITO_CLIENT_SECRET"
#          value = var.aws_cognito_client_secret
#        }
#        env {
#          name  = "COGNITO_REDIRECT_URI"
#          value = var.aws_cognito_redirect_url
#        }
#        env {
#          name  = "OPENAI_API_KEY"
#          value = var.openai_api_key
#        }
#        env {
#          name  = "REDIS_HOST"
#          value = google_redis_instance.redis_instance.host
#        }
#        env {
#          name  = "REDIS_PORT"
#          value = var.redis_port
#        }
#        env {
#          name  = "REDIS_DB"
#          value = var.redis_db
#        }
#        env {
#          name  = "REDIS_TTL"
#          value = var.redis_ttl
#        }
#        resources {
#          limits = {
#            cpu    = "8"
#            memory = "16Gi"
#          }
#        }
#      }
#    }
#    metadata {
#      annotations = {
#        "run.googleapis.com/sessionAffinity" = true
#      }
#    }
#  }
#
#  traffic {
#    percent         = 100
#    latest_revision = true
#  }
#}
#
#
## IAM policy to make the service public
#resource "google_cloud_run_service_iam_policy" "public" {
#  location = google_cloud_run_service.default.location
#  project  = google_cloud_run_service.default.project
#  service  = google_cloud_run_service.default.name
#
#  policy_data = <<EOF
#  {
#    "bindings": [
#      {
#        "role": "roles/run.invoker",
#        "members": [
#          "allUsers"
#        ]
#      }
#    ]
#  }
#  EOF
#}