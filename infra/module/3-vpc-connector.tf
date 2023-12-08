resource "google_project_service" "vpcaccess-api" {
  project = var.gcp_project_id
  service = "vpcaccess.googleapis.com"
}

module "vpc" {
  source       = "terraform-google-modules/network/google"
  version      = "~> 8.0"
  project_id   = var.gcp_project_id
  network_name = "serverless-network"
  mtu          = 1460

  subnets = [
    {
      subnet_name   = "serverless-subnet"
      subnet_ip     = "10.10.10.0/28"
      subnet_region = "us-central1"
    }
  ]
}

resource "google_vpc_access_connector" "central_serverless" {
  name          = "central-serverless"
  project       = var.gcp_project_id
  region        = "us-central1"
  subnet {
    name = module.vpc.subnets["us-central1/serverless-subnet"].name
  }
  machine_type  = "e2-micro"
  min_throughput = 200
  max_throughput = 500
}


#module "serverless-connector" {
#  source     = "terraform-google-modules/network/google//modules/vpc-serverless-connector-beta"
#  version    = "~> 8.0"
#  project_id = var.gcp_project_id
#
#  vpc_connectors = [{
#    name           = "central-serverless"
#    region         = "us-central1"
#    subnet_name    = module.vpc.subnets["us-central1/serverless-subnet"].name
#    machine_type   = "e2-micro"  # Downsized machine type
#    min_instances  = 2  # Adjusted based on usage
#    max_instances  = 5  # Adjusted based on usage
#  }]
#
#  depends_on = [
#    google_project_service.vpcaccess-api
#  ]
#}
