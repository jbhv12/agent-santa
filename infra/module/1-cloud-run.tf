locals {
 timestamp = timestamp()
}
resource "google_cloud_run_service" "default" {
 name     = "red-jingles-service"
 location = "us-east1"

 template {
   spec {
     containers {
       image = "docker.io/jbhv12/red-jingles:latest"
       ports {
         container_port = 8080
       }
       env {
         name  = "LAST_UPDATED"
         value = local.timestamp
       }
       env {
         name  = "LITERAL_API_KEY"
         value = var.chainlit_api_key
       }
       env {
         name  = "CHAINLIT_AUTH_SECRET"
         value = var.chainlit_auth_secret
       }
       env {
         name  = "OAUTH_COGNITO_CLIENT_ID"
         value = aws_cognito_user_pool_client.client.id
       }
       env {
        name  = "OAUTH_COGNITO_DOMAIN"
        value = format("%s.auth.us-west-2.amazoncognito.com", aws_cognito_user_pool_domain.domain.domain)
       }
       env {
         name  = "OAUTH_COGNITO_CLIENT_SECRET"
         value = aws_cognito_user_pool_client.client.client_secret
       }
       env {
         name  = "CHAINLIT_URL"
         value = "https://red-jingles-service-zo5w7qkf4a-ue.a.run.app"
       }
       env {
         name  = "OPENAI_API_KEY"
         value = var.openai_api_key
       }
       env {
         name  = "REDIS_HOST"
         value = google_redis_instance.redis_instance.host
       }
       env {
         name  = "REDIS_PORT"
         value = var.redis_port
       }
       env {
         name  = "REDIS_DB"
         value = var.redis_db
       }
       env {
         name  = "REDIS_TTL"
         value = var.redis_ttl
       }
       resources {
         limits = {
           cpu    = "8"
           memory = "16Gi"
         }
       }
     }
   }
   metadata {
     annotations = {
       "run.googleapis.com/sessionAffinity" = true
     }
   }
 }

 traffic {
   percent         = 100
   latest_revision = true
 }
}

resource "google_cloud_run_service_iam_member" "public" {
  service     = google_cloud_run_service.default.name
  location    = google_cloud_run_service.default.location
  role        = "roles/run.invoker"
  member      = "allUsers"
}