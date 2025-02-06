provider "aws" {
 region = var.region
}


variable "region" {
}


# Mocked IP var
# variable "ipsetup" {
#     default =aws_instance.vm.public_ip
# }

variable "amisetup" {
  
}
variable "instance_type_setup" {
  
}

resource "aws_security_group" "sg" {
 ingress {
   from_port   = 22
   to_port     = 22
   protocol    = "tcp"
   cidr_blocks = ["0.0.0.0/0"]
 }


 egress {
   from_port   = 0
   to_port     = 0
   protocol    = "-1"
   cidr_blocks = ["0.0.0.0/0"]
 }
}

variable "machine_name" {
  
}

resource "aws_instance" "vm" {
  ami           = var.amisetup
 instance_type = var.instance_type_setup


 vpc_security_group_ids = [aws_security_group.sg.id]


 tags = {
   Name = var.machine_name
 }
}


output "publicip_output" {
  value = "the public ip is: ${aws_instance.vm.public_ip}"
}

output "ami_output" {
  value = "the ami is: ${var.amisetup}"
}

output "region_output" {
  value = "the region is: ${var.region}"
}

variable "enabled_services" {
    
  type = list(string)
  default = ["prod"]
}

variable "s3_buckets" {
  type    = set(string)
  default = ["prod", "dev"]

}

resource "aws_s3_bucket" "buckets" {
  for_each ={for key in var.s3_buckets : key => key if contains(var.enabled_services, key) }

  bucket = "my-app-${each.key}"
  acl    = "private"

  tags = {
    Name        = "Bucket for ${each.key}"
    Environment = "${each.key}"
  }
}


output "vm_public_ip" {
 value       = aws_instance.vm.public_ip
 description = "Public IP address of the VM"
 depends_on = [ null_resource.check_public_ip ]
}


resource "null_resource" "check_public_ip" {
 provisioner "local-exec" {
   command = <<EOT
     if [ -z "${aws_instance.vm.public_ip}" ]; then
       echo "ERROR: Public IP address was not assigned." >&2
       exit 1
       else
       echo "We got the IP! ${aws_instance.vm.public_ip}"
     fi
   EOT
 }


 depends_on = [aws_instance.vm]
}
