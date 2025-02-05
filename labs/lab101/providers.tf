provider "aws" {
  region = var.region
}

terraform {
  required_providers {
    time = {
      source = "hashicorp/time"
      version = "0.12.1"
    }
  }
}

