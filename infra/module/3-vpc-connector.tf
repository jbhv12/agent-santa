#resource "google_project_service" "vpcaccess-api" {
#  project = var.gcp_project_id
#  service = "vpcaccess.googleapis.com"
#}
#
#module "vpc" {
#  source       = "terraform-google-modules/network/google"
#  version      = "~> 8.0"
#  project_id   = var.gcp_project_id # Replace this with your project ID in quotes
#  network_name = "serverless-network"
#  mtu          = 1460
#
#  subnets = [
#    {
#      subnet_name   = "serverless-subnet"
#      subnet_ip     = "10.10.10.0/28"
#      subnet_region = "us-central1"
#    }
#  ]
#}
#
#module "serverless-connector" {
#  source     = "terraform-google-modules/network/google//modules/vpc-serverless-connector-beta"
#  version    = "~> 8.0"
#  project_id = var.gcp_project_id
#
#  vpc_connectors = [{
#    name           = "central-serverless"
#    region         = "us-central1"  # Consider changing the region based on cost
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
