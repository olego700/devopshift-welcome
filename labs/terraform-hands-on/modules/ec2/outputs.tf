output "vm_public_ip" {
 value = "ip of the machine: ${aws_instance.vm.public_ip}"
}
