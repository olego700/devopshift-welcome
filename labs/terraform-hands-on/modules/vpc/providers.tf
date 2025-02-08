terraform {
  required_providers {
    time = {
      source = "hashicorp/time"
      version = "0.12.1"
    }
  }
}
provider "aws" {
  region = "us-east-1"
}
