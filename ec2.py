#testing 
import boto3
#print existing s3 buckets 
ec2 = boto3.resource('ec2')
for instance in ec2.instances.all():
    print(instance.id, instance.state)