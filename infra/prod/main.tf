module "capstone" {
  source                      = "../module"
  env                         = var.env
  gcp_project_id              = var.gcp_project_id
  gcp_region                  = var.gcp_region
  gcp_public_resources_bucket = var.gcp_public_resources_bucket

  serp_api_key         = var.serp_api_key
  chainlit_auth_secret = var.chainlit_auth_secret
  chainlit_api_key     = var.chainlit_api_key

  openai_api_key = var.openai_api_key
    
  redis_port = var.redis_port
  redis_db   = var.redis_db
  redis_ttl  = var.redis_ttl
}