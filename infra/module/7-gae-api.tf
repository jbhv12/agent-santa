resource "google_app_engine_standard_app_version" "api_app" {
  project     = var.gcp_project_id
  service     = "red-jingles-api"
  version_id  = formatdate("YY-MM-DD-hh-mm", timestamp())
  runtime     = "python311"
  instance_class = "F1"
  deployment {
    zip {
      source_url = "https://storage.googleapis.com/${google_storage_bucket_object.app_zip.bucket}/${google_storage_bucket_object.app_zip.name}"
    }
  }
  entrypoint {
    shell = "gunicorn -b :$PORT -k uvicorn.workers.UvicornWorker api_server:app"
  }
  automatic_scaling {
    min_idle_instances      = 1
    max_idle_instances      = 3
  }

  vpc_access_connector {
    name = "projects/${var.gcp_project_id}/locations/${var.gcp_region}/connectors/central-serverless"
  }

  env_variables = {
    PORT                       = "8080"
    COGNITO_USER_POOL_ID       = aws_cognito_user_pool.cognito_pool.id
    COGNITO_CLIENT_ID          = aws_cognito_user_pool_client.client.id
    COGNITO_DOMAIN             = "${aws_cognito_user_pool_domain.domain.domain}.auth.us-west-2.amazoncognito.com"
    COGNITO_CLIENT_SECRET      = aws_cognito_user_pool_client.client.client_secret
    COGNITO_REDIRECT_URI       = "https://red-jingles-api-dot-red-jingles.ue.r.appspot.com/docs/oauth2-redirect"
    OPENAI_API_KEY             = var.openai_api_key
    REDIS_HOST                 = google_redis_instance.redis_instance.host
    REDIS_PORT                 = var.redis_port
    REDIS_DB                   = var.redis_db
    REDIS_TTL                  = var.redis_ttl
  }
  lifecycle {
    create_before_destroy = true
  }
  inbound_services = ["INBOUND_SERVICE_WARMUP"]
}

resource "google_app_engine_service_split_traffic" "api_split" {
  service = google_app_engine_standard_app_version.api_app.service

  migrate_traffic = true
  split {
    shard_by = "IP"
    allocations = {
      (google_app_engine_standard_app_version.api_app.version_id) = 1
    }
  }
}
