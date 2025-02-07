variable "subnet_id" {
  description = "Subnet to launch the instance in"
  type        = string
}

variable "instance_type" {
  
}

variable "ami_id" {
  description = "AMI ID for the instance"
  type        = string
  default     = "ami-0c55b159cbfafe1f0"  # Ubuntu 22.04
}

variable "assign_public_ip" {
  type        = bool
}