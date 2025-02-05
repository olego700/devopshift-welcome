
provider "aws" {
  region = var.region
}

variable "region" {
  default = "us-east-1"
}


# variable "varcheck" {
#   default = ""
# }



# resource "null_resource" "check_var" {
#   provisioner "local-exec" {
#     command = <<EOT
#       if [ -z "${var.varcheck}" ]; then
#         echo "ERROR: var was not assigned." >&2
#         exit 1
#         else
#         echo "var not empty"
#       fi
#     EOT
#   }
#   #depends_on = [aws_instance.vm]
# }

data "aws_instance" "machine_ip" {
  instance_id = "i-09df7e0ed385f871b"
}

output "instance_ip" {
  value = data.aws_instance.machine_ip.public_ip
}
