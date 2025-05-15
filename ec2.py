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

# 2️⃣ List EC2 Instances
def list_instances():
    print("Listing EC2 Instances:")
    for instance in ec2.instances.all():
        print(f" - ID: {instance.id}, State: {instance.state['Name']}, Type: {instance.instance_type}")


# 🧪 Example usage
if __name__ == "__main__":
    ami = "ami-0e670eb768a5fc3d4"  # ✅ Amazon Linux 2 (ap-south-1)
    instance_type = "t2.micro"
    key_pair = "my-key"  # ✅ your key name
    security_group = "sg-08b8b31d20e27fd4b"  # ✅ your security group ID

    input("\n Press Enter to list all instances...")
    list_instances()