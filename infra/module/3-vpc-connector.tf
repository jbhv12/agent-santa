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
      subnet_region = "asia-south1"
    }
  ]
}