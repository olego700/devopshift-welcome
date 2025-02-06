variable "create_vpc" {
  type    = bool
  default = true
}

variable "create_ec2" {
  type    = bool
  default = true
}

variable "your_name" {

}

resource "aws_vpc" "custom_vpc" {
  count = var.create_vpc ? 1 : 0
  
  cidr_block = "10.0.0.0/16"
  enable_dns_support = true
  enable_dns_hostnames = true
  tags = {
    Name = "${var.your_name}-vpc"
  }
}


resource "aws_instance" "example" {
  count = var.create_ec2 ? 1 : 0
  # please add a public ip to the machine (USE GOOGLE INSTEAD OF CHATGPT)

  ami           = "ami-0c02fb55956c7d316" # Ubuntu AMI
  instance_type = "t2.micro"

  subnet_id = var.create_vpc ? aws_subnet.custom_subnet[0].id : data.aws_subnet.default.id

  tags = {
    Name = "${var.your_name}-ec2"
  }
    associate_public_ip_address = true
  # Make sure that if i'm using a deafult vpc ... this wont cause an issue ...
  depends_on = [aws_vpc.custom_vpc]
}

resource "aws_subnet" "custom_subnet" {
  count = var.create_vpc ? 1 : 0
  
  vpc_id            = aws_vpc.custom_vpc[0].id
  cidr_block        = "10.0.1.0/24"
  map_public_ip_on_launch = true

  tags = {
    Name = "${var.your_name}-subnet"
  }
}

data "aws_vpc" "default" {
  default = true
}

variable "az_list" {
  default = ["us-east-1a","us-east-1b","us-east-1c"]
}

resource "random_shuffle" "random_az" {
  input = var.az_list
  result_count = 1
}

data "aws_subnet" "default" {
#   vpc_id = data.aws_vpc.default.id

#   # Add a filter to specify the availability zone
#   availability_zone = "us-east-1a"  # Adjust this to the correct availability zone

  filter {
    name   = "default-for-az"
    values = ["true"]
  }
  filter {
    name="availability-zone"
    values = [random_shuffle.random_az.result[0]]
  }
}

# OUTPUTS : please print to machine ip and [vpcid + subnetid] using the following "The following is your {VPCID} and {SUBNET}"

output "instance_ip_and_vpc_subnet" {
  value = "The instance IP is ${aws_instance.example[0].public_ip}, VPCID: ${aws_vpc.custom_vpc[0].id}, SubnetID: ${aws_subnet.custom_subnet[0].id}"
}