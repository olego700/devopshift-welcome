variable "subnet_id" {
  description = "Subnet to launch the instance in"
  type        = string
}

variable "instance_type" {
  type = string
}

variable "ami_id" {
  description = "AMI ID for the instance"
  type        = string
  default     = "ami-0c02fb55956c7d316" 
}

variable "assign_public_ip" {
  type        = bool
}