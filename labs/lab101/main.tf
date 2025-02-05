variable "region" {
  default = "us-east-1"
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

resource "aws_instance" "vm" {
  ami           = "ami-0c02fb55956c7d316"
  instance_type = "t2.micro"

  vpc_security_group_ids = [aws_security_group.sg.id]

  tags = {
    Name = "oleg-vm"
  }
}


resource "time_sleep" "wait_for_ip" {
  create_duration = "10s"  # Wait for 10 seconds
}

# resource "null_resource" "run_script" {
#   provisioner "local-exec" {
#     command = "echo 'Running a script after provisioning.'"
#   }
# }

variable "varcheck" {
  default = ""
}

resource "null_resource" "check_public_ip" {
  provisioner "local-exec" {
    environment = {
      PUBLIC_IP = aws_instance.vm.public_ip
    }
    command = <<EOT
      if [ -z "${aws_instance.vm.public_ip}" ]; then
        echo "ERROR: Public IP address was not assigned." >&2
        exit 1
        else
        echo "IP is $PUBLIC_IP"
      fi
    EOT
  }

  depends_on = [aws_instance.vm]
}



# resource "null_resource" "with_triggers" {
#   triggers = {
#     build_number = "1.0.0"
#   }
#   provisioner "local-exec" {
#     command = "echo 'Triggered on build number 1.0.0'"
#   }
# }

# resource "null_resource" "after_vm" {
#   depends_on = [aws_instance.vm]
#   provisioner "local-exec" {
#     command = "echo 'VM is created, now running commands.'"
#   }
# }
