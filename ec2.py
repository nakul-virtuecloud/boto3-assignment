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

# Stop EC2 Instance
def stop_instance(instance_id):
    try:
        instance = ec2.Instance(instance_id)
        instance.stop()
        print(f"Stopping instance: {instance.id}")
        instance.wait_until_stopped()
        print("Instance stopped.")
    except ClientError as e:
        print("Error stopping instance:", e)

# Terminate EC2 Instance
def terminate_instance(instance_id):
    try:
        instance = ec2.Instance(instance_id)
        instance.terminate()
        print(f"Terminating instance: {instance.id}")
        instance.wait_until_terminated()
        print("Instance terminated.")
    except ClientError as e:
        print("Error terminating instance:", e)




# Example usage
if __name__ == "__main__":
    ami = "ami-0e670eb768a5fc3d4"  # Amazon Linux 2 (ap-south-1)
    instance_type = "t2.micro"
    key_pair = "flask-tf-key"  # your key name
    security_group = "sg-04170c32022113a49"  # your security group ID

    instance_id = None
    confirm = input("🚀 Do you want to launch a new EC2 instance? (yes/no): ").strip().lower()

    if confirm == "yes":
        instance_id = launch_instance(ami, instance_type, key_pair, security_group)
    else:
        print("Skipping EC2 instance launch.")

    # Always list instances
    input("\n⏳ Press Enter to list all instances...")
    list_instances()

    # Ask for ID to stop (manual or newly launched)
    instance_to_stop = input("\n Enter instance ID to stop (or leave blank to skip): ").strip()
    if instance_to_stop:
        stop_instance(instance_to_stop)

    # Ask for ID to terminate
    instance_to_terminate = input("\n Enter instance ID to terminate (or leave blank to skip): ").strip()
    if instance_to_terminate:
        terminate_instance(instance_to_terminate)