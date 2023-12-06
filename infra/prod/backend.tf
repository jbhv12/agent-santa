provider "aws" {
  region = "us-west-2"
}

provider "google" {
  project = "personal-334605"
  region  = "us-east1"
}

terraform {
  #  backend "s3" {
  #    profile = "haiku_dev"
  #    bucket  = "haiku-tf-state-bucket"
  #    key     = "range_infra/capstone/terraform.tfstate"
  #    region  = "us-west-2"
  #  }
  backend "gcs" {
    bucket = "jbhv12-personal"
    prefix = "terraform/state"
  }
  required_version = ">= 0.13"
}