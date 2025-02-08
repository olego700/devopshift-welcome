module "vpc" {
    source = "./modules/vpc"
    cidr_range = 16
    subnet_count = 1
}

module "ec2" {
  source = "./modules/ec2"
  
  subnet_id        = module.vpc.public_subnet_id
  instance_type    = "t2.micro"
  ami_id           = "ami-0c02fb55956c7d316" 
  assign_public_ip = true
}

module "alb" {
  source = "./modules/alb"
  
  vpc_id           = module.vpc.vpc_id
  public_subnet_id = module.vpc.public_subnet_id
}