#resource "google_redis_instance" "redis_instance" {
#  name           = "red-jingles-instance"
#  tier           = "BASIC"
#  authorized_network = module.vpc.network_id
#  memory_size_gb = 1
#  region         = "us-central1"
#  redis_version  = "REDIS_6_X"
#}