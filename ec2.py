# #testing 
# import boto3
# #print existing s3 buckets 
# ec2 = boto3.resource('ec2')
# for instance in ec2.instances.all():
#     print(instance.id, instance.state)

# for this we are using resource() not client()
import boto3
from botocore.exceptions import ClientError

# Initialize EC2 resource (high-level)
ec2 = boto3.resource('ec2', region_name='ap-south-1')

# Launch EC2 Instance
def launch_instance(ami_id, instance_type, key_name, sg_id):
    try:
        instance = ec2.create_instances(
            ImageId=ami_id,
            InstanceType=instance_type,
            KeyName=key_name,
            SecurityGroupIds=[sg_id],
            MinCount=1,
            MaxCount=1,
        )[0]
        print(f"Launching EC2 instance... ID: {instance.id}")
        instance.wait_until_running()
        instance.reload()
        print(f"EC2 instance is now running at: {instance.public_dns_name}")
        return instance.id
    except ClientError as e:
        print("Error launching EC2 instance:", e)


# List EC2 Instances
def list_instances():
    print("Listing EC2 Instances:")
    for instance in ec2.instances.all():
        print(f" - ID: {instance.id}, State: {instance.state['Name']}, Type: {instance.instance_type}")


# Example usage
if __name__ == "__main__":
    ami = "ami-0e670eb768a5fc3d4"  # Amazon Linux 2 (ap-south-1)
    instance_type = "t2.micro"
    key_pair = "flask-tf-key"  # your key name
    security_group = "sg-04170c32022113a49"  # your security group ID

    instance_id = launch_instance(ami, instance_type, key_pair, security_group)

    input("\n Press Enter to list all instances...")
    list_instances()