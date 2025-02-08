
#create vpc wiht cidr range from the user input
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/${var.cidr_range}"
  enable_dns_support = true
  enable_dns_hostnames = true
  tags = {
    Name = "Main VPC"
  }
}
#create public subnet
resource "aws_subnet" "public" {
  vpc_id     = aws_vpc.main.id
  cidr_block = var.public_subnet_ad
  map_public_ip_on_launch = true

  tags = {
    Name = "Public Subnet"
  }
}
#create private subnet
resource "aws_subnet" "private" {
  vpc_id     = aws_vpc.main.id
  cidr_block = var.private_subnet_ad
  
  tags = {
    Name = "Private Subnet"
  }
}

#create internet gateway for the vpc
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "Main IGW"
  }
}

#create public Route Table
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "Public Route Table"
  }
}

#public Route (Allow Internet Access)
resource "aws_route" "public_route" {
  route_table_id         = aws_route_table.public.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.main.id
}

#associate Public Subnets with Public Route Table
resource "aws_route_table_association" "public" {
  count = var.subnet_count

  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public.id
}

#private Route Table (No Internet Access)
resource "aws_route_table" "private" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "Private Route Table"
  }
}

#associate Private Subnets with Private Route Table
resource "aws_route_table_association" "private" {
  count = var.subnet_count

  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.private.id
}
