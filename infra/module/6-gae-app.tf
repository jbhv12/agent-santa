resource "google_app_engine_flexible_app_version" "chat_app" {
  project        = var.gcp_project_id
  service        = "default"
  version_id     = formatdate("YY-MM-DD-hh-mm", timestamp())
  runtime        = "custom"
  instance_class = "F1"
  deployment {
    zip {
      source_url = "https://storage.googleapis.com/${google_storage_bucket_object.app_zip.bucket}/${google_storage_bucket_object.app_zip.name}"
    }
  }
  network {
    name             = "projects/${var.gcp_project_id}/global/networks/serverless-network"
    subnetwork       = "serverless-subnet"
    session_affinity = true
  }
  automatic_scaling {
    #    min_idle_instances      = 1
    #    max_idle_instances      = 3
    cpu_utilization {
      target_utilization = 0.9
    }
  }


  env_variables = {
    CHAINLIT_API_KEY      = var.chainlit_api_key
    CHAINLIT_AUTH_SECRET  = var.chainlit_auth_secret
    SERPAPI_API_KEY       = var.serp_api_key
    DISABLE_AUTH          = false
    COGNITO_USER_POOL_ID  = aws_cognito_user_pool.cognito_pool.id
    COGNITO_CLIENT_ID     = aws_cognito_user_pool_client.client.id
    COGNITO_DOMAIN        = "${aws_cognito_user_pool_domain.domain.domain}.auth.us-west-2.amazoncognito.com"
    COGNITO_CLIENT_SECRET = aws_cognito_user_pool_client.client.client_secret
    COGNITO_REDIRECT_URI  = "https://red-jingles.ue.r.appspot.com/auth/oauth/cognito/callback"
    OPENAI_API_KEY        = var.openai_api_key
    REDIS_HOST            = google_redis_instance.redis_instance.host
    REDIS_PORT            = var.redis_port
    REDIS_DB              = var.redis_db
    REDIS_TTL             = var.redis_ttl
  }
  liveness_check {
    path = "readiness_check"
  }
  readiness_check {
    path = "readiness_check"
  }
  lifecycle {
    create_before_destroy = true
  }
  inbound_services = ["INBOUND_SERVICE_WARMUP"]
}

resource "google_app_engine_service_split_traffic" "app_split" {
  service = google_app_engine_flexible_app_version.chat_app.service

  migrate_traffic = false
  split {
    shard_by = "IP"
    allocations = {
      (google_app_engine_flexible_app_version.chat_app.version_id) = 1
    }
  }
}

data "archive_file" "app_zip" {
  type        = "zip"
  source_dir  = "../../app/"
  output_path = "${path.module}/app.zip"
}

resource "google_storage_bucket_object" "app_zip" {
  name   = "src/api-${timestamp()}.zip"
  bucket = "rj-tf-state"
  source = data.archive_file.app_zip.output_path
}