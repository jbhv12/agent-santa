provider "aws" {
  region = "us-west-2"
}

provider "google" {
  project = "red-jingles"
  region  = "us-east1"
}

terraform {
  backend "gcs" {
    bucket = "rj-tf-state"
    prefix = "terraform"
  }
  required_version = "= 1.6.5"
}