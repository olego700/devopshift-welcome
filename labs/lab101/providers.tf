provider "aws" {
  region = us-east-1
}

terraform {
  required_providers {
    time = {
      source = "hashicorp/time"
      version = "0.12.1"
    }
  }
}

