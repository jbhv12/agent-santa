## This service account is used for automation in Github Actions, we need to fetch key from console and set Github secret manually

resource "google_service_account" "terraform_account" {
  account_id   = "terraform-account"
  display_name = "Terraform Account"
}

# Grant the service account editor role to manage most resources
resource "google_project_iam_member" "terraform_account_editor" {
  project = "personal-334605"
  role    = "roles/editor"
  member  = "serviceAccount:${google_service_account.terraform_account.email}"
}