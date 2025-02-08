# Terraform Infrastructure Deployment

## 📌 Overview

This Terraform project provisions a complete cloud infrastructure on AWS, including:

- A **Custom VPC** with public and private subnets
- An **EC2 instance** with user-defined AMI and instance type
- An **Application Load Balancer (ALB)** with auto-scaling

## 🛠️ Prerequisites

Before running Terraform, ensure you have:
-if you wish to change the VPC CIDR range you can change it in the module
-you can change the instance type and the ami
-you can control if to assigne public ip or not with True or False

- **Terraform v1.x+** installed → [Download Terraform](https://developer.hashicorp.com/terraform/downloads)
- **AWS CLI** installed & configured (`aws configure`)
- **IAM Permissions** to create VPCs, EC2, and ALB resources

## 🚀 Deployment Steps

### 1️⃣ Initialize Terraform

```sh
terraform init
```
