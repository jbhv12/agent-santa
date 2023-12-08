provider "aws" {
  region = "us-west-2"
}

provider "google" {
  project = "personal-334605"
  region  = "us-east1"
}

terraform {
  backend "gcs" {
    bucket = "jbhv12-personal"
    prefix = "terraform/state"
  }
  required_version = "= 1.5.3"
}