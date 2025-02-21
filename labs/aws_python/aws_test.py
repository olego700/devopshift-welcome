import json
import os
import boto3
import time
from jinja2 import Template
from python_terraform import Terraform

AMI_OPTIONS = {
    "1": "ami-0dee1ac7107ae9f8c",  
    "2": "ami-0f1a6835595fb9246"  
}

INSTANCE_TYPES = ["t3.small", "t3.medium"]
REGION = "us-east-1" 
AVAILABILITY_ZONES=["us-east-1a", "us-east-1b"]

# user Input Function
def get_user_input() -> dict[str,str]:
    while True:
        try:
            ami_choice = input("Select AMI:\n1) Ubuntu\n2) Amazon Linux\nEnter choice (1/2): ").strip()
            if ami_choice in AMI_OPTIONS:
                ami = AMI_OPTIONS[ami_choice]
                break
            else:
                raise ValueError("invalid choice")
        except ValueError as e:
            print(e)
    while True:
        try:
            instance_type=input("enter instance type (t3.small / t3.medium):").strip()
            if instance_type in INSTANCE_TYPES:
                break
            else:
                raise ValueError("invalid instance type only t3.small or t3.medium")
        except ValueError as e:
            print(e)
    
    region=input("please enter a region (cannot be different than 'us-east-1'):").strip().lower()
    if region == REGION:
         print("setting region as 'us-east-1'")
    else:
         print("not a valid region...defaulting to 'us-east-1'")
         region=REGION   

    try:
        av_zone_choice=input("enter availability zone\n 1) us-east-1a\n 2) us-east-1b\n enter choice(1/2):")
        if av_zone_choice=="1":
            availability_zone=AVAILABILITY_ZONES[0]
            print("us-east-1a selected")
        elif av_zone_choice=="2":
            availability_zone=AVAILABILITY_ZONES[1]
            print("us-east-1b selected")
        else:
            raise ValueError("invalid selection")
    except ValueError as e:
        print(f"{e} defaulting to us-east-1a")
        availability_zone=AVAILABILITY_ZONES[0]

                 
    try:
        load_balancer_name=input("enter load balancer name or press enter for default name:").strip()
        if not load_balancer_name:
            raise ValueError("load balancer name cannot be empty...")
    except ValueError as e:
        print(f"{e} default name 'my-alb' will be given")
        load_balancer_name="my-alb"
    return { 
        "ami": ami,
        "instance_type": instance_type,
        "region": region,
        "availability_zone": availability_zone, 
        "load_balancer_name": load_balancer_name
    }

# Generate Terraform file using Jinja2
def generate_terraform_config(user_input: dict[str, str]) -> None:
    try:
        # print the current working directory
        current_directory = os.getcwd()
        print(f"Current working directory: {current_directory}")
        
        # list files in the current directory
        files_in_directory = os.listdir(current_directory)
        print(f"Files in the current directory: {files_in_directory}")
        
        # check if the template file exists
        template_path = "terraform_template.j2"
        if template_path not in files_in_directory:
            raise Exception(f"{template_path} file not found. Please ensure it exists in the current directory.")
        
        print(f"Loading template from {template_path}")
        with open(template_path, "r") as f:
            template_content = f.read()
        
        print("template file read successfully.")
        
        # Debugging the user input
        print(f"User input: {user_input}")
        
        # create and render the template with explicit error handling
        try:
            template = Template(template_content)
            terraform_config = template.render(**user_input)
            print(f"Template variables used: {user_input}")
        except Exception as e:
            raise Exception(f"Template rendering failed: {str(e)}")
        
        # Debug the rendered Terraform config
        print(f"Rendered Terraform Configuration: {terraform_config}")
        
        # Write the rendered configuration
        with open("main.tf", "w") as f:
            f.write(terraform_config)
            print("Terraform configuration written to main.tf.")
            
        # Check if the file has content
        with open("main.tf", "r") as f:
            file_content = f.read()
            print(f"Content of main.tf: {file_content}")
            
    except Exception as e:
        raise Exception(f"Error generating Terraform configuration: {str(e)}")

# Execute Terraform Commands
def deploy_infrastructure():
    try:
        tf = Terraform()
        try:
            tf.init()
            print("Terraform initialized!")
        except Exception as e:
            print("Error initializing Terraform:", e)
        try:
            tf.plan()
            print("Terraform plan complete!")
        except Exception as e:
            print("Error planning Terraform deployment:", e)
        
        return_code, stdout, stderr = tf.apply(skip_plan=True, auto_approve=True)
        print("Terraform apply complete!")
        
        if return_code != 0:
            print("Terraform deployment failed:", stderr)
            exit(1)
        
        # Get outputs
        return_code, stdout, stderr = tf.output(capture_output=True, json_format=True)
        if return_code != 0:
            raise Exception(f"Failed to get Terraform outputs: {stderr}")
            
        outputs = json.loads(stdout)
        return outputs
    except Exception as e:
        print("Error deploying infrastructure:", e)
        destroy_infrastructure()
        raise

# Validate Deployment with Boto3
def validate_aws_resources(instance_id: str, alb_name: str):
    try:
        ec2 = boto3.client("ec2", region_name=REGION)
        elb = boto3.client("elbv2", region_name=REGION)
        
        # Get EC2 instance
        instances = ec2.describe_instances(InstanceIds=[instance_id])
        instance = instances["Reservations"][0]["Instances"][0]
        instance_state = instance["State"]["Name"]
        public_ip = instance.get("PublicIpAddress", "Not Assigned")
        
        # Get ALB
        load_balancers = elb.describe_load_balancers(Names=[alb_name])
        alb_dns = load_balancers["LoadBalancers"][0]["DNSName"]
        
        aws_data = {
            "instance_id": instance_id,
            "instance_state": instance_state,
            "public_ip": public_ip,
            "load_balancer_dns": alb_dns
        }
        
        with open("aws_validation.json", "w") as f:
            json.dump(aws_data, f, indent=4)
        
        print("\nAWS Validation Data:", aws_data)
    except Exception as e:
        print("Error validating AWS resources:", e)

# Destroy Infrastructure
def destroy_infrastructure():
    try:
        tf = Terraform()
        tf.destroy(auto_approve=True)
        print("Infrastructure destroyed!")
    except Exception as e:
        print("Error destroying infrastructure:", e)

if __name__ == "__main__":
    user_input = get_user_input()
    generate_terraform_config(user_input)

    print("\nDeploying Infrastructure...")
    outputs = deploy_infrastructure()

    print("\nValidating AWS Deployment...")
    time.sleep(20) 
    validate_aws_resources(outputs['instance_id']['value'], user_input['load_balancer_name'])

    print("\nDeployment Complete! To destroy, run this script again and type 'yes'.")
    destroy = input("Destroy Infrastructure? (yes/no): ").lower()
    if destroy == "yes":
        destroy_infrastructure()
