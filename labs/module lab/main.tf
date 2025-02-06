module "ec2_setup" {
  source = "./modules/ec2"
  amisetup = "ami-0c02fb55956c7d316"
  region = "us-east-1"
  instance_type_setup = "t2.micro"
  machine_name = "oleg-vm"

}

output "printingmpduleinfo" {
    value = module.ec2_setup

}