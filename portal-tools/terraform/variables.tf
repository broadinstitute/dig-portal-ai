variable "project_id" {
  type        = string
  description = "GCP project ID"
}

variable "region" {
  type        = string
  default     = "us-central1"
}

variable "service_name" {
  type        = string
  default     = "tool-backend"
}

variable "image_url" {
  type        = string
  description = "URL of the container image in Artifact Registry or GCR"
}
