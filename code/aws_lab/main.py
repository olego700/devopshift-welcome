import boto3

user_choise=input("1-manage s3 buckets\n2-manage ec2 instances\n3-exit\ninput:").strip()

if user_choise=="1":
    s3_choise=input("1-list buckets\n2-create bucket\n3-delete bucket\ninput:").strip()
    if s3_choise=="1":
        try:
            s3_client=boto3.client("s3")
            s3_resource=boto3.resource("s3")
            response=s3_client.list_buckets()
            print(response)
        except:
            print("could not retrive buckets")
    elif s3_choise=="2":
        s3_name=input("enter s3 bucket name:").strip()
        s3_client=boto3.client("s3")
        s3_resource=boto3.resource("s3")
        response=s3_client.list_buckets()
        if s3_name not in response["Buckets"]:
            try:
                s3_client.create_bucket(Bucket=s3_name)
                print(f"created {s3_name} bucket")
            except:
                print("could not create bucket")
        else:
            print("bucket name already exists")
    elif s3_choise=="3":
        s3_name=input("enter s3 bucket name to delete:").strip()
        s3_client=boto3.client("s3")
        s3_resource=boto3.resource("s3")
        response=s3_client.list_buckets()
        if s3_name in response["buckets"]:
            try:
                s3_client.delete_bucket(Bucket=s3_name)
                print(f"deleted {s3_name} bucket")
            except:
                print("could not delete bucket")
        else:
            print("s3 bucket does not exist")
elif user_choise=="2":
    ec2_client=boto3.client("ec2")
    ec2_input=input("1-list instances\n2-start instance\n3-stop instance\n4-terminate instance\ninput:").strip()
    if ec2_input=="1":
        try:
            
            response = ec2_client.describe_instances()
            print(response)
        except:
            print("could not list instances")
    elif ec2_input=="2":
            try:
                ec2_id=input("enter instance ID:").strip()
                ec2_client.start_instances(InstanceIds=["ec2_id"])
            except:
                print("could not start instance")