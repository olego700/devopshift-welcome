# variable "vpc_cidr" {
#   type        = string
#   default     = "10.0.0.0/16"
# }
variable "cidr_range" {
}


variable "public_subnet_ad" {
  type        = string
  default     = "10.0.1.0/24"
}

variable "private_subnet_ad" {
  type        = string
  default     = "10.0.2.0/24"
}

variable "subnet_count" {
  
}

variable "availability_zones" {
  type        = list(string)
  default     = ["us-east-1a", "us-east-1b"]
}