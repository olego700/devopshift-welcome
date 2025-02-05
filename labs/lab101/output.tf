output "vm_public_ip" {
  value       = aws_instance.vm.public_ip
  depends_on  = [time_sleep.wait_for_ip]  # Wait for the time_sleep resource to complete
  description = "Public IP address of the VM"
}

resource "null_resource" "with_triggers" {
  triggers = {
    build_number = "1.0.0"
  }

  provisioner "local-exec" {
    command = "echo 'Triggered on build number 1.0.0'"
  }
}
resource "null_resource" "after_vm" {
  depends_on = [aws_instance.vm]
  provisioner "local-exec" {
    command = "echo 'VM is created, now running commands.'"
  }
}
