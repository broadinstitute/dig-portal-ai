provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_cloud_run_v2_service" "backend" {
  name     = var.service_name
  location = var.region
  ingress  = "INGRESS_TRAFFIC_ALL"

  deletion_protection = false


  template {
    containers {
      image = var.image_url
      ports {
        container_port = 8080
      }
    }
  }

  traffic {
    percent         = 100
    type            = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
  }
}

resource "google_cloud_run_service_iam_member" "run_invoker" {
  location = "us-central1"
  project  = "simage-main"
  service  = google_cloud_run_v2_service.backend.name

  role   = "roles/run.invoker"
  member = "allUsers"
}
