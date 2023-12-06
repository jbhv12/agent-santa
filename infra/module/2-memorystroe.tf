#resource "google_redis_instance" "my_memorystore_redis_instance" {
#  name           = "myinstance"
#  tier           = "BASIC"
#  authorized_network = module.test-vpc-module.network_id
#  memory_size_gb = 1
#  region         = "us-central1"
#  redis_version  = "REDIS_6_X"
#}