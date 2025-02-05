variable "varcheck" {
  default = "test"
}



resource "null_resource" "check_var" {
  provisioner "local-exec" {
    command = <<EOT
      if [ -z "${var.varcheck}" ]; then
        echo "ERROR: var was not assigned." >&2
        exit 1
      else  
      fi
    EOT
  }
}

